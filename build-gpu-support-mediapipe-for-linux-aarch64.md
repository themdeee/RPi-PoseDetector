# 为Linux-aarch64设备编译带GPU支持的MediaPipe

## 先说结论

- 对于在树莓派5上运行MediaPipe，运行模式选择GPU模式的运行速度并不见得比CPU要快~~也可能是还需在代码层面加入一些GPU加速技巧~~
- 直接拉取MediaPipe源码编译即可，MediaPipe提供的Dockerfile缺乏维护，若使用Docker编译会让修复报错变得复杂麻烦
- 本文主要参考了[MediaPipe官方文档](https://ai.google.dev/edge/mediapipe/framework/getting_started/install?hl=zh-cn#installing_on_debian_and_ubuntu)和[Linux 下编译安装 OpenGL GPU 支持的 mediapipe 指南](https://butui.me/posts/build-mediapipe-from-the-source-with-gpu-support-by-opengl/)，在此致谢



## 前期准备

按照[MediaPipe官方文档](https://ai.google.dev/edge/mediapipe/framework/getting_started/install?hl=zh-cn#installing_on_debian_and_ubuntu)，检查Bazelisk、OpenCV和FFmpeg的安装

拉取MediaPipe源码

```bash
git clone --depth 1 https://github.com/google-ai-edge/mediapipe.git
```



## 修改源码

### ./setup.py

1. 修改`__version__`为`x.x.x`格式的版本号
2. 修改`self.link_opencv`为`True`（目前是4个）



### ./WORKSPACE

由于维护不及时，此处部分sha256校验值可能需要根据实际下载到的文件进行手动更改



### ./third_party/opencv_linux.BULID

根据设备相应类型解注释

```
    hdrs = glob([
        # For OpenCV 4.x
        #"include/aarch64-linux-gnu/opencv4/opencv2/cvconfig.h",
        #"include/arm-linux-gnueabihf/opencv4/opencv2/cvconfig.h",
        #"include/x86_64-linux-gnu/opencv4/opencv2/cvconfig.h",
        #"include/opencv4/opencv2/**/*.h*",
    ]),
    includes = [
        # For OpenCV 4.x
        #"include/aarch64-linux-gnu/opencv4/",
        #"include/arm-linux-gnueabihf/opencv4/",
        #"include/x86_64-linux-gnu/opencv4/",
        #"include/opencv4/",
    ],
```

对于Linux-aarch64设备，则保留以下代码即可

```
    hdrs = glob([
        "include/aarch64-linux-gnu/opencv4/opencv2/cvconfig.h",
        "include/opencv4/opencv2/**/*.h*",
    ]),
    includes = [
        "include/aarch64-linux-gnu/opencv4/",
        "include/opencv4/",
    ],
```



### ./mediapipe/framework/api3/internal/contract_validator.h

修改116行附近

```c++
           using FieldT = std::decay_t<decltype(*field)>::Field;
```

为

```c++
           using FieldT = typename std::decay_t<decltype(*field)>::Field;
```



## 开始编译

```bash
cd mediapipe
export MEDIAPIPE_DISABLE_GPU=0
python -m build --wheel --no-isolation
```



## 运行报错处理

### version `GLIBCXX_3.4.32' not found

对于在Conda虚拟环境中使用自编译MediaPipe时回报此错误，可在Conda环境（名为xxx）中执行以下命令解决

```bash
conda install -n xxx -c conda-forge libstdcxx-ng
```

