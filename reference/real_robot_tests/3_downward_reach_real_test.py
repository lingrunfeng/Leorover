#!/usr/bin/env python3
"""
第三步：向下抓取极限测试（真实机器版）
目的：测试你在仿真中验证的向下抓取能力
参考：DOWNWARD_REACH_TEST.md 中的测试数据

仿真成功数据：
- 最远：X=0.27m (27cm), Z=-0.08m (向下8cm)
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
    
    print("❌ 无法连接到机械臂！")
    sys.exit(1)

def downward_reach_test():
    print("=" * 70)
    print("📏 MyCobot 向下抓取极限测试 - 真实机器版")
    print("=" * 70)
    
    mc, port = find_robot()
    
    print("\n📋 测试说明：")
    print("   仿真测试结果：最远达到 X=270mm, Z=-80mm")
    print("   真实测试将从保守参数开始，逐步挑战极限")
    print("\n⚠️  重要安全提示：")
    print("   1. 机械臂底座固定牢固")
    print("   2. 下方没有障碍物")
    print("   3. 准备好急停")
    print("   4. 速度设置为安全的慢速\n")
    
    response = input("确认安全后，输入 'yes' 开始: ")
    if response.lower() != 'yes':
        print("❌ 测试已取消")
        sys.exit(0)
    
    # 测试序列（逐步挑战）
    test_cases = [
        {"name": "基线测试", "x": 150, "z": 0, "desc": "与底座同高"},
        {"name": "向下5cm", "x": 150, "z": -50, "desc": "轻微向下"},
        {"name": "向下8cm", "x": 150, "z": -80, "desc": "仿真成功的Z值"},
        {"name": "挑战：27cm远+5cm下", "x": 270, "z": -50, "desc": "距离挑战"},
        {"name": "挑战：27cm远+8cm下", "x": 270, "z": -80, "desc": "仿真极限值"},
    ]
    
    results = []
    
    # 先回到HOME
    print("\n🏠 移动到HOME位置...")
    mc.send_angles([0, 0, 0, 0, 0, 0], 20)
    time.sleep(6)
    
    for i, test in enumerate(test_cases, 1):
        print("\n" + "=" * 70)
        print(f"📍 测试 {i}/{len(test_cases)}: {test['name']}")
        print(f"   目标坐标: X={test['x']}mm, Y=0mm, Z={test['z']}mm")
        print(f"   说明: {test['desc']}")
        print("=" * 70)
        
        response = input(f"   执行此测试？(y/n/q退出): ")
        if response.lower() == 'q':
            print("⏹️  用户终止测试")
            break
        elif response.lower() != 'y':
            print("⏭️  跳过此测试")
            results.append({**test, "status": "⏭️ 跳过"})
            continue
        
        try:
            # 读取当前位置
            current = mc.get_coords()
            print(f"\n   当前位置: X={current[0]:.1f}, Y={current[1]:.1f}, Z={current[2]:.1f}")
            
            # 移动到目标位置
            # 注意：pymycobot的坐标系可能与仿真不同，需要调整
            # 这里假设坐标系一致，如果不对需要转换
            print(f"   ⏳ 移动到目标位置...")
            
            # 保持当前的姿态角度，只改变位置
            mc.send_coords([test['x'], 0, test['z'], current[3], current[4], current[5]], 15)
            
            # 等待移动完成（根据距离调整等待时间）
            wait_time = 8
            for t in range(wait_time):
                time.sleep(1)
                print(f"   ⏳ {t+1}/{wait_time}秒...")
            
            # 检查是否到达
            final = mc.get_coords()
            print(f"\n   最终位置: X={final[0]:.1f}, Y={final[1]:.1f}, Z={final[2]:.1f}")
            
            # 计算误差
            error_x = abs(final[0] - test['x'])
            error_z = abs(final[2] - test['z'])
            
            if error_x < 10 and error_z < 10:  # 误差小于10mm
                print(f"   ✅ 成功！误差: X={error_x:.1f}mm, Z={error_z:.1f}mm")
                status = "✅ 成功"
            else:
                print(f"   ⚠️  到达但有误差: X={error_x:.1f}mm, Z={error_z:.1f}mm")
                status = "⚠️ 有误差"
            
            results.append({**test, "status": status, "error_x": error_x, "error_z": error_z})
            
        except Exception as e:
            print(f"   ❌ 失败: {e}")
            results.append({**test, "status": f"❌ 失败: {e}"})
        
        # 每次测试后返回HOME
        print("\n   🏠 返回HOME...")
        mc.send_angles([0, 0, 0, 0, 0, 0], 20)
        time.sleep(6)
    
    # 打印测试结果汇总
    print("\n" + "=" * 70)
    print("📊 测试结果汇总")
    print("=" * 70)
    print(f"\n{'序号':<4} {'测试名称':<20} {'X(mm)':<8} {'Z(mm)':<8} {'状态':<15}")
    print("-" * 70)
    for i, result in enumerate(results, 1):
        print(f"{i:<4} {result['name']:<20} {result['x']:<8} {result['z']:<8} {result['status']:<15}")
    
    print("\n" + "=" * 70)
    print("🎉 向下抓取测试完成！")
    print("\n📝 结论：")
    success_count = sum(1 for r in results if r['status'].startswith('✅'))
    print(f"   - 成功: {success_count}/{len(results)}")
    print(f"   - 真实机器的向下抓取能力已测试")
    print(f"   - 可与仿真结果对比，调整参数")
    print("=" * 70)

if __name__ == '__main__':
    downward_reach_test()
