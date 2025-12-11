#!/usr/bin/env python3
"""
机械臂坐标控制节点（仿真版）
接收目标坐标指令，使用IK计算关节角度，控制机械臂运动
模拟pymycobot的send_coords()功能
"""
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.action import FollowJointTrajectory
from builtin_interfaces.msg import Duration
import numpy as np
import math


class ArmCoordinateController(Node):
    def __init__(self):
        super().__init__('arm_coordinate_controller')
        
        # 订阅目标坐标话题 (用于YOLO等视觉节点发布目标)
        self.pose_subscriber = self.create_subscription(
            PoseStamped,
            '/target_object_pose',
            self.target_pose_callback,
            10
        )
        
        # Action client for trajectory control
        self.trajectory_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/arm_controller/follow_joint_trajectory'
        )
        
        self.get_logger().info('机械臂坐标控制节点已启动 (仿真模式)')
        self.get_logger().info('订阅话题: /target_object_pose')
        
    def target_pose_callback(self, msg: PoseStamped):
        """接收目标坐标并计算IK"""
        x = msg.pose.position.x * 1000  # 转换为mm
        y = msg.pose.position.y * 1000
        z = msg.pose.position.z * 1000
        
        self.get_logger().info(f'收到目标坐标: X={x:.1f}mm, Y={y:.1f}mm, Z={z:.1f}mm')
        
        # 计算IK并发送指令
        joint_angles = self.simple_ik(x, y, z)
        
        if joint_angles is not None:
            self.send_joint_command(joint_angles)
        else:
            self.get_logger().error('IK求解失败，目标可能超出工作空间')
    
    def simple_ik(self, x, y, z):
        """
        简化的IK计算
        对于MyCobot 280，这里使用基于几何的简单IK
        实际应用中可以使用ikpy或其他IK库
        
        返回6个关节角度 [j1, j2, j3, j4, j5, j6]
        """
        # MyCobot 280的连杆长度 (单位:mm)
        L1 = 131.56  # link1 height
        L2 = 110.4   # link2-3 length
        L3 = 96.0    # link3-4 length
        L4 = 73.18   # link4-5 length
        L5 = 45.6    # link5-6 length
        
        # 简化计算：假设垂直向下抓取
        # Joint 1: 绕Z轴旋转对准X-Y平面目标
        j1 = math.atan2(y, x)
        
        # 计算水平距离
        r = math.sqrt(x*x + y*y)
        
        # 末端在base坐标系的高度差
        # 调整Z值基于机械臂base高度
        z_adjusted = z - L1  # 相对于joint2的高度
        
        # 2R平面IK (joint2 and joint3)
        # 简化：假设joint4, j5, j6保持特定配置用于向下抓取
        L_horizontal = L2 + L3  # 简化的水平臂展
        
        # 检查是否在工作空间内
        reach = math.sqrt(r*r + z_adjusted*z_adjusted)
        if reach > L_horizontal + L4:
            self.get_logger().warn(f'目标距离 {reach:.1f}mm 超出最大臂展 {L_horizontal + L4:.1f}mm')
            # 返回一个保守的姿态用于测试
            return [0.0, -1.0, 1.5, 0.0, 1.0, 0.0]
        
        # 简化的关节角度计算 (适用于向下抓取)
        # 这是一个近似解，适合测试用
        j2 = -math.atan2(z_adjusted, r) - 0.5
        j3 = 1.5  # 约90度
        j4 = 0.0
        j5 = 1.0  # 调整使末端向下
        j6 = 0.0
        
        joint_angles = [j1, j2, j3, j4, j5, j6]
        self.get_logger().info(f'IK解: {[f"{a:.2f}" for a in joint_angles]}')
        
        return joint_angles
    
    def send_joint_command(self, joint_angles, duration_sec=3.0):
        """发送关节轨迹指令"""
        goal_msg = FollowJointTrajectory.Goal()
        
        trajectory = JointTrajectory()
        trajectory.joint_names = [
            'mycobot_link1_to_mycobot_link2',
            'mycobot_link2_to_mycobot_link3',
            'mycobot_link3_to_mycobot_link4',
            'mycobot_link4_to_mycobot_link5',
            'mycobot_link5_to_mycobot_link6',
            'mycobot_link6_to_mycobot_link6_flange'
        ]
        
        point = JointTrajectoryPoint()
        point.positions = joint_angles
        point.time_from_start = Duration(sec=int(duration_sec), nanosec=0)
        
        trajectory.points = [point]
        goal_msg.trajectory = trajectory
        
        self.get_logger().info('发送关节轨迹指令...')
        self.trajectory_client.wait_for_server()
        future = self.trajectory_client.send_goal_async(goal_msg)
        future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        """处理action响应"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('目标被拒绝')
            return
        
        self.get_logger().info('✅ 目标已接受，机械臂正在移动...')
        
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)
    
    def result_callback(self, future):
        """处理执行结果"""
        result = future.result().result
        self.get_logger().info(f'✅ 运动完成！状态: {result.error_code}')


def main(args=None):
    rclpy.init(args=args)
    node = ArmCoordinateController()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
