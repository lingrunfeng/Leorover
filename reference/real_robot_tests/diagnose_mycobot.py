#!/usr/bin/env python3
"""
完整的myCobot通信诊断脚本
"""
import serial
import time
import sys

print("=" * 70)
print("🔍 myCobot 280 Pi 通信诊断")
print("=" * 70)

# 测试1: 直接串口通信
print("\n📡 测试1: 检查串口通信")
try:
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=2)
    print(f"✅ 串口已打开: {ser.name}")
    print(f"   波特率: {ser.baudrate}")
    print(f"   超时: {ser.timeout}秒")
    
    # 发送简单命令测试
    print("\n   发送测试字节...")
    ser.write(b'\xFE\xFE\x02\x20\xFA')  # 简单的myCobot命令
    time.sleep(0.5)
    
    # 读取响应
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting)
        print(f"   ✅ 收到响应: {response.hex()}")
    else:
        print(f"   ⚠️  无响应（in_waiting: {ser.in_waiting}）")
    
    ser.close()
except Exception as e:
    print(f"❌ 串口测试失败: {e}")
    sys.exit(1)

# 测试2: 使用pymycobot (旧API)
print("\n📡 测试2: pymycobot.MyCobot")
try:
    from pymycobot.mycobot import MyCobot
    
    mc = MyCobot('/dev/ttyAMA0', 115200)
    time.sleep(2)
    
    result = mc.get_angles()
    print(f"   get_angles() 返回: {result}")
    
    if result == -1 or result is None:
        print("   ⚠️  旧版API返回-1，尝试其他波特率...")
        
        # 尝试1000000波特率
        mc2 = MyCobot('/dev/ttyAMA0', 1000000)
        time.sleep(2)
        result2 = mc2.get_angles()
        print(f"   波特率1000000: {result2}")
        
except Exception as e:
    print(f"   ❌ MyCobot测试失败: {e}")

# 测试3: 使用新版API (Mercury)
print("\n📡 测试3: pymycobot.Mercury (新API)")
try:
    from pymycobot import Mercury
    
    mc_new = Mercury('/dev/ttyAMA0')
    time.sleep(2)
    
    result = mc_new.get_angles()
    print(f"   get_angles() 返回: {result}")
    
    if result and result != -1:
        print("   ✅ 新版API成功！")
        print(f"   当前角度: {result}")
except Exception as e:
    print(f"   ⚠️  Mercury API不可用: {e}")

# 测试4: 检查Atom固件通信
print("\n📡 测试4: Atom通信检查")
try:
    from pymycobot.mycobot import MyCobot
    
    mc = MyCobot('/dev/ttyAMA0', 115200)
    time.sleep(1)
    
    # 尝试设置LED颜色来测试Atom响应
    print("   尝试设置Atom LED...")
    result = mc.set_color(255, 0, 0)  # 红色
    print(f"   set_color 返回: {result}")
    
    time.sleep(1)
    mc.set_color(0, 255, 0)  # 绿色
    time.sleep(1)
    mc.set_color(0, 0, 255)  # 蓝色
    time.sleep(1)
    mc.set_color(0, 0, 0)  # 关闭
    
except Exception as e:
    print(f"   ⚠️  Atom测试失败: {e}")

print("\n" + "=" * 70)
print("📊 诊断总结")
print("=" * 70)
print("\n建议:")
print("1. 如果串口通信正常但pymycobot返回-1")
print("   → 可能需要更新Atom固件")
print("2. 如果看到LED灯变色")
print("   → Atom通信正常，但角度读取有问题")
print("3. 如果完全无响应")
print("   → 检查串口连接或固件版本")
print("=" * 70)
