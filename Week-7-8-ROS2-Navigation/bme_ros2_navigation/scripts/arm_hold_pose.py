#!/usr/bin/env python3
"""
机械臂保持固定姿态节点
用于导航测试，保持机械臂向上折叠，避免干扰雷达扫描
"""
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class ArmHoldPoseNode(Node):
    def __init__(self):
        super().__init__('arm_hold_pose')
        
        # 创建发布器发送关节轨迹
        self.publisher = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )
        
        # 定义向上折叠的安全姿态 (避开雷达扫描平面)
        # 关节顺序: link1-2, link2-3, link3-4, link4-5, link5-6, link6-flange
        self.safe_pose = [
                     0.0,        # joint1: base，不转
                     -1.5,        # joint2: 大臂前伸（不是完全向上）
                     0.5,        # joint3: 小臂向前
                     0.0,        # joint4
                     0.0,       # joint5: 让末端朝下
                     0.0         # joint6
                      ]

        
        self.get_logger().info('机械臂保持姿态节点已启动')
        self.get_logger().info(f'目标姿态: {self.safe_pose}')
        
        # 延迟发送，等待控制器就绪
        self.timer = self.create_timer(2.0, self.send_hold_command)
        self.command_sent = False
        
    def send_hold_command(self):
        """发送固定姿态指令"""
        if self.command_sent:
            self.timer.cancel()
            return
            
        msg = JointTrajectory()
        msg.joint_names = [
            'mycobot_link1_to_mycobot_link2',
            'mycobot_link2_to_mycobot_link3',
            'mycobot_link3_to_mycobot_link4',
            'mycobot_link4_to_mycobot_link5',
            'mycobot_link5_to_mycobot_link6',
            'mycobot_link6_to_mycobot_link6_flange'
        ]
        
        point = JointTrajectoryPoint()
        point.positions = self.safe_pose
        point.time_from_start = Duration(sec=3, nanosec=0)
        
        msg.points = [point]
        
        self.publisher.publish(msg)
        self.get_logger().info('✅ 已发送固定姿态指令 - 机械臂将保持向上折叠')
        self.command_sent = True


def main(args=None):
    rclpy.init(args=args)
    node = ArmHoldPoseNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
