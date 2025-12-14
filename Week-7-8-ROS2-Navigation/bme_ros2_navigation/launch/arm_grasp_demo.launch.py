#!/usr/bin/env python3
"""
机械臂坐标抓取演示启动文件
一键启动完整的抓取测试环境
"""
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_bme_ros2_navigation = get_package_share_directory('bme_ros2_navigation')
    
    # Launch参数
    rviz_arg = DeclareLaunchArgument(
        'rviz', default_value='true',
        description='启动RViz可视化'
    )
    
    world_arg = DeclareLaunchArgument(
        'world', default_value='empty.sdf',
        description='Gazebo世界场景'
    )
    
    x_arg = DeclareLaunchArgument(
        'x', default_value='0.0',
        description='机器人初始X坐标'
    )
    
    y_arg = DeclareLaunchArgument(
        'y', default_value='0.0',
        description='机器人初始Y坐标'
    )
    
    yaw_arg = DeclareLaunchArgument(
        'yaw', default_value='0.0',
        description='机器人初始朝向（弧度）'
    )
    
    # 1. 启动Gazebo和机器人（包含控制器spawner）
    spawn_robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_bme_ros2_navigation, 'launch', 'spawn_robot.launch.py')
        ),
        launch_arguments={
            'world': LaunchConfiguration('world'),
            'x': LaunchConfiguration('x'),
            'y': LaunchConfiguration('y'),
            'yaw': LaunchConfiguration('yaw'),
            'use_sim_time': 'True',
        }.items()
    )
    
    # 2. 启动机械臂坐标控制节点（替代arm_hold_pose）
    arm_coordinate_controller_node = Node(
        package='bme_ros2_navigation',
        executable='arm_coordinate_controller.py',
        name='arm_coordinate_controller',
        output='screen',
        parameters=[{'use_sim_time': True}],
    )
    
    # 3. RViz配置
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', PathJoinSubstitution([pkg_bme_ros2_navigation, 'rviz', 'rviz.rviz'])],
        condition=IfCondition(LaunchConfiguration('rviz')),
        parameters=[{'use_sim_time': True}],
    )
    
    # 创建Launch Description
    ld = LaunchDescription()
    
    # 添加参数
    ld.add_action(rviz_arg)
    ld.add_action(world_arg)
    ld.add_action(x_arg)
    ld.add_action(y_arg)
    ld.add_action(yaw_arg)
    
    # 添加节点和launch文件
    ld.add_action(spawn_robot_launch)
    ld.add_action(arm_coordinate_controller_node)
    ld.add_action(rviz_node)
    
    return ld
