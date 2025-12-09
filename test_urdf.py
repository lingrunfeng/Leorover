#!/usr/bin/env python3

"""
测试URDF文件是否正确加载
"""

import os
from ament_index_python.packages import get_package_share_directory
import xacro

try:
    # 获取包路径
    pkg_bme_ros2_navigation = get_package_share_directory('bme_ros2_navigation')
    
    # URDF文件路径
    urdf_file = os.path.join(pkg_bme_ros2_navigation, 'urdf', 'leo_sim.urdf.xacro')
    
    print(f"正在处理URDF文件: {urdf_file}")
    
    # 处理xacro文件
    robot_description = xacro.process_file(urdf_file)
    urdf_content = robot_description.toxml()
    
    print("\n✅ URDF文件处理成功！")
    print(f"生成的URDF长度: {len(urdf_content)} 字符")
    
    # 检查关键链接是否存在
    key_links = [
        'base_link',
        'base_footprint',
        'scan_link',
        'arm_mount_link',
        'mycobot_link1',
        'mycobot_link2',
        'mycobot_link6',
    ]
    
    print("\n检查关键链接:")
    for link in key_links:
        if link in urdf_content:
            print(f"  ✓ {link} 存在")
        else:
            print(f"  ✗ {link} 不存在")
    
    # 保存URDF到文件以便查看
    output_file = '/home/student26/Leorover/robot_with_arm.urdf'
    with open(output_file, 'w') as f:
        f.write(urdf_content)
    print(f"\n完整URDF已保存到: {output_file}")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()



