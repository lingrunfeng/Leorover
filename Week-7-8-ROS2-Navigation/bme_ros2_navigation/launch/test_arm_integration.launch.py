#!/usr/bin/env python3

"""
测试Leorover与机械臂整合的TF树结构
此launch文件只用于验证URDF结构，不启动导航
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    
    # 获取包路径
    pkg_bme_ros2_navigation = get_package_share_directory('bme_ros2_navigation')
    
    # URDF文件路径
    urdf_file = os.path.join(pkg_bme_ros2_navigation, 'urdf', 'leo_sim.urdf.xacro')
    
    # 处理xacro文件
    robot_description_config = xacro.process_file(urdf_file)
    robot_description = {'robot_description': robot_description_config.toxml()}
    
    # Robot State Publisher节点
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )
    
    # Joint State Publisher GUI节点（用于手动测试关节）
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )
    
    # RViz节点
    rviz_config_file = os.path.join(pkg_bme_ros2_navigation, 'rviz', 'nav2_default_view.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )
    
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])


