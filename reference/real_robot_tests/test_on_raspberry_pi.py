#!/usr/bin/env python3
"""
在树莓派上直接控制myCobot
不需要GUI，不需要ROS2
"""
from pymycobot.mycobot import MyCobot
import time

def test_mycobot():
    print("=" * 60)
    print("🤖 MyCobot 直接控制测试（树莓派）")
    print("=" * 60)
    
    # 连接机械臂
    # 树莓派通过串口连接，通常是 /dev/ttyAMA0 或 /dev/ttyS0
    ports_to_try = ['/dev/ttyAMA0', '/dev/ttyS0', '/dev/ttyUSB0', '/dev/ttyACM0']
    
    mc = None
    for port in ports_to_try:
        try:
            print(f"\n尝试连接到 {port}...")
            mc = MyCobot(port, 115200)
            time.sleep(2)
            
            # 测试连接
            angles = mc.get_angles()
            if angles and len(angles) == 6:
                print(f"✅ 成功连接到 {port}！")
                break
        except Exception as e:
            print(f"❌ {port} 失败: {e}")
    
    if not mc:
        print("\n❌ 无法连接到机械臂！")
        return
    
    # 读取当前状态
    print("\n📊 当前关节角度：")
    angles = mc.get_angles()
    for i, angle in enumerate(angles, 1):
        print(f"   关节 {i}: {angle:>7.2f}°")
    
    print("\n📍 当前末端坐标：")
    coords = mc.get_coords()
    print(f"   X: {coords[0]:>7.2f} mm")
    print(f"   Y: {coords[1]:>7.2f} mm")
    print(f"   Z: {coords[2]:>7.2f} mm")
    
    # 交互式控制
    print("\n" + "=" * 60)
    print("🎮 交互式控制")
    print("=" * 60)
    
    while True:
        print("\n选择测试：")
        print("  1 - 移动到HOME位置（所有关节归零）")
        print("  2 - 测试单个关节")
        print("  3 - 测试夹爪")
        print("  4 - 读取当前状态")
        print("  q - 退出")
        
        choice = input("\n请选择: ").strip()
        
        if choice == 'q':
            print("\n👋 退出控制")
            break
        
        elif choice == '1':
            print("\n🏠 移动到HOME位置...")
            confirm = input("   确认？(y/n): ")
            if confirm.lower() == 'y':
                mc.send_angles([0, 0, 0, 0, 0, 0], 20)
                print("   ⏳ 移动中，等待6秒...")
                time.sleep(6)
                print("   ✅ 完成")
        
        elif choice == '2':
            joint = input("   选择关节 (1-6): ")
            angle = input("   目标角度 (-165 to 165): ")
            try:
                joint_num = int(joint)
                target_angle = float(angle)
                print(f"   ⏳ 移动关节{joint_num}到{target_angle}°...")
                mc.send_angle(joint_num, target_angle, 20)
                time.sleep(3)
                print("   ✅ 完成")
            except:
                print("   ❌ 输入无效")
        
        elif choice == '3':
            print("\n🤏 夹爪控制")
            print("   1 - 打开夹爪")
            print("   2 - 关闭夹爪")
            gripper_choice = input("   选择: ")
            if gripper_choice == '1':
                mc.set_gripper_value(100, 50)
                print("   ✅ 夹爪已打开")
            elif gripper_choice == '2':
                mc.set_gripper_value(0, 50)
                print("   ✅ 夹爪已关闭")
        
        elif choice == '4':
            angles = mc.get_angles()
            coords = mc.get_coords()
            print("\n📊 当前状态：")
            print("   关节角度：", [f"{a:.1f}°" for a in angles])
            print("   末端坐标：", [f"{c:.1f}" for c in coords[:3]], "mm")

if __name__ == '__main__':
    test_mycobot()
