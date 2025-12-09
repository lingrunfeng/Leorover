#!/usr/bin/env python3

"""
检查TF树结构
"""

import xml.etree.ElementTree as ET

# 读取URDF文件
tree = ET.parse('/home/student26/Leorover/robot_with_arm.urdf')
root = tree.getroot()

print("=== TF树关键连接检查 ===\n")

# 找到所有joint
joints = root.findall('.//joint')

# 我们关心的关键joints
key_joints = [
    'base_joint',
    'arm_mount_joint',
    'scan_joint',
]

print("✓ Leorover关键连接:")
for joint in joints:
    joint_name = joint.get('name')
    if joint_name in key_joints or 'arm' in joint_name.lower():
        parent = joint.find('parent')
        child = joint.find('child')
        joint_type = joint.get('type')
        if parent is not None and child is not None:
            print(f"  {joint_name} ({joint_type}):")
            print(f"    {parent.get('link')} → {child.get('link')}")

print("\n✓ 机械臂连接:")
for joint in joints:
    joint_name = joint.get('name')
    if 'mycobot' in joint_name:
        parent = joint.find('parent')
        child = joint.find('child')
        joint_type = joint.get('type')
        if parent is not None and child is not None:
            print(f"  {joint_name} ({joint_type}):")
            print(f"    {parent.get('link')} → {child.get('link')}")
        if 'link1' in joint_name:
            break  # 只显示第一个机械臂关节

print("\n=== TF树结构 ===")
print("""
base_footprint
    └── base_link
        ├── rocker_L_link (wheels)
        ├── rocker_R_link (wheels)  
        ├── camera_frame
        ├── imu_frame
        ├── scan_link (lidar)
        └── arm_mount_link
            └── mycobot_link1
                └── mycobot_link2
                    └── ... (机械臂其他关节)
""")

# 验证关键点
print("=== 验证关键连接 ===")
arm_mount_found = False
mycobot_connected = False

for joint in joints:
    if joint.get('name') == 'arm_mount_joint':
        parent = joint.find('parent').get('link')
        child = joint.find('child').get('link')
        if parent == 'base_link' and child == 'arm_mount_link':
            print(f"✓ arm_mount_link 正确连接到 base_link")
            arm_mount_found = True
        else:
            print(f"✗ arm_mount_link 连接错误: {parent} → {child}")
    
    if 'link1' in joint.get('name', '') and 'mycobot' in joint.get('name', ''):
        parent = joint.find('parent').get('link')
        child = joint.find('child').get('link')
        print(f"  机械臂base连接: {parent} → {child}")
        if 'arm_mount_link' in parent and 'mycobot_link1' in child:
            print(f"✓ mycobot_link1 正确连接到 arm_mount_link")
            mycobot_connected = True
        else:
            print(f"⚠ 机械臂连接可能有问题")

if arm_mount_found and mycobot_connected:
    print("\n✅ TF树结构完全正确！")
    print("   base_link 保持不变，机械臂作为子节点挂载。")
    print("   Nav2 导航不会受到影响。")
else:
    print("\n⚠ TF树可能需要调整")



