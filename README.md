# 基于树莓派的人体姿态识别系统

## 项目介绍

![usbcam](images/ui/usbcam.jpeg)

本项目是一套基于[MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)构建的人体姿态识别系统，实际运行在树莓派5上，理论上支持全平台使用，支持image、usbcam和webcam三种输入模式，UI界面通过[Gradio](https://www.gradio.app/)实现

## 安装

克隆仓库到本地

```bash
git clone https://github.com/themdeee/RPi-PoseDetector.git
```

安装依赖

```bash
cd RPi-PoseDetector
pip install -r requirements.txt
```

> [!NOTE]
>
> 项目目前限制Gradio版本为5.24.0，Gradio在版本5.25.0中修改了`webcam_options`接口，相关接口适配已在[webcam_options](https://github.com/themdeee/RPi-PoseDetector/tree/webcam_options)分支中完成，但适配后会导致图像串流性能大幅下降，演示效果不佳，故main分支暂时保留使用5.24.0版本Gradio的相关接口

## 开始使用

```python
python main.py
```

