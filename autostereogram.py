import numpy as np
import cv2
import os
import subprocess


def generate_autostereogram(depth_map, pattern, shift_factor=20, ):
    """
    Generate autostereogram

    :param depth_map: depth map image, if you don't have depth map image, 
                      try using binarized image to substitute
    :param pattern: background pattern image
    :param shift_factor: number of pixels shifted
    :return output
    """
    height, width = depth_map.shape
    pattern_height, pattern_width, channels = pattern.shape

    # tile pattern by height to align with depth map
    if pattern_height < height:
        pattern = tile_image(pattern, height, pattern_width)
        pattern_height = height

    # copy pattern to the left region of output autostereogram
    output = np.zeros((height, width, channels), dtype=np.uint8)
    output[:, :pattern_width] = pattern

    y_indices, x_indices = np.meshgrid(np.arange(height), np.arange(width), indexing="ij")
    depth_prop = depth_map.astype(float) / 255
    shift = (x_indices - pattern_width + depth_prop * shift_factor).astype(int)

    # iterate through each column and apply the autostereogram algorithm
    for x in range(pattern_width, width):
        mask = shift[:, x] >= 0
        output[mask, x] = output[y_indices[mask, x], shift[mask, x]]

    return output


def tile_image(img, new_height, new_width):
    """
    Tile image to the given new_height and new_width

    :param new_height: height of tiled image
    :param new_width: width of tiled image
    :return output
    """
    height, width, channels = img.shape
    num_repeat_x = int(np.ceil(new_width / width))
    num_repeat_y = int(np.ceil(new_height / height))
    output = np.tile(img, (num_repeat_y, num_repeat_x, 1))[:new_height, :new_width]
    return output


def generate_pattern(height, width):
    """
    Generate random white noise pattern

    In order to avoid the loss of high-frequency information due to compression, 
    an image of 1/2 of the given height and width is generated 
    and then resized to the given size

    :param height: height of pattern
    :param width: width of pattern
    :return pattern
    """
    pattern = np.random.rand(int(height / 2), int(width / 2))
    pattern = cv2.resize(pattern, (int(width), int(height)))*255
    pattern = np.dstack((pattern, pattern, pattern))
    return pattern


# def generate_pattern(height, width, num_circles, radius_range):
#     """
#     Generate random circles with random color and radius
#     """
#     pattern = np.zeros((height, width, 3), dtype=np.uint8)
#     pattern.fill(255)
#     for i in range(int(num_circles)):
#         x = np.random.randint(0, width-1)
#         y = np.random.randint(0, height-1)
#         r = np.random.randint(radius_range[0], radius_range[1])
#         color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
#         cv2.circle(pattern, (x, y), r, color, -1, cv2.LINE_AA)
#     return pattern


def asg_img(img_dir, output_dir, num_clips=8):
    """
    Generate autostereogram image and save to .png

    :param img_dir: input image file directory
    :param output_dir: output image file directory
    :param num_clips: the number of times the pattern is repeated
    :return None
    """
    file_name = os.path.basename(img_dir)
    file_prefix = os.path.splitext(file_name)[0]
    # read image as gray scale image
    img = cv2.imread(img_dir, 0)
    height, width = img.shape
    pattern = generate_pattern(height, int(width / num_clips))
    img_asg = generate_autostereogram(img, pattern)
    cv2.imwrite(f'{output_dir}\\{file_prefix}_asg.png', img_asg)
    return


def asg_video(video_dir, output_dir, num_clips=8, crf=25):
    """
    Generate autostereogram video and save to .avi

    :param img_dir: input image file directory
    :param output_dir: output image file directory
    :param num_clips: the number of times the pattern is repeated
    :param crf: the quality of video, the smaller the better, but the size is larger
    :return None
    """
    print('reading video...')
    video = cv2.VideoCapture(video_dir)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    video_name = os.path.splitext(os.path.basename(video_dir))[0]

    output_dir = os.path.join(output_dir, f'{video_name}_asg_outputs')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    print('autostereogram processing...')
    # process and write to the folder frame by frame
    i = 0
    while True:
        success, frame = video.read()
        if not success:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pattern = generate_pattern(height, int(width / num_clips))
        frame_asg = generate_autostereogram(frame, pattern)
        frame_asg *= 255
        cv2.imwrite(os.path.join(output_dir, f'{i}.png'), frame_asg)
        i += 1
    video.release()
    print('ffmpeg from img to video...')
    # call ffmpeg to stitch pictures into video, using h264 encoding
    cmd = ['ffmpeg', '-r', f'{fps}', '-f', 'image2',
                     '-i', f'{output_dir}\\%d.png',
                     '-vcodec', 'libx264', '-crf', f'{crf}',
                     f'{output_dir}\\{video_name}_asg.avi']
    subprocess.Popen(cmd)

    print('autostereogram video generated.')
    return

def binarize_image(img):
    """
    Binarize image

    :param img: input image
    :return output: binarized image
    """
    output = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, output = cv2.threshold(output, 128, 255, cv2.THRESH_BINARY)
    return output

def binarize_video(video_dir, output_dir, crf=25):
    """
    Binarize video

    :param img: input image
    :return output: binarized image
    """
    print('reading video...')
    video = cv2.VideoCapture(video_dir)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    video_name = os.path.splitext(os.path.basename(video_dir))[0]

    output_dir = os.path.join(output_dir, f'{video_name}_binarized')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print('binarizing video...')
    # process and write to the folder frame by frame
    i = 0
    while True:
        success, frame = video.read()
        if not success:
            break
        frame = binarize_image(frame)
        cv2.imwrite(os.path.join(output_dir, f'{i}.png'), frame)
        i += 1
    video.release()
    print('ffmpeg from img to video...')
    # call ffmpeg to stitch pictures into video, using h264 encoding
    cmd = ['ffmpeg', '-r', f'{fps}', '-f', 'image2',
                     '-i', f'{output_dir}\\%d.png',
                     '-vcodec', 'libx264', '-crf', f'{crf}',
                     f'{output_dir}\\{video_name}_binarized.avi']

    subprocess.Popen(cmd)
    print('binarize video complete.')
