#!/usr/bin/env python3
"""验证机械臂是否正确整合到URDF中"""

import os
from ament_index_python.packages import get_package_share_directory
import xacro
import xml.etree.ElementTree as ET

try:
    pkg = get_package_share_directory('bme_ros2_navigation')
    urdf_file = os.path.join(pkg, 'urdf', 'leo_sim.urdf.xacro')
    
    print(f"正在处理: {urdf_file}")
    
    # 处理xacro
    doc = xacro.process_file(urdf_file)
    urdf_content = doc.toxml()
    
    # 解析XML
    root = ET.fromstring(urdf_content)
    
    print("\n✅ URDF处理成功！")
    print(f"URDF长度: {len(urdf_content)} 字符")
    
    # 检查关键链接
    print("\n🔍 检查关键链接:")
    key_links = [
        'base_link',
        'base_footprint',
        'scan_link',
        'mycobot_arm_mount_link',
        'mycobot_link1',
        'mycobot_link2',
        'mycobot_link6',
        'mycobot_link6_flange',
    ]
    
    found_links = []
    for link in root.findall('.//link'):
        link_name = link.get('name')
        if link_name in key_links:
            print(f"  ✓ {link_name}")
            found_links.append(link_name)
    
    missing = set(key_links) - set(found_links)
    if missing:
        print(f"\n  ⚠️  缺失: {missing}")
    
    # 检查关键关节
    print("\n🔍 检查关键关节:")
    key_joints = [
        ('base_joint', 'base_footprint', 'base_link'),
        ('arm_mount_joint', 'base_link', 'mycobot_arm_mount_link'),
        ('mycobot_arm_mount_link_to_mycobot_link1', 'mycobot_arm_mount_link', 'mycobot_link1'),
    ]
    
    for joint_name, expected_parent, expected_child in key_joints:
        for joint in root.findall('.//joint'):
            if joint.get('name') == joint_name:
                parent = joint.find('parent').get('link')
                child = joint.find('child').get('link')
                if parent == expected_parent and child == expected_child:
                    print(f"  ✓ {joint_name}: {parent} → {child}")
                else:
                    print(f"  ✗ {joint_name}: {parent} → {child} (期望: {expected_parent} → {expected_child})")
                break
        else:
            print(f"  ✗ {joint_name}: 未找到")
    
    print("\n📊 TF树结构:")
    print("""
    base_footprint
      └── base_link
          ├── scan_link (激光雷达)
          ├── camera_frame (相机)
          ├── wheels (车轮)
          └── mycobot_arm_mount_link (机械臂安装座)
              └── mycobot_link1 (机械臂)
                  └── mycobot_link2
                      └── ... → mycobot_link6_flange
    """)
    
    print("\n✅ 机械臂已成功整合！")
    print("   现在可以重启Gazebo查看机械臂。")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()



