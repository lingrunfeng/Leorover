# 🤖 MyCobot 真实机器测试完整指南 - 方案A（直接控制）

> **离线文档** - 连上热点后可能没网，请提前阅读此文档

---

## 📱 方法1：手机热点连接（推荐，最稳定）

### **准备工作**
1. 手机开启热点
   - 热点名称：记下来（例如：`MyPhone`）
   - 密码：记下来
   - 频段：选择 **2.4GHz**（5GHz可能不稳定）

2. 记录信息：
   ```
   热点名称：_______________
   热点密码：_______________
   ```

---

### **连接步骤**

#### **步骤1：树莓派连接热点**

**物理连接**：
1. 给机械臂上电（12V电源 + 电源开关）
2. 等待60秒让树莓派启动
3. 用网线连接机械臂和电脑（临时用于配置WiFi）

**配置WiFi**：
```bash
# SSH连接树莓派（通过网线）
ssh elephant@10.3.14.59
# 密码：trunk

# 在树莓派上配置WiFi
sudo nmcli dev wifi connect "你的热点名称" password "你的热点密码"

# 检查获得的IP
ip addr show wlan0 | grep "inet "
# 记下IP地址，例如：192.168.43.123
```

#### **步骤2：电脑连接同一热点**

- 在电脑WiFi设置中连接到同一热点
- 等待连接成功

#### **步骤3：通过WiFi SSH连接**

```bash
# 断开网线，用新IP连接
ssh elephant@192.168.43.XXX  # 替换成树莓派的实际IP
# 密码：trunk
```

**成功！现在可以拔掉网线了！**

---

## 🧪 方案A：直接控制测试（简单快速）

### **核心原理**

```
你的电脑 (SSH) → 树莓派 → 串口(/dev/ttyAMA0) → 机械臂控制板
                     ↓
                pymycobot库
                     ↓
              直接发送坐标
```

**不需要**：ROS2、MoveIt、RViz
**需要**：SSH连接 + Python3 + pymycobot

---

## 📋 完整测试流程

### **测试1：基础连接测试**

SSH连接到树莓派后，运行：

```python
python3 << 'EOF'
from pymycobot.mycobot import MyCobot
import time

# 连接机械臂（波特率1000000很重要！）
mc = MyCobot('/dev/ttyAMA0', 1000000)
time.sleep(2)

# 读取当前角度
angles = mc.get_angles()
print(f"当前角度: {angles}")

# 读取当前坐标
coords = mc.get_coords()
print(f"当前坐标: {coords}")

if angles and angles != -1:
    print("✅ 连接成功！")
else:
    print("❌ 连接失败，检查：")
    print("1. 电源是否打开")
    print("2. 运行: sudo chmod 666 /dev/ttyAMA0")
EOF
```

**预期输出**：
```
当前角度: [0.12, -0.35, 0.26, ...]
当前坐标: [150.5, 0.2, 120.3, ...]
✅ 连接成功！
```

---

### **测试2：关节运动测试**

```python
python3 << 'EOF'
from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyAMA0', 1000000)
time.sleep(2)

print("🤖 关节运动测试")

# 移动到HOME
print("移动到HOME...")
mc.send_angles([0, 0, 0, 0, 0, 0], 30)
time.sleep(6)
print(f"位置: {mc.get_angles()}")

# 底座旋转
print("\n底座旋转30度...")
mc.send_angle(1, 30, 30)
time.sleep(4)

# 返回
print("返回HOME...")
mc.send_angles([0, 0, 0, 0, 0, 0], 30)
time.sleep(6)
print("✅ 测试完成")
EOF
```

---

### **测试3：坐标运动测试（重点！）**

这是你要的坐标抓取测试：

```python
python3 << 'EOF'
from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyAMA0', 1000000)
time.sleep(2)

print("📐 坐标运动测试")
print("=" * 60)

# 测试序列（逐步挑战）
tests = [
    {"x": 150, "y": 0, "z": 100, "desc": "安全基准位置"},
    {"x": 200, "y": 0, "z": 100, "desc": "向前20cm"},
    {"x": 150, "y": 0, "z": 0, "desc": "向下到底座高度"},
    {"x": 150, "y": 0, "z": -50, "desc": "向下5cm"},
    {"x": 270, "y": 0, "z": -80, "desc": "仿真极限值"},
]

for i, test in enumerate(tests, 1):
    print(f"\n测试{i}: {test['desc']}")
    print(f"目标: X={test['x']}, Y={test['y']}, Z={test['z']}")
    
    ans = input("执行？(y/n): ")
    if ans != 'y':
        continue
    
    # 获取当前姿态
    current = mc.get_coords()
    
    # 发送新坐标（保持姿态）
    target = [test['x'], test['y'], test['z'], 
              current[3], current[4], current[5]]
    
    result = mc.send_coords(target, 30, 0)
    print(f"send_coords返回: {result}")
    
    # 等待移动
    for t in range(6):
        time.sleep(1)
        print(f"  {t+1}/6秒...")
    
    # 检查到达位置
    final = mc.get_coords()
    print(f"目标: [{test['x']}, {test['y']}, {test['z']}]")
    print(f"实际: [{final[0]:.1f}, {final[1]:.1f}, {final[2]:.1f}]")
    
    # 返回HOME
    print("返回HOME...")
    mc.send_angles([0, 0, 0, 0, 0, 0], 30)
    time.sleep(6)

print("\n✅ 坐标测试完成！")
EOF
```

---

### **测试4：夹爪测试**

```python
python3 << 'EOF'
from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyAMA0', 1000000)
time.sleep(2)

print("🤏 夹爪测试")

# 打开
print("打开夹爪...")
mc.set_gripper_value(100, 50)
time.sleep(3)

# 关闭
print("关闭夹爪...")
mc.set_gripper_value(0, 50)
time.sleep(3)

print("✅ 夹爪测试完成")
EOF
```

---

## 📊 坐标系统说明

### **myCobot坐标系**（单位：mm）

```
        Z↑
         |
         |
    X ←--+
       /
      / Y
```

- **X轴**：向前为正（0-280mm可达）
- **Y轴**：向左为正（-150 to +150mm）
- **Z轴**：向上为正（可以为负值，向下延伸）

### **仿真vs真机对照**

| 位置 | 仿真坐标(m) | 真机坐标(mm) |
|------|------------|-------------|
| 基准 | X=0.15, Z=0.0 | X=150, Z=0 |
| 向下5cm | X=0.15, Z=-0.05 | X=150, Z=-50 |
| 极限 | X=0.27, Z=-0.08 | X=270, Z=-80 |

**转换公式**：`真机(mm) = 仿真(m) × 1000`

---

## ⚠️ 安全注意事项

### **移动前检查**
- [ ] 机械臂固定牢固
- [ ] 周围1米内无障碍物  
- [ ] 了解急停方法（关电源或Ctrl+C）
- [ ] 第一次速度设为30（中等速度）

### **危险区域避免**
- ❌ Z < -100mm（可能撞到桌面）
- ❌ X > 280mm（超出范围）
- ❌ 速度 > 80（太快不安全）

---

## 🆘 故障排查

### **问题1：angles返回-1**
```bash
# 解决：修复权限
sudo chmod 666 /dev/ttyAMA0

# 重启Python测试
```

### **问题2：机械臂不动但无报错**
- 检查伺服电机是否通电（手动移动有阻力=通电）
- 尝试更长等待时间（sleep增加到10秒）
- 检查send_coords返回值（应该是1）

### **问题3：WiFi连接断开**
```bash
# 重新连接WiFi
sudo nmcli dev wifi connect "热点名" password "密码"

# 查看IP
ip addr show wlan0
```

### **问题4：坐标到不了**
- 可能超出工作范围
- 尝试更保守的坐标
- 检查姿态角度是否合理

---

## 📝 测试记录表格

打印或抄写此表格记录测试结果：

| 测试 | X(mm) | Z(mm) | 成功？ | 备注 |
|------|-------|-------|--------|------|
| 基准 | 150 | 100 | □ | |
| 向前 | 200 | 100 | □ | |
| 同高 | 150 | 0 | □ | |
| 下5cm | 150 | -50 | □ | |
| 下8cm | 150 | -80 | □ | |
| 极限 | 270 | -80 | □ | |

---

## 🎯 下一步：集成MoveIt（可选）

测试完成后，如果想要：
- ✅ RViz可视化
- ✅ 路径规划
- ✅ 避障功能

需要配置MoveIt硬件接口，那是**方案B**，更复杂但功能强大。

**建议**：先用方案A验证功能，确认没问题后再考虑方案B。

---

## ✅ 成功标准

完成以下测试即为成功：
- [x] 基础连接（读取角度/坐标）
- [x] 关节运动（能移动到HOME）
- [x] 坐标运动（至少到达X=150, Z=0）
- [x] 夹爪控制（能开合）
- [ ] 仿真极限（X=270, Z=-80）

**祝测试顺利！** 🚀
