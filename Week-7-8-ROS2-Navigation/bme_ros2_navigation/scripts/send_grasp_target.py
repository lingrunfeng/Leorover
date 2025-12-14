#!/usr/bin/env python3
"""
发送抓取目标坐标测试脚本
用于向机械臂控制节点发送目标位置，测试坐标抓取功能
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import argparse
import sys


class GraspTargetPublisher(Node):
    def __init__(self):
        super().__init__('grasp_target_publisher')
        self.publisher = self.create_publisher(
            PoseStamped,
            '/target_object_pose',
            10
        )
        self.get_logger().info('抓取目标发布节点已启动')
    
    def send_target(self, x, y, z, frame_id='base_link'):
        """发送目标坐标（单位：米）"""
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = frame_id
        
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z
        
        # 默认姿态（向下抓取）
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0
        msg.pose.orientation.w = 1.0
        
        self.publisher.publish(msg)
        self.get_logger().info(f'✅ 已发送目标坐标: X={x:.3f}m, Y={y:.3f}m, Z={z:.3f}m')
        self.get_logger().info(f'   (参考坐标系: {frame_id})')


# 预设测试位置
PRESETS = {
    'front': {
        'x': 0.25,
        'y': 0.0,
        'z': 0.15,
        'description': '前方中央位置'
    },
    'left': {
        'x': 0.20,
        'y': 0.15,
        'z': 0.12,
        'description': '左前方位置'
    },
    'right': {
        'x': 0.20,
        'y': -0.15,
        'z': 0.12,
        'description': '右前方位置'
    },
    'high': {
        'x': 0.15,
        'y': 0.0,
        'z': 0.25,
        'description': '较高位置'
    },
    'low': {
        'x': 0.20,
        'y': 0.0,
        'z': 0.05,
        'description': '较低位置（接近地面）'
    },
    'far': {
        'x': 0.30,
        'y': 0.0,
        'z': 0.10,
        'description': '较远位置（测试臂展）'
    }
}


def main(args=None):
    parser = argparse.ArgumentParser(description='发送机械臂抓取坐标')
    parser.add_argument('--preset', type=str, choices=list(PRESETS.keys()),
                        help='使用预设位置: ' + ', '.join(PRESETS.keys()))
    parser.add_argument('--x', type=float, help='目标X坐标（米）')
    parser.add_argument('--y', type=float, help='目标Y坐标（米）')
    parser.add_argument('--z', type=float, help='目标Z坐标（米）')
    parser.add_argument('--frame', type=str, default='base_link',
                        help='参考坐标系（默认: base_link）')
    parser.add_argument('--list', action='store_true',
                        help='列出所有预设位置')
    
    # 解析参数（从命令行或ROS2 arguments）
    if '--ros-args' in sys.argv:
        # ROS2 launch file调用
        ros_args_idx = sys.argv.index('--ros-args')
        parsed_args = parser.parse_args(sys.argv[1:ros_args_idx])
    else:
        parsed_args = parser.parse_args()
    
    # 列出预设位置
    if parsed_args.list:
        print("\n📍 可用的预设位置:")
        print("-" * 50)
        for name, preset in PRESETS.items():
            print(f"  {name:10s} - {preset['description']}")
            print(f"             X={preset['x']:.2f}m, Y={preset['y']:.2f}m, Z={preset['z']:.2f}m")
        print("-" * 50)
        print("\n使用方法:")
        print(f"  ros2 run bme_ros2_navigation send_grasp_target.py --preset front")
        print(f"  ros2 run bme_ros2_navigation send_grasp_target.py --x 0.2 --y 0.1 --z 0.15")
        return
    
    rclpy.init(args=args)
    node = GraspTargetPublisher()
    
    # 确定目标坐标
    if parsed_args.preset:
        preset = PRESETS[parsed_args.preset]
        x, y, z = preset['x'], preset['y'], preset['z']
        node.get_logger().info(f'使用预设位置: {parsed_args.preset} - {preset["description"]}')
    elif parsed_args.x is not None and parsed_args.y is not None and parsed_args.z is not None:
        x, y, z = parsed_args.x, parsed_args.y, parsed_args.z
        node.get_logger().info('使用自定义坐标')
    else:
        # 默认使用front预设
        node.get_logger().warn('未指定坐标，使用默认预设: front')
        preset = PRESETS['front']
        x, y, z = preset['x'], preset['y'], preset['z']
    
    # 等待一下让节点完全启动
    rclpy.spin_once(node, timeout_sec=0.5)
    
    # 发送目标
    node.send_target(x, y, z, parsed_args.frame)
    
    # 再等待一下确保消息发送
    rclpy.spin_once(node, timeout_sec=0.5)
    
    node.get_logger().info('✅ 坐标已发送，节点关闭')
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
