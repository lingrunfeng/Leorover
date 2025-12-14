#!/usr/bin/env python3
"""
Quick test script to disable LeoRover base collisions in planning scene
Run this AFTER launching MTC
"""

import rclpy
from rclpy.node import Node
from moveit_msgs.srv import GetPlanningScene, ApplyPlanningScene
from moveit_msgs.msg import PlanningScene, AllowedCollisionMatrix, AllowedCollisionEntry

class DisableLeoRoverCollisions(Node):
    def __init__(self):
        super().__init__('disable_leorover_collisions')
        
        # Create service clients
        self.get_scene_client = self.create_client(GetPlanningScene, '/get_planning_scene')
        self.apply_scene_client = self.create_client(ApplyPlanningScene, '/apply_planning_scene')
        
        self.get_logger().info('Waiting for planning scene services...')
        self.get_scene_client.wait_for_service(timeout_sec=5.0)
        self.apply_scene_client.wait_for_service(timeout_sec=5.0)
        
        self.disable_leo_collisions()
        
    def disable_leo_collisions(self):
        # LeoRover links to disable
        leo_links = [
            'base_link', 'base_footprint', 'scan_link', 'camera_link',
            'rocker_L_link', 'rocker_R_link',
            'wheel_FL_link', 'wheel_FR_link', 'wheel_RL_link', 'wheel_RR_link'
        ]
        
        # Get current planning scene
        get_req = GetPlanningScene.Request()
        get_req.components.components = get_req.components.ALLOWED_COLLISION_MATRIX
        
        future = self.get_scene_client.call_async(get_req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        
        if not future.result():
            self.get_logger().error('Failed to get planning scene')
            return
            
        scene = future.result().scene
        acm = scene.allowed_collision_matrix
        
        self.get_logger().info(f'Current ACM has {len(acm.entry_names)} entries')
        
        # Add Leo links to ACM if not present
        for link in leo_links:
            if link not in acm.entry_names:
                acm.entry_names.append(link)
                # Add new row
                new_entry = AllowedCollisionEntry()
                new_entry.enabled = [True] * len(acm.entry_names)
                acm.entry_values.append(new_entry)
                
                # Update all existing rows
                for entry in acm.entry_values[:-1]:
                    entry.enabled.append(True)
                    
        # Enable collisions between all Leo links and everything
        for i, name1 in enumerate(acm.entry_names):
            if name1 in leo_links:
                acm.entry_values[i].enabled = [True] * len(acm.entry_names)
                
        self.get_logger().info(f'Updated ACM to {len(acm.entry_names)} entries')
        self.get_logger().info('Disabled collisions for all LeoRover base links')
        
        # Apply modified scene
        apply_req = ApplyPlanningScene.Request()
        apply_req.scene = scene
        
        future = self.apply_scene_client.call_async(apply_req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        
        if future.result() and future.result().success:
            self.get_logger().info('✅ Successfully disabled LeoRover collisions!')
        else:
            self.get_logger().error('❌ Failed to apply planning scene')

def main():
    rclpy.init()
    node = DisableLeoRoverCollisions()
    rclpy.shutdown()
    print('\n✅ LeoRover collisions disabled! You can now test MTC grasp.')
    print('Run: ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped ...')

if __name__ == '__main__':
    main()
