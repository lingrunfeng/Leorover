# 🚀 Leorover 完整启动玩法清单

> 包含所有启动方式：source环境、Gazebo、导航、探索、键盘控制等

---

## 📋 目录

1. [基础环境设置](#基础环境设置)
2. [Gazebo仿真启动](#gazebo仿真启动)
3. [导航功能启动](#导航功能启动)
4. [建图功能启动](#建图功能启动)
5. [探索功能启动](#探索功能启动)
6. [控制方式](#控制方式)
7. [实用工具](#实用工具)
8. [完整玩法组合](#完整玩法组合)

---

## 1️⃣ 基础环境设置

### 1.1 Source环境（每次都需要）

```bash
# 进入工作空间
cd /home/student26/Leorover

# Source ROS2系统环境
source /opt/ros/jazzy/setup.bash

# Source工作空间
source install/setup.bash
```

### 1.2 一键Source脚本（推荐）

创建快捷脚本：

```bash
# 创建别名（添加到 ~/.bashrc）
echo "alias leosrc='cd /home/student26/Leorover && source /opt/ros/jazzy/setup.bash && source install/setup.bash'" >> ~/.bashrc
source ~/.bashrc

# 使用方法
leosrc
```

---

## 2️⃣ Gazebo仿真启动

### 2.1 基础启动（默认empty世界）

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

### 2.2 更换世界场景

```bash
# 使用home世界（室内场景）
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=home.sdf

# 使用empty世界（空场景）
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=empty.sdf
```

### 2.3 自定义机器人初始位置

```bash
# 设置初始位置和朝向
ros2 launch bme_ros2_navigation spawn_robot.launch.py \
    world:=home.sdf \
    x:=0.0 \
    y:=0.0 \
    yaw:=0.0

# 参数说明：
# x: X坐标（米）
# y: Y坐标（米）
# yaw: 朝向角度（弧度），0.0=向东，1.57=向北，3.14=向西，-1.57=向南
```

### 2.4 更换机器人模型

```bash
# 使用不同的URDF模型（如果有）
ros2 launch bme_ros2_navigation spawn_robot.launch.py model:=your_model.urdf.xacro
```

### 2.5 关闭RViz（仅启动Gazebo）

```bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py rviz:=false
```

---

## 3️⃣ 导航功能启动

### 3.1 边建图边导航（SLAM + Navigation）⭐推荐

**启动步骤**：

```bash
# 终端1: 启动Gazebo和机器人
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 等待Gazebo完全启动后，打开终端2
# 终端2: 启动SLAM和导航
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py
```

**使用说明**：
- 等待10-30秒让SLAM初始化（等map frame出现）
- 在RViz中使用 **"2D Goal Pose"** 设置导航目标
- 机器人会自动导航，同时建图
- 地图会实时更新

**关闭RViz**：
```bash
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py rviz:=false
```

**更换RViz配置**：
```bash
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py \
    rviz_config:=mapping.rviz
```

---

### 3.2 使用已有地图导航（Localization + Navigation）

**启动步骤**：

```bash
# 终端1: 启动Gazebo和机器人
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: 启动定位和导航（使用已有地图）
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation navigation.launch.py
```

**使用说明**：
1. **设置初始位姿**：在RViz中使用 **"2D Pose Estimate"** 工具
   - 点击地图上机器人实际位置
   - 拖动鼠标设置机器人朝向

2. **设置导航目标**：使用 **"2D Nav Goal"** 工具
   - 点击地图上目标位置
   - 机器人会自动规划路径并导航

**地图文件位置**：
```
/home/student26/Leorover/Week-7-8-ROS2-Navigation/bme_ros2_navigation/maps/
```

---

### 3.3 仅定位（Localization Only）

```bash
# 终端1: 启动Gazebo
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: 启动定位（不包含导航）
ros2 launch bme_ros2_navigation localization.launch.py
```

---

## 4️⃣ 建图功能启动

### 4.1 仅建图（SLAM Only，无导航）

```bash
# 终端1: 启动Gazebo
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: 启动SLAM建图
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation mapping.launch.py
```

**使用说明**：
- 用键盘控制机器人移动（见下方键盘控制部分）
- 观察RViz中的地图实时更新
- 建图完成后保存地图（见保存地图部分）

**关闭RViz**：
```bash
ros2 launch bme_ros2_navigation mapping.launch.py rviz:=false
```

---

### 4.2 使用SLAM Toolbox进行定位（已有地图）

```bash
# 终端1: 启动Gazebo
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: 使用SLAM Toolbox定位
ros2 launch bme_ros2_navigation localization_slam_toolbox.launch.py
```

---

## 5️⃣ 探索功能启动

### 5.1 自动探索 + SLAM + 导航 ⭐推荐

**完整自动探索系统**：

```bash
# 终端1: 启动Gazebo和机器人
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: 启动探索、SLAM和导航
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation navigation_slam_exploration.launch.py
```

**使用说明**：
- 机器人会自动探索未知区域
- 同时进行SLAM建图
- 可以手动设置导航目标覆盖自动探索

**禁用自动探索**：
```bash
ros2 launch bme_ros2_navigation navigation_slam_exploration.launch.py \
    enable_exploration:=false
```

---

## 6️⃣ 控制方式

### 6.1 键盘控制

```bash
# 确保已安装
sudo apt install ros-jazzy-teleop-twist-keyboard

# 启动键盘控制
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**键盘控制键位**：

```
移动控制：
   u    i    o        ← 左前  前进  右前
   j    k    l        ← 左转  停止  右转
   m    ,    .        ← 左后  后退  右后

速度调整：
   q/z : 增加/减少最大速度 10%
   w/x : 增加/减少线速度 10%
   e/c : 增加/减少角速度 10%
   k 或 空格 : 强制停止
```

---

### 6.2 RViz交互式控制

如果launch文件启动了interactive_marker_twist_server，可以在RViz中使用交互式标记控制机器人。

**在RViz中添加**：
- Add → Interactive Markers
- Topic: `/cmd_vel_marker_server/cmd_vel`

---

### 6.3 话题直接控制

```bash
# 发布速度命令（前进）
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

# 发布速度命令（转向）
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}"

# 停止
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

---

## 7️⃣ 实用工具

### 7.1 查看TF树

```bash
# 生成TF树PDF
ros2 run tf2_tools view_frames

# 查看TF树（实时）
ros2 run tf2_ros tf2_echo map base_link

# 查看所有TF
ros2 topic echo /tf --once
```

---

### 7.2 查看话题列表

```bash
# 列出所有话题
ros2 topic list

# 查看特定话题信息
ros2 topic info /cmd_vel
ros2 topic info /scan
ros2 topic info /odom

# 查看话题数据
ros2 topic echo /scan
ros2 topic echo /odom
ros2 topic echo /cmd_vel
```

---

### 7.3 查看节点列表

```bash
# 列出所有节点
ros2 node list

# 查看节点信息
ros2 node info /robot_state_publisher
```

---

### 7.4 保存地图

```bash
# 保存当前地图
ros2 run nav2_map_server map_saver_cli \
    -f ~/my_map \
    --ros-args -p save_map_timeout:=10000

# 或保存到指定位置
ros2 run nav2_map_server map_saver_cli \
    -f /home/student26/Leorover/Week-7-8-ROS2-Navigation/bme_ros2_navigation/maps/my_map
```

地图会保存为：
- `my_map.pgm` - 地图图像
- `my_map.yaml` - 地图元数据

---

### 7.5 测试机械臂整合

```bash
# 启动测试（只可视化，无Gazebo）
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation test_arm_integration.launch.py
```

---

### 7.6 检查URDF

```bash
# 启动URDF检查
ros2 launch bme_ros2_navigation check_urdf.launch.py
```

---

## 8️⃣ 完整玩法组合

### 🎮 玩法1：手动建图

```bash
# 终端1: Gazebo
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=home.sdf

# 终端2: 建图
ros2 launch bme_ros2_navigation mapping.launch.py

# 终端3: 键盘控制
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 手动移动机器人建图，完成后保存地图
```

---

### 🎮 玩法2：自动探索建图

```bash
# 终端1: Gazebo
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=home.sdf

# 终端2: 自动探索+SLAM+导航
ros2 launch bme_ros2_navigation navigation_slam_exploration.launch.py

# 机器人会自动探索并建图，你也可以手动设置导航目标
```

---

### 🎮 玩法3：使用已有地图导航

```bash
# 终端1: Gazebo（确保地图对应的世界场景）
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=home.sdf

# 终端2: 定位和导航
ros2 launch bme_ros2_navigation navigation.launch.py

# 在RViz中设置初始位姿，然后设置导航目标
```

---

### 🎮 玩法4：边导航边建图

```bash
# 终端1: Gazebo
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=home.sdf

# 终端2: SLAM+导航
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py

# 在RViz中设置导航目标，机器人导航的同时建图
```

---

### 🎮 玩法5：纯键盘控制

```bash
# 终端1: Gazebo
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=home.sdf

# 终端2: 键盘控制
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 纯手动控制，适合测试机器人基本功能
```

---

### 🎮 玩法6：测试机械臂模型

```bash
# 终端1: Gazebo（带机械臂）
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: 测试URDF
ros2 launch bme_ros2_navigation test_arm_integration.launch.py

# 可以看到机械臂模型，用Joint State Publisher GUI控制关节
```

---

## 📊 快速参考表格

| 功能 | Launch文件 | 是否需要Gazebo | 说明 |
|------|-----------|---------------|------|
| **仅Gazebo** | `spawn_robot.launch.py` | 自己启动 | 只启动仿真环境 |
| **SLAM建图** | `mapping.launch.py` | ✓ | 仅建图，无导航 |
| **边导航边建图** | `navigation_with_slam.launch.py` | ✓ | 同时导航和建图 ⭐ |
| **已有地图导航** | `navigation.launch.py` | ✓ | 使用已有地图导航 ⭐ |
| **仅定位** | `localization.launch.py` | ✓ | 只做定位，无导航 |
| **自动探索** | `navigation_slam_exploration.launch.py` | ✓ | 自动探索+建图+导航 ⭐⭐ |
| **键盘控制** | `teleop_twist_keyboard` | ✓ | 手动控制移动 |
| **测试机械臂** | `test_arm_integration.launch.py` | ✗ | 仅可视化URDF |

---

## 🗺️ 可用世界场景

- `empty.sdf` - 空场景（默认）
- `home.sdf` - 室内场景

位置：`Week-7-8-ROS2-Navigation/bme_ros2_navigation/worlds/`

---

## 🎨 RViz配置文件

- `navigation.rviz` - 导航配置（默认）
- `mapping.rviz` - 建图配置
- `localization.rviz` - 定位配置
- `rviz.rviz` - 基础配置
- `urdf.rviz` - URDF查看配置

位置：`Week-7-8-ROS2-Navigation/bme_ros2_navigation/rviz/`

---

## ⚙️ 常用参数

### Gazebo参数

```bash
world:=empty.sdf|home.sdf        # 世界场景
x:=0.0                           # 初始X坐标
y:=0.0                           # 初始Y坐标
yaw:=0.0                         # 初始朝向（弧度）
rviz:=true|false                 # 是否启动RViz
```

### 导航参数

```bash
rviz:=true|false                 # 是否启动RViz
rviz_config:=navigation.rviz     # RViz配置文件
use_sim_time:=True|False         # 使用仿真时间
enable_exploration:=true|false   # 启用探索（仅探索launch）
```

---

## 🚨 常见问题

### Q: 如何选择玩法？

**A**: 
- 未知环境 → 玩法2（自动探索）或玩法1（手动建图）
- 已知环境 → 玩法3（已有地图导航）
- 需要同时导航和建图 → 玩法4（边导航边建图）
- 测试机器人 → 玩法5（纯键盘控制）

### Q: map frame不存在？

**A**: 
- 等待10-30秒让SLAM初始化
- 确保有激光扫描数据
- 在RViz中将Fixed Frame临时设为`odom`

### Q: 导航无法规划路径？

**A**:
- 确保已设置初始位姿（2D Pose Estimate）
- 检查目标点是否在自由空间
- 查看costmap是否正确更新

### Q: 键盘控制无响应？

**A**:
- 确保键盘控制终端处于活动状态
- 检查是否有其他节点在发布`/cmd_vel`
- 查看话题：`ros2 topic echo /cmd_vel`

---

## 📝 最佳实践

1. **启动顺序**：先启动Gazebo，再启动其他节点
2. **等待初始化**：SLAM和导航需要几秒钟初始化
3. **保存地图**：定期保存地图，避免丢失
4. **检查终端**：注意错误和警告信息
5. **使用RViz**：可视化有助于理解系统状态

---

## 🔧 一键启动脚本（可选）

创建便捷脚本 `start_nav.sh`:

```bash
#!/bin/bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# 玩法选择
case "$1" in
  slam)
    ros2 launch bme_ros2_navigation navigation_with_slam.launch.py
    ;;
  nav)
    ros2 launch bme_ros2_navigation navigation.launch.py
    ;;
  explore)
    ros2 launch bme_ros2_navigation navigation_slam_exploration.launch.py
    ;;
  map)
    ros2 launch bme_ros2_navigation mapping.launch.py
    ;;
  *)
    echo "用法: $0 {slam|nav|explore|map}"
    exit 1
    ;;
esac
```

使用：
```bash
chmod +x start_nav.sh
./start_nav.sh slam    # 启动SLAM导航
./start_nav.sh explore # 启动自动探索
```

---

## 📚 相关文档

- `QUICK_START.md` - 快速启动指南
- `LEOROVER_STARTUP_GUIDE.md` - 详细启动指南
- `ARM_INTEGRATION_GUIDE.md` - 机械臂整合文档

---

**祝使用愉快！🚀**

如有问题，检查：
- ROS2版本：`ros2 --version`
- 包是否正确安装：`ros2 pkg list | grep bme_ros2_navigation`
- 日志文件：`~/.ros/log/`

