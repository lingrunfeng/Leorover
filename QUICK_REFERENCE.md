# ⚡ Leorover 快速参考卡片

> 一键复制粘贴的常用命令

---

## 🔥 最常用组合

### 1. 自动探索（最推荐）

```bash
# 终端1: Source + Gazebo
cd /home/student26/Leorover && source /opt/ros/jazzy/setup.bash && source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=home.sdf

# 终端2: Source + 自动探索
cd /home/student26/Leorover && source /opt/ros/jazzy/setup.bash && source install/setup.bash
ros2 launch bme_ros2_navigation navigation_slam_exploration.launch.py
```

---

### 2. 边导航边建图

```bash
# 终端1: Source + Gazebo
cd /home/student26/Leorover && source /opt/ros/jazzy/setup.bash && source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: Source + SLAM导航
cd /home/student26/Leorover && source /opt/ros/jazzy/setup.bash && source install/setup.bash
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py
```

---

### 3. 使用已有地图导航

```bash
# 终端1: Source + Gazebo
cd /home/student26/Leorover && source /opt/ros/jazzy/setup.bash && source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: Source + 导航
cd /home/student26/Leorover && source /opt/ros/jazzy/setup.bash && source install/setup.bash
ros2 launch bme_ros2_navigation navigation.launch.py
```

---

### 4. 键盘控制

```bash
# 终端1: Source + Gazebo
cd /home/student26/Leorover && source /opt/ros/jazzy/setup.bash && source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: Source + 键盘
cd /home/student26/Leorover && source /opt/ros/jazzy/setup.bash && source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---

## 📦 Source环境（每次必做）

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

或创建别名（一次设置，永久使用）：
```bash
echo "alias leosrc='cd /home/student26/Leorover && source /opt/ros/jazzy/setup.bash && source install/setup.bash'" >> ~/.bashrc
source ~/.bashrc
```

然后只需：`leosrc`

---

## 🎮 Launch命令速查

| 功能 | 命令 |
|------|------|
| **仅Gazebo** | `ros2 launch bme_ros2_navigation spawn_robot.launch.py` |
| **仅建图** | `ros2 launch bme_ros2_navigation mapping.launch.py` |
| **SLAM+导航** | `ros2 launch bme_ros2_navigation navigation_with_slam.launch.py` |
| **已有地图导航** | `ros2 launch bme_ros2_navigation navigation.launch.py` |
| **自动探索** | `ros2 launch bme_ros2_navigation navigation_slam_exploration.launch.py` |
| **键盘控制** | `ros2 run teleop_twist_keyboard teleop_twist_keyboard` |
| **测试机械臂** | `ros2 launch bme_ros2_navigation test_arm_integration.launch.py` |

---

## 🗺️ Gazebo世界场景

```bash
# 空场景（默认）
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=empty.sdf

# 室内场景
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=home.sdf
```

---

## 📍 自定义初始位置

```bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py \
    world:=home.sdf \
    x:=0.0 \
    y:=0.0 \
    yaw:=0.0
```

参数说明：
- `x`: X坐标（米）
- `y`: Y坐标（米）
- `yaw`: 朝向（弧度）0.0=东, 1.57=北, 3.14=西, -1.57=南

---

## 🛠️ 实用工具

### 查看TF树
```bash
ros2 run tf2_tools view_frames
```

### 查看话题
```bash
ros2 topic list                    # 列出所有话题
ros2 topic echo /scan             # 查看激光数据
ros2 topic echo /odom             # 查看里程计
ros2 topic info /cmd_vel          # 查看话题信息
```

### 保存地图
```bash
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```

### 发布速度命令
```bash
# 前进
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    "{linear: {x: 0.5}, angular: {z: 0.0}}"

# 转向
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    "{linear: {x: 0.0}, angular: {z: 0.5}}"

# 停止
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

---

## ⌨️ 键盘控制键位

```
移动：
   u    i    o        ← 左前  前进  右前
   j    k    l        ← 左转  停止  右转
   m    ,    .        ← 左后  后退  右后

速度：
   q/z : +/- 最大速度
   w/x : +/- 线速度
   e/c : +/- 角速度
   k 或 空格 : 停止
```

---

## 🔍 调试命令

```bash
# 检查节点
ros2 node list

# 检查TF
ros2 run tf2_ros tf2_echo map base_link

# 检查话题连接
ros2 topic info /cmd_vel
ros2 topic hz /scan

# 查看日志
ros2 topic echo /rosout
```

---

## 📚 完整文档

- **详细启动指南**: `STARTUP_PLAYBOOK.md`
- **快速启动**: `QUICK_START.md`
- **机械臂整合**: `Week-7-8-ROS2-Navigation/bme_ros2_navigation/ARM_INTEGRATION_GUIDE.md`

---

## 💡 快速提示

1. **启动顺序**：先Gazebo，后其他节点
2. **等待时间**：SLAM需要10-30秒初始化
3. **保存地图**：及时保存，避免丢失
4. **查看RViz**：可视化帮助理解系统状态

---

**快速复制使用！🚀**



