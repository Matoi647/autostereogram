# 生成自动立体图和视频

## 免责声明
为避免可能的法律纠纷和道德风险，使用者在使用本项目前，请务必仔细阅读本条款并同意本声明。使用者使用本项目的行为以及通过各类方式利用本项目的行为，都将被视作是对本声明全部内容的无异议的认可。

1. 本项目遵循BSD 3-Clause开源许可，仅供学习和交流使用，不得用于任何非法用途或非正当用途。
2. 本项目作者从未向任何组织或个人提供任何形式的帮助，不对使用本项目的行为承担任何责任，也不对由此造成的任何损害或侵权行为负责。使用本项目所造成的责任均由使用者自行承担。
3. 未经作者允许，任何人不得转载或二次分发本项目。未经允许私自转载传播者，其造成的后果自行承担。
4. 使用本项目即表示您同意遵守本免责声明，否则请立即停止使用并删除本项目。

以上声明内容的最终解释权归项目作者所有，因使用者违反上述条款中的任意一条或多条而造成的一切后果，均由使用者自行承担，与项目作者无关，特此声明。

## 效果演示
素材来自https://www.bilibili.com/video/BV1x5411o7Kn/

原图

![original image](assets/test.png)

自动立体图

![!autostereogram](assets/test_asg.png)

自动立体图（附有焦点）

![autostereogram(focus)](assets/test_asg_focus.png)
## 使用方法
1. 安装ffmpeg: https://ffmpeg.org/download.html
2. 安装numpy和opencv-python
```
pip install numpy opencv-python
```

克隆项目
```
git clone https://github.com/Matoi647/autostereogram.git
```

制作自动立体图需要使用深度图，如果没有深度图，可以使用`asg.binarize_video()`将图像二值化作为替代
```python
import autostereogram as asg

asg.asg_img(r"YOUR_IMAGE_PATH", r"OUTPUT_PATH")
# asg.binarize_video(r"YOUR_VIDEO_PATH", r"OUTPUT_PATH")
# asg.asg_video(r"YOUR_VIDEO_PATH", r"OUTPUT_PATH")
```
