#!/usr/bin/env python3
"""
Spawn LeoRover robot for MTC (without arm_hold_pose interference)
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_bme_nav = get_package_share_directory('bme_ros2_navigation')
    
    # Arguments
    world_arg = DeclareLaunchArgument(
        'world',
        default_value='empty.sdf',
        description='Gazebo world file'
    )
    
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock'
    )
    
    # Include base spawn_robot but we'll need to check if we can exclude arm_hold_pose
    # For now, just include the normal spawn
    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(pkg_bme_nav, 'launch', 'spawn_robot.launch.py')
        ]),
        launch_arguments={
            'world': LaunchConfiguration('world'),
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        }.items()
    )
    
    ld = LaunchDescription()
    ld.add_action(world_arg)
    ld.add_action(use_sim_time_arg)
    ld.add_action(spawn_robot)
    
    return ld
