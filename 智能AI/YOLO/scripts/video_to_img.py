import cv2
import time
import os

# 确保 images 文件夹存在
images_folder = 'images'
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# 初始化摄像头
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 获取时间的初始刻度
start_time = time.time()
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法读取帧")
        break

    cv2.imshow('frame', frame)
    
    # 计算当前时间
    current_time = time.time()
    
    # 检查是否已经过去1秒
    if current_time - start_time >= 1:
        # 更新开始时间
        start_time = current_time
        # 更新帧计数
        frame_count += 1
        
        # 保存当前帧为图片，文件名包含帧编号到 images 文件夹
        filename = os.path.join(images_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(filename, frame)
        print(f"已保存图片: {filename}")
    
    # 按 'q' 退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()
# 关闭所有OpenCV窗口
cv2.destroyAllWindows()