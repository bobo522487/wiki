import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped, Twist
from sensor_msgs.msg import Imu

class PIDController:
    def __init__(self, kp, kp2, kd, kd2):
        # PID控制器初始化
        self.kp = kp  # 比例系数
        self.kp2 = kp2  # 非线性比例系数
        self.kd = kd  # 微分系数
        self.kd2 = kd2  # 微分项的补偿系数
        self.prev_position_error = 0  # 上一次的位置误差

    def update(self, position_error, angular_velocity):
        # 更新PID控制器的输出
        proportional_term = position_error * self.kp + abs(position_error) * position_error * self.kp2
        derivative_term = (position_error - self.prev_position_error) * self.kd
        gyro_term = angular_velocity * self.kd2
        output = proportional_term + derivative_term + gyro_term
        self.prev_position_error = position_error
        return output

class LineFollowingController(Node):
    def __init__(self):
        super().__init__('line_following_controller')
        # 从参数服务器获取PID参数，如果没有设置则使用默认值
        self.pid_controller = self.get_pid_controller()

        self.current_x = 0
        self.bottom_center = 380  # 目标X坐标
        self.linear_velocity = 0.2  # 线速度

        # 创建订阅者和发布者
        self.create_subscription(PointStamped, '/yolo/detect_pos', self.yolo_callback, 10)
        self.create_subscription(Imu, '/imu/data', self.imu_callback, 10)
        self.cmd_vel_publisher = self.create_publisher(Twist, "/cmd_vel", 1)

    def get_pid_controller(self):
        # 从参数服务器获取PID参数，如果没有设置则使用默认值
        kp = self.get_parameter('kp').get_parameter_value().double_value
        kp2 = self.get_parameter('kp2').get_parameter_value().double_value
        kd = self.get_parameter('kd').get_parameter_value().double_value
        kd2 = self.get_parameter('kd2').get_parameter_value().double_value
        return PIDController(kp, kp2, kd, kd2)

    def yolo_callback(self, msg):
        # yolo_callback回调函数，处理YOLO检测结果
        try:
            if msg is None or (msg.point.x == 0 and msg.point.y == 0 and msg.point.z == 0): 
                self.publish_empty_twist()  # 发布空的Twist消息
            else:
                self.current_x = msg.point.x
                position_error = self.current_x - self.bottom_center

                cmd_vel = Twist()
                if abs(position_error) < 30:
                    cmd_vel.angular.z = 0.0
                else:
                    cmd_vel.angular.z = self.pid_controller.update(position_error, self.angular_velocity)
                cmd_vel.linear.x = self.linear_velocity
                self.cmd_vel_publisher.publish(cmd_vel)  # 发布Twist消息
        except Exception as e:
            self.get_logger().warn(f'Error in yolo_callback: {e}')

    def imu_callback(self, msg):
        # imu_callback回调函数，处理IMU数据
        try:
            self.angular_velocity = msg.angular_velocity.z  # 更新角速度
        except Exception as e:
            self.get_logger().warn(f'Error in imu_callback: {e}')

    def publish_empty_twist(self):
        # 发布空的Twist消息
        cmd_vel = Twist()
        self.cmd_vel_publisher.publish(cmd_vel)

def main(args=None):
    rclpy.init(args=args)
    linedetect = LineFollowingController()
    try:
        rclpy.spin(linedetect)
    except KeyboardInterrupt:
        pass
    finally:
        linedetect.publish_empty_twist()
        linedetect.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
