#!/usr/bin/env python3
"""
第一步：USB连接测试
目的：验证机械臂是否正确连接
"""
from pymycobot.mycobot import MyCobot
import time
import sys

def test_connection():
    print("=" * 60)
    print("🔌 MyCobot 280 Pi USB连接测试")
    print("=" * 60)
    
    # 常见的串口设备名
    possible_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyAMA0']
    
    mc = None
    connected_port = None
    
    # 尝试所有可能的端口
    for port in possible_ports:
        try:
            print(f"\n📡 尝试连接到 {port}...")
            mc = MyCobot(port, 115200)
            time.sleep(2)  # 等待连接稳定
            
            # 测试读取角度
            angles = mc.get_angles()
            if angles and len(angles) == 6:
                connected_port = port
                print(f"✅ 成功连接到 {port}！")
                break
            else:
                print(f"❌ {port} 无响应或数据无效")
        except Exception as e:
            print(f"❌ {port} 连接失败: {e}")
    
    if not mc or not connected_port:
        print("\n" + "=" * 60)
        print("❌ 无法连接到机械臂！")
        print("\n请检查：")
        print("1. USB线是否已连接")
        print("2. 机械臂是否已上电")
        print("3. 运行以下命令查看设备：")
        print("   ls /dev/ttyUSB* /dev/ttyACM*")
        print("4. 如需要权限，运行：")
        print("   sudo chmod 666 /dev/ttyUSB0  (或其他设备)")
        print("=" * 60)
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ 连接成功！开始运行测试...")
    print("=" * 60)
    
    # 测试1：读取关节角度
    print("\n📊 测试1：读取当前关节角度")
    try:
        angles = mc.get_angles()
        if angles:
            print(f"✅ 成功读取 6 个关节角度：")
            for i, angle in enumerate(angles, 1):
                print(f"   关节 {i}: {angle:>7.2f}°")
        else:
            print("❌ 无法读取关节角度")
    except Exception as e:
        print(f"❌ 读取失败: {e}")
    
    # 测试2：读取坐标
    print("\n📍 测试2：读取当前末端坐标")
    try:
        coords = mc.get_coords()
        if coords:
            print(f"✅ 成功读取末端坐标：")
            print(f"   X: {coords[0]:>7.2f} mm")
            print(f"   Y: {coords[1]:>7.2f} mm")
            print(f"   Z: {coords[2]:>7.2f} mm")
            print(f"   RX: {coords[3]:>7.2f}°")
            print(f"   RY: {coords[4]:>7.2f}°")
            print(f"   RZ: {coords[5]:>7.2f}°")
        else:
            print("❌ 无法读取坐标")
    except Exception as e:
        print(f"❌ 读取失败: {e}")
    
    # 测试3：夹爪测试
    print("\n🤏 测试3：夹爪控制测试")
    try:
        response = input("是否测试夹爪？(y/n): ")
        if response.lower() == 'y':
            print("   打开夹爪...")
            mc.set_gripper_value(100, 50)
            time.sleep(2)
            print("   关闭夹爪...")
            mc.set_gripper_value(0, 50)
            time.sleep(2)
            print("✅ 夹爪测试完成")
        else:
            print("⏭️  跳过夹爪测试")
    except Exception as e:
        print(f"⚠️  夹爪测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 所有基础测试完成！")
    print(f"📌 成功连接的端口: {connected_port}")
    print(f"📌 波特率: 115200")
    print("\n下一步：运行 python3 2_simple_move_test.py")
    print("=" * 60)

if __name__ == '__main__':
    test_connection()
