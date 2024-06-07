



### 

#### 环境yolo安装

```
1.显卡驱动查看
nvidia-smi

2.yolo源码与模型
https://hub.nuaa.cf/ultralytics/ultralytics
https://github.com/ultralytics/ultralytics

3.anaconda
https://www.anaconda.com/download
https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
环境变量：
C:\ProgramData\miniconda3
C:\ProgramData\miniconda3\Scripts
C:\ProgramData\miniconda3\Library\bin

4.创建python环境
conda create -n yolo python==3.8
查看现有环境
conda env list
激活环境
conda activate yolo
激活失败
conda init cmd.exe
删除环境
conda env remove -n yolo

5.安装库
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple torch torchvision torchaudio	# CPU
pip3 install torch torchvision torchaudio --index-url  #GUP https://download.pytorch.org/whl/cu118
pip install ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install onnx -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install onnxsim -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install onnxruntime -i https://pypi.tuna.tsinghua.edu.cn/simple


修改输出维度
gitub镜像下载地址:https://hub.nuaa.cf/shouxieai/infer
python v8trans.py best.onnx

推理检测
yolo predict model=yolov8n.pt source=4.png



```



YOLOv8n 模型导出为不同的格式

```
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load an official model
model = YOLO('path/to/best.pt')  # load a custom trained model

# Export the model
model.export(format='onnx')
```



```
yolo export model=yolov8n.pt format=onnx  # export official model
yolo export model=path/to/best.pt format=onnx  # export custom trained model
```



```
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple ultralytics
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple onnx
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple onnxruntime
```

yolo detect train data=coco8.yaml model=yolov8n.pt epochs=100 imgsz=640