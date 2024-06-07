



### 环境onnx安装

```
import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.onnx', task='detect')

# HTTP stream URL
stream_url = "http://dsm.t-plus.com.cn:7088/udp/238.255.2.16:5999"

# Open the video stream
cap = cv2.VideoCapture(stream_url)

while cap.isOpened():
    # Read a frame from the stream
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Process results list
        for result in results:
            pass
            # print(result.boxes.xywhn)
            # print(result.probs)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the stream is reached or there's an error
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
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