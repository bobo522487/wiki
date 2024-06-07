import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
from time import sleep
import numpy as np
import math

class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')
        self.declare_parameter('cmd_vel_topic', '/turtle1/cmd_vel')
        self.declare_parameter('pose_topic', '/turtle1/pose')
        self.cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        self.pose_topic = self.get_parameter('pose_topic').value
        self.subscriber = self.create_subscription(Pose, self.pose_topic, self.pose_callback, 10)
        self.publisher = self.create_publisher(Twist, self.cmd_vel_topic, 10)
        self.cmd_msg = Twist()
        self.rate = self.create_rate(10)
        self.pull_point = 0.3
        self.kp = 10.0
        self.robot_speed = 1.5
        self.no_points = 100
        self.position = [0.0, 0.0]
        self.orientation = 0.0

    def pose_callback(self, msg):
        self.position = [msg.x, msg.y]
        self.orientation = msg.theta

    def goTo(self, goal_pose):
        point = [goal_pose.position.x, goal_pose.position.y]
        path = self.calculate_path(point)
        total_time = self.calculate_distance(path) / self.robot_speed
        for i in range(self.no_points):
            pull_point = [self.position[0] + self.pull_point * np.cos(self.orientation),
                          self.position[1] + self.pull_point * np.sin(self.orientation)]
            next_point = path[:, i]
            err_distance_x = next_point[0] - pull_point[0]
            err_distance_y = next_point[1] - pull_point[1]
            v_x = self.kp * err_distance_x
            v_y = self.kp * err_distance_y
            v_tangent = v_x * np.cos(self.orientation) + v_y * np.sin(self.orientation)
            v_perpendicular = -v_x * np.sin(self.orientation) + v_y * np.cos(self.orientation)
            self.cmd_msg.linear.x = v_tangent
            self.cmd_msg.angular.z = v_perpendicular * self.pull_point
            self.publisher.publish(self.cmd_msg)
            self.rate.sleep()

    def calculate_distance(self, path):
        distance = 0.0
        for i in range(1, len(path[0])):
            distance += np.linalg.norm(np.array([path[0][i-1], path[1][i-1]]) - np.array([path[0][i], path[1][i]]))
        return distance

    def calculate_path(self, goal_point):
        x0 = self.position[0] + self.pull_point * np.cos(self.orientation)
        y0 = self.position[1] + self.pull_point * np.sin(self.orientation)
        x1 = goal_point[0]
        y1 = goal_point[1]
        x = np.linspace(x0, x1, self.no_points)
        y_prime = (y1 - y0) / (x1 - x0)
        y0_prime = self.orientation
        A = np.array([[x0**3, x0**2, x0, 1.0],
                      [3*x0**2, 2*x0, 1.0, 0.0],
                      [x1**3, x1**2, x1, 1],
                      [3*x1**2, 2*x1, 1.0, 0.0]])
        C = np.array([y0, y0_prime, y1, y_prime]).reshape(4, 1)
        a, b, c, d = np.dot(np.linalg.inv(A), C)
        y = a*x**3 + b*x**2 + c*x + d
        path = np.array([y, x])
        return path

def main(args=None):
    rclpy.init(args=args)
    controller = TurtleController()
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
