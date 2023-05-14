import autostereogram as asg

if __name__ == '__main__':
    # you should use depth map as input, 
    # if you don't have depth map, 
    # try using binarized image to substitute

    asg.asg_img(r"assets\test.png", r"assets")
    # asg.binarize_video(r"assets\bad_apple_clip.mp4", r"assets")
    # asg.asg_video(r"assets\bad_apple_clip.mp4", r"assets")
