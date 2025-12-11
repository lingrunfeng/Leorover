#!/usr/bin/env python3
"""
真实机器坐标抓取测试
基于仿真测试数据：DOWNWARD_REACH_TEST.md
"""
from pymycobot.mycobot import MyCobot
import time

def test_coordinate_grasp():
    print("=" * 70)
    print("📐 MyCobot 坐标抓取测试（真实机器）")
    print("=" * 70)
    
    # 连接机械臂
    mc = MyCobot('/dev/ttyAMA0', 1000000)
    time.sleep(2)
    
    # 读取当前位置
    print("\n📍 当前状态：")
    current_angles = mc.get_angles()
    current_coords = mc.get_coords()
    print(f"   关节角度: {current_angles}")
    print(f"   末端坐标: {current_coords}")
    
    # 测试序列（保守的测试点，避免IK失败）
    test_cases = [
        {"name": "基准测试", "x": 150, "y": 0, "z": 120, "desc": "前方15cm，高度12cm"},
        {"name": "向前20cm", "x": 200, "y": 0, "z": 100, "desc": "前方20cm"},
        {"name": "向前更远", "x": 220, "y": 0, "z": 80, "desc": "前方22cm，降低高度"},
        {"name": "接近桌面", "x": 180, "y": 0, "z": 50, "desc": "前方18cm，Z=5cm"},
        {"name": "测试抓取", "x": 150, "y": 0, "z": 80, "desc": "适合抓取的位置"},
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print("\n" + "=" * 70)
        print(f"📍 测试 {i}/{len(test_cases)}: {test['name']}")
        print(f"   目标坐标: X={test['x']}mm, Y={test['y']}mm, Z={test['z']}mm")
        print(f"   说明: {test['desc']}")
        print("=" * 70)
        
        ans = input("   执行此测试？(y/n/q退出): ")
        if ans.lower() == 'q':
            print("⏹️  用户终止测试")
            break
        elif ans.lower() != 'y':
            print("⏭️  跳过此测试")
            results.append({**test, "status": "跳过"})
            continue
        
        try:
            # 设置垂直向下的姿态用于top-down grasp
            # rx=-180: gripper垂直向下
            # ry=0, rz=0: 无额外旋转
            target_coords = [test['x'], test['y'], test['z'], 
                           -180, 0, 0]
            
            print(f"   ⏳ 移动到目标位置...")
            result = mc.send_coords(target_coords, 30, 0)  # 速度30，模式0
            print(f"   send_coords 返回: {result}")
            
            if result == 1 or result:
                # 等待移动完成
                wait_time = 6
                for t in range(wait_time):
                    time.sleep(1)
                    print(f"   ⏳ {t+1}/{wait_time}秒...")
                
                # 检查最终位置
                final = mc.get_coords()
                if final:
                    print(f"\n   ✅ 移动完成")
                    print(f"   目标坐标: [{test['x']}, {test['y']}, {test['z']}]")
                    print(f"   实际坐标: [{final[0]:.1f}, {final[1]:.1f}, {final[2]:.1f}]")
                    
                    # 计算误差
                    error_x = abs(final[0] - test['x'])
                    error_y = abs(final[1] - test['y'])
                    error_z = abs(final[2] - test['z'])
                    
                    if error_x < 20 and error_y < 20 and error_z < 20:
                        print(f"   ✅ 误差小于20mm！")
                        status = "成功"
                        
                        # 测试gripper开合动作
                        print(f"\n   🤖 测试gripper动作...")
                        print(f"   📂 打开gripper...")
                        mc.set_gripper_value(100, 30)  # 打开到100%，速度30
                        time.sleep(2)
                        
                        print(f"   📁 关闭gripper...")
                        mc.set_gripper_value(0, 30)  # 关闭到0%，速度30
                        time.sleep(2)
                        
                        print(f"   📂 再次打开gripper...")
                        mc.set_gripper_value(100, 30)
                        time.sleep(2)
                        print(f"   ✅ Gripper动作完成！")
                    else:
                        print(f"   ⚠️  误差: X={error_x:.1f}, Y={error_y:.1f}, Z={error_z:.1f}mm")
                        status = "成功但有误差"
                    
                    results.append({**test, "status": status, 
                                  "final": [final[0], final[1], final[2]]})
                else:
                    print("   ⚠️  无法读取最终坐标")
                    results.append({**test, "status": "完成但无法验证"})
            else:
                print(f"   ❌ 发送命令失败")
                results.append({**test, "status": "命令失败"})
                
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            results.append({**test, "status": f"异常: {e}"})
        
        # 每次测试后返回HOME
        print("\n   🏠 返回HOME位置...")
        mc.send_angles([0, 0, 0, 0, 0, 0], 30)
        time.sleep(6)
    
    # 打印测试结果汇总
    print("\n\n" + "=" * 70)
    print("📊 测试结果汇总")
    print("=" * 70)
    print(f"\n{'序号':<4} {'测试名称':<12} {'X(mm)':<8} {'Z(mm)':<8} {'状态':<20}")
    print("-" * 70)
    for i, result in enumerate(results, 1):
        print(f"{i:<4} {result['name']:<12} {result['x']:<8} {result['z']:<8} {result['status']:<20}")
    
    print("\n" + "=" * 70)
    print("🎉 坐标抓取测试完成！")
    
    success_count = sum(1 for r in results if r['status'].startswith('成功'))
    print(f"\n✅ 成功: {success_count}/{len(results)}")
    print(f"📝 真实机器的工作空间已测试")
    print("=" * 70)

if __name__ == '__main__':
    test_coordinate_grasp()
