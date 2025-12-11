#!/usr/bin/env python3
"""
第二步：简单运动测试
目的：安全地测试机械臂运动功能
警告：请确保机械臂周围没有障碍物！
"""
from pymycobot.mycobot import MyCobot
import time
import sys

def find_robot():
    """查找并连接机械臂"""
    possible_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyAMA0']
    
    for port in possible_ports:
        try:
            mc = MyCobot(port, 115200)
            time.sleep(1)
            angles = mc.get_angles()
            if angles and len(angles) == 6:
                print(f"✅ 已连接到 {port}")
                return mc, port
        except:
            continue
    
    print("❌ 无法连接到机械臂！请先运行 1_test_usb_connection.py")
    sys.exit(1)

def simple_move_test():
    print("=" * 60)
    print("🤖 MyCobot 简单运动测试")
    print("=" * 60)
    
    # 连接机械臂
    mc, port = find_robot()
    
    print("\n⚠️  警告：机械臂即将移动！")
    print("⚠️  请确保：")
    print("   1. 机械臂已固定在桌面上")
    print("   2. 周围没有障碍物")
    print("   3. 人员保持安全距离")
    print("   4. 准备好随时关闭电源\n")
    
    response = input("确认安全后，输入 'yes' 开始测试: ")
    if response.lower() != 'yes':
        print("❌ 测试已取消")
        sys.exit(0)
    
    # 读取当前位置
    print("\n📍 当前位置：")
    current_angles = mc.get_angles()
    for i, angle in enumerate(current_angles, 1):
        print(f"   关节 {i}: {angle:>7.2f}°")
    
    # 测试1：移动到HOME位置（所有关节归零）
    print("\n🏠 测试1：移动到HOME位置（速度：20%）")
    print("   目标：所有关节 = 0°")
    response = input("   继续？(y/n): ")
    if response.lower() == 'y':
        mc.send_angles([0, 0, 0, 0, 0, 0], 20)  # 速度20，很慢很安全
        print("   ⏳ 移动中...")
        time.sleep(6)
        
        final_angles = mc.get_angles()
        print("   ✅ 到达位置：")
        for i, angle in enumerate(final_angles, 1):
            print(f"      关节 {i}: {angle:>7.2f}°")
    
    # 测试2：轻微移动关节2（肩部）
    print("\n💪 测试2：轻微移动肩部关节（关节2）")
    print("   动作：关节2从0°移动到30°再回到0°")
    response = input("   继续？(y/n): ")
    if response.lower() == 'y':
        print("   ⏳ 移动到 30°...")
        mc.send_angle(2, 30, 20)  # 关节2，30度，速度20
        time.sleep(3)
        
        print("   ⏳ 返回到 0°...")
        mc.send_angle(2, 0, 20)
        time.sleep(3)
        print("   ✅ 完成")
    
    # 测试3：轻微移动关节3（肘部）
    print("\n🦾 测试3：轻微移动肘部关节（关节3）")
    print("   动作：关节3从0°移动到-30°再回到0°")
    response = input("   继续？(y/n): ")
    if response.lower() == 'y':
        print("   ⏳ 移动到 -30°...")
        mc.send_angle(3, -30, 20)
        time.sleep(3)
        
        print("   ⏳ 返回到 0°...")
        mc.send_angle(3, 0, 20)
        time.sleep(3)
        print("   ✅ 完成")
    
    # 测试4：末端坐标控制测试
    print("\n📐 测试4：末端坐标控制（轻微前后移动）")
    response = input("   继续？(y/n): ")
    if response.lower() == 'y':
        current_coords = mc.get_coords()
        print(f"   当前X坐标: {current_coords[0]:.2f} mm")
        
        # 向前移动2cm
        new_x = current_coords[0] + 20
        print(f"   ⏳ 向前移动20mm (X: {new_x:.2f})...")
        mc.send_coord(1, new_x, 15)  # X轴，速度15
        time.sleep(3)
        
        # 返回
        print(f"   ⏳ 返回原位 (X: {current_coords[0]:.2f})...")
        mc.send_coord(1, current_coords[0], 15)
        time.sleep(3)
        print("   ✅ 完成")
    
    # 返回HOME
    print("\n🏠 测试完成，返回HOME位置")
    mc.send_angles([0, 0, 0, 0, 0, 0], 20)
    time.sleep(6)
    
    print("\n" + "=" * 60)
    print("🎉 所有运动测试完成！")
    print("\n✅ 机械臂运动正常")
    print("✅ 可以进行下一步测试")
    print("\n下一步：运行 python3 3_downward_reach_real_test.py")
    print("=" * 60)

if __name__ == '__main__':
    simple_move_test()
