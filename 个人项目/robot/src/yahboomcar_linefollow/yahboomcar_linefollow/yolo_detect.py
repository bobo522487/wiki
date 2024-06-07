import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO

class YOLODetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')
        self.publisher = self.create_publisher(PointStamped, '/yolo/detect_pos', 10)
        self.cap = cv2.VideoCapture(0)  # 初始化视频捕获对象
        self.bridge = CvBridge()

        # Load YOLO model
        self.model = YOLO('/root/yahboomcar_ros2_ws/yahboomcar_ws/src/yahboomcar_linefollow/yolov8n.onnx')

    def detect(self, frame):
        results = self.model(frame)  # Run inference on the frame

        best_detection = None  # Initialize best_detection variable

        for r in results:
            boxes = r.boxes  # Boxes object for bbox outputs

            bounding_boxes = (
                boxes.xywh.cpu().numpy()
            )  # Convert bounding boxes to numpy array
            classes = boxes.cls.cpu().numpy().astype(int)  # Convert classes to numpy array
            confidences = boxes.conf.cpu().numpy()  # Convert confidences to numpy array

            # Filter out detections with class_id == 0 (person)
            person_indices = np.where(classes == 0)[0]
            if len(person_indices) == 0:
                continue

            # Find index of maximum confidence among detections with class_id == 0
            max_confidence_idx = person_indices[np.argmax(confidences[person_indices])]
            max_confidence = confidences[max_confidence_idx]  # Get maximum confidence

            x, y, w, h = bounding_boxes[max_confidence_idx]  # Extract bounding box coordinates
            center_x = int(x + w / 2)  # Calculate center x-coordinate
            center_y = int(y + h / 2)  # Calculate center y-coordinate

            best_detection = {
                "bbox": bounding_boxes[max_confidence_idx],
                "class_id": classes[max_confidence_idx],
                "confidence": max_confidence,
                "center_x": center_x,
                "center_y": center_y,
            }

        self.draw_detection(frame, best_detection)

        return best_detection

    def draw_detection(self, frame, detection):
        """Draw bounding box and label on the frame."""
        if detection is not None:
            x, y, w, h = detection["bbox"]
            x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)

            # Draw bounding box with red color
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # Calculate center coordinates
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Add label with class name, confidence, and center coordinates
            label = f"Person {detection['confidence']:.2f} (X: {center_x}, Y: {center_y})"
            print(label)
            cv2.putText(
                frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2
            )

            # Draw center point
            cv2.circle(frame, (center_x, center_y), 3, (0, 0, 255), -1)


    def main_loop(self):
        while True:
            # Read a frame from the video
            ret, frame = self.cap.read()
            if not ret:
                self.get_logger().info("End of video.")
                break

            # Perform object detection on the frame
            detections = self.detect(frame)

            if detections is not None:

                center_x = float(detections['center_x'])
                center_y = float(detections['center_y'])

                # Publish detection result
                msg = PointStamped()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = 'volo_detection'
                msg.point.x = center_x
                msg.point.y = center_y
                msg.point.z = float(0)
                self.publisher.publish(msg)

            else:
                msg = PointStamped()
                self.publisher.publish(msg)
                self.get_logger().warn("No detections found.")

            # Display the frame with detections
            cv2.imshow("Object Detection", frame)

            # Break the loop if 'q' is pressed or if the window is closed
            if cv2.waitKey(1) & 0xFF == ord("q") or cv2.getWindowProperty("Object Detection", cv2.WND_PROP_VISIBLE) < 1:
                break

        # Release the video capture object and close all windows
        self.cap.release()
        cv2.destroyAllWindows()


def main(args=None):
    rclpy.init(args=args)
    yolo_detector = YOLODetector()
    yolo_detector.main_loop()
    yolo_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
