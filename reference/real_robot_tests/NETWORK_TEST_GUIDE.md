# 🌐 网络连接测试指南

## ✅ 当前状态

- **网络连接**：成功 ✅
- **你的电脑IP**：10.3.14.100
- **树莓派IP**：10.3.14.59
- **Ping测试**：0%丢包

---

## 🚀 三种测试方式

### **方式1：直接在树莓派上运行（推荐新手）**

#### 第一步：SSH连接树莓派
```bash
cd ~/mycobot/real_robot_tests
bash connect_to_robot.sh
# 或者直接：ssh elephant@10.3.14.59
# 密码：trunk
```

#### 第二步：在树莓派上测试机械臂
```bash
# 在树莓派终端运行：
ros2 launch mycobot_280pi slider_control.launch.py
```

这会启动一个图形界面，可以用滑块控制每个关节！

---

### **方式2：从你的电脑远程控制（需要ROS2配置）**

#### 第一步：配置ROS2环境
确保你的`.bashrc`有这些配置：
```bash
export ROS_DOMAIN_ID=10  # 和树莓派一致
export ROS_LOCALHOST_ONLY=0
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
```

#### 第二步：重新加载配置
```bash
source ~/.bashrc
```

#### 第三步：测试ROS2通信
先在树莓派上启动节点：
```bash
# SSH到树莓派
ssh elephant@10.3.14.59
# 在树莓派上运行
ros2 launch mycobot_280pi slider_control.launch.py
```

然后在**你的电脑**上查看话题：
```bash
# 在你的电脑上
ros2 topic list
ros2 topic echo /joint_states
```

---

### **方式3：使用pymycobot通过网络控制**

如果树莓派上运行了pymycobot的服务端，你也可以从电脑控制。

但这需要在树莓派上额外配置，**暂时不推荐**。

---

## 🧪 推荐的测试流程

### **今天的第一次测试（安全保守）**

1. **SSH连接树莓派**：
   ```bash
   bash ~/mycobot/real_robot_tests/connect_to_robot.sh
   ```

2. **在树莓派上启动滑块控制**：
   ```bash
   ros2 launch mycobot_280pi slider_control.launch.py
   ```

3. **用滑块界面测试**：
   - ✅ 逐个关节轻微移动
   - ✅ 观察机械臂反应
   - ✅ 确认一切正常

4. **测试夹爪**（如果有夹爪接口）

---

### **验证完毕后的高级测试**

如果上面的基础测试OK，可以尝试：

1. **从你的电脑发送ROS2命令**

2. **运行你的抓取代码**（修改后在真机上）

3. **测试向下抓取极限**

---

## 🔄 两种工作模式对比

| 模式 | 在哪里运行代码 | 优点 | 缺点 |
|------|--------------|------|------|
| **树莓派模式** | 在树莓派上 | 简单，不需要配置 | 需要SSH，树莓派性能弱 |
| **电脑模式** | 在你的电脑上 | 电脑性能强，开发方便 | 需要配置ROS2网络 |

**建议**：
- 🟢 **今天第一次测试**：用树莓派模式（简单安全）
- 🟡 **以后开发**：配置好后用电脑模式（方便强大）

---

## 📝 快速命令参考

```bash
# 连接树莓派
bash ~/mycobot/real_robot_tests/connect_to_robot.sh

# 在树莓派上运行滑块控制
ros2 launch mycobot_280pi slider_control.launch.py

# 在你电脑上查看话题（需要先在树莓派启动节点）
ros2 topic list

# 测试网络连接
ping 10.3.14.59

# 重新配置网络（如果断开了）
bash ~/mycobot/real_robot_tests/setup_network_connection.sh
```

---

## 🆘 常见问题

### ❓ SSH连接超时
```bash
# 检查网络
ping 10.3.14.59

# 如果ping不通，重新配置网络
bash ~/mycobot/real_robot_tests/setup_network_connection.sh
```

### ❓ 在电脑上看不到ROS2话题
确认：
1. 树莓派上的节点已启动
2. ROS_DOMAIN_ID一致（都是10）
3. ROS_LOCALHOST_ONLY=0
4. 防火墙没有阻止

### ❓ 树莓派图形界面很卡
这是正常的，树莓派性能有限。可以用SSH的X11转发：
```bash
ssh -X elephant@10.3.14.59
```

---

## 🎯 下一步建议

**现在立即做：**
1. SSH连接树莓派
2. 启动slider_control测试
3. 确认机械臂能正常控制

**今天结束前：**
1. 测试所有6个关节
2. 测试夹爪（如果有）
3. 记录工作范围

**明天或以后：**
1. 配置ROS2网络（从电脑控制）
2. 集成你的抓取代码
3. 测试向下抓取极限

---

**祝测试顺利！** 🚀
