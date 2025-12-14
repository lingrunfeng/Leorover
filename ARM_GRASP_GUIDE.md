# 🤖 MyCobot 机械臂坐标抓取使用指南

> 快速启动和测试 MyCobot 机械臂的坐标抓取功能

---

## 📋 功能说明

本系统实现了基于坐标的机械臂控制功能（模拟 pymycobot 的 `send_coords()` 方法）：
- ✅ 发送目标坐标 (x, y, z)
- ✅ 自动计算逆运动学 (IK)
- ✅ 机械臂向下抓取姿态
- ✅ 在 Gazebo 仿真中可视化运动
- ⚠️ 当前版本：无夹爪，仅展示运动到目标位置

---

## 🚀 快速启动

### 方法一：一键启动完整演示（推荐）

```bash
# 启动完整系统（Gazebo + 控制器 + 坐标控制节点）
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation arm_grasp_demo.launch.py
```

**等待系统完全启动后（约10-15秒），打开新终端发送测试坐标：**

```bash
# 新终端
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# 使用预设位置
ros2 run bme_ros2_navigation send_grasp_target.py --preset front
```

---

### 方法二：分步启动（调试用）

如果需要分别控制各个组件：

```bash
# 终端1: 启动 Gazebo 和机器人
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: 启动坐标控制节点
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run bme_ros2_navigation arm_coordinate_controller.py

# 终端3: 发送目标坐标
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run bme_ros2_navigation send_grasp_target.py --preset front
```

---

## 📍 预设测试位置

系统提供了6个预设位置，覆盖机械臂的工作空间：

| 预设名称 | 描述 | 坐标 (米) |
|---------|------|----------|
| `front` | 前方中央位置 | X=0.25, Y=0.0, Z=0.15 |
| `left` | 左前方位置 | X=0.20, Y=0.15, Z=0.12 |
| `right` | 右前方位置 | X=0.20, Y=-0.15, Z=0.12 |
| `high` | 较高位置 | X=0.15, Y=0.0, Z=0.25 |
| `low` | 较低位置（接近地面） | X=0.20, Y=0.0, Z=0.05 |
| `far` | 较远位置（测试臂展） | X=0.30, Y=0.0, Z=0.10 |

### 使用预设位置

```bash
# 查看所有预设位置
ros2 run bme_ros2_navigation send_grasp_target.py --list

# 发送预设位置
ros2 run bme_ros2_navigation send_grasp_target.py --preset front
ros2 run bme_ros2_navigation send_grasp_target.py --preset left
ros2 run bme_ros2_navigation send_grasp_target.py --preset high
```

---

## 🎯 自定义坐标

你可以发送自定义坐标进行测试：

```bash
# 发送自定义坐标 (单位：米)
ros2 run bme_ros2_navigation send_grasp_target.py --x 0.25 --y 0.05 --z 0.05

# 指定参考坐标系（默认为 base_link）
ros2 run bme_ros2_navigation send_grasp_target.py --x 0.2 --y 0.0 --z 0.15 --frame base_link
```

**坐标系说明：**
- 原点：机器人 `base_link`（车体中心）
- X轴：向前为正
- Y轴：向左为正
- Z轴：向上为正

**工作空间参考：**
- X: 0.10 ~ 0.35 米（前方）
- Y: -0.20 ~ 0.20 米（左右）
- Z: 0.05 ~ 0.30 米（高度）

---

## 📊 观察机械臂运动

### 在 Gazebo 中观察
1. 启动后在 Gazebo 窗口中可以看到机械臂
2. 发送坐标后，机械臂会在约3秒内移动到目标位置
3. 观察末端姿态（应该向下，模拟抓取姿态）

### 在 RViz 中观察（可选）
如果启动时启用了 RViz：
1. 可以看到 TF 变换树
2. 查看机械臂各关节状态
3. 可视化目标坐标（如果添加了 marker）

---

## 🔧 Launch 参数说明

### arm_grasp_demo.launch.py 参数

```bash
# 基础用法
ros2 launch bme_ros2_navigation arm_grasp_demo.launch.py

# 自定义参数
ros2 launch bme_ros2_navigation arm_grasp_demo.launch.py \
    world:=home.sdf \
    rviz:=true \
    x:=0.0 y:=0.0 yaw:=0.0
```

**可用参数：**
- `world`: Gazebo世界场景（默认：`empty.sdf`，可选：`home.sdf`）
- `rviz`: 是否启动RViz（默认：`true`）
- `x`, `y`, `yaw`: 机器人初始位置和朝向
- 自动使用 `use_sim_time:=True`

---

## 🛠️ 话题和服务

### 关键话题

| 话题名称 | 类型 | 说明 |
|---------|------|------|
| `/target_object_pose` | `geometry_msgs/PoseStamped` | 目标坐标输入 |
| `/arm_controller/joint_trajectory` | `trajectory_msgs/JointTrajectory` | 关节轨迹指令 |
| `/joint_states` | `sensor_msgs/JointState` | 关节状态反馈 |
| `/arm_controller/follow_joint_trajectory` | Action | 轨迹跟踪 Action |

### 查看话题

```bash
# 查看目标坐标话题
ros2 topic echo /target_object_pose

# 查看关节状态
ros2 topic echo /joint_states

# 手动发送坐标（调试用）
ros2 topic pub --once /target_object_pose geometry_msgs/PoseStamped \
  "{header: {frame_id: 'base_link'}, pose: {position: {x: 0.25, y: 0.0, z: 0.15}}}"
```

---

## 🐛 常见问题

### Q1: 机械臂不动？
**A**: 检查以下几点：
1. 确认 `arm_coordinate_controller` 节点正在运行
   ```bash
   ros2 node list | grep arm_coordinate
   ```
2. 检查控制器是否激活
   ```bash
   ros2 control list_controllers
   ```
   应该看到 `arm_controller` 状态为 `active`
3. 查看节点日志
   ```bash
   ros2 node info /arm_coordinate_controller
   ```

### Q2: 提示"IK求解失败"？
**A**: 目标坐标超出工作空间
- 检查坐标是否在推荐范围内
- 尝试使用预设位置测试
- 查看节点日志了解具体原因

### Q3: 机械臂运动不平滑？
**A**: 
- 增加轨迹执行时间（修改 `arm_coordinate_controller.py` 中的 `duration_sec`）
- 检查 Gazebo 仿真性能

### Q4: 如何调试IK计算？
**A**: 查看日志输出
```bash
# 查看详细日志
ros2 run bme_ros2_navigation arm_coordinate_controller.py --ros-args --log-level debug
```

### Q5: 如何与导航功能结合？
**A**: 当前版本专注于机械臂控制。如需同时使用导航：
```bash
# 使用 spawn_robot.launch.py 同时启动导航和机械臂
# 然后单独启动坐标控制节点
```

---

## 📝 代码结构

```
bme_ros2_navigation/
├── scripts/
│   ├── arm_coordinate_controller.py  # 坐标控制节点（IK求解）
│   ├── send_grasp_target.py         # 测试脚本（发送坐标）
│   └── arm_hold_pose.py             # 保持姿态节点（导航时用）
├── launch/
│   ├── arm_grasp_demo.launch.py     # 抓取演示启动文件 ⭐
│   └── spawn_robot.launch.py        # 基础机器人启动
├── config/
│   └── mycobot_controllers.yaml     # ros2_control配置
└── urdf/
    └── mycobot/
        └── mycobot_280_arm.urdf.xacro  # 机械臂URDF
```

---

## 🎓 技术原理

1. **逆运动学 (IK)**：将目标坐标 (x, y, z) 转换为关节角度
   - 使用几何法简化计算
   - 假设向下抓取姿态
   - 检查工作空间可达性

2. **轨迹控制**：使用 ros2_control 框架
   - `JointTrajectoryController` 跟踪轨迹
   - `GazeboSimSystem` 仿真硬件接口
   - Action 接口提供异步执行和反馈

3. **坐标系**：基于 `base_link` 的机器人本体坐标系

---

## 🚦 下一步开发方向

- [ ] 添加夹爪支持（需要更新URDF）
- [ ] 改进IK求解器（使用 ikpy 或 MoveIt）
- [ ] 添加碰撞检测
- [ ] 与视觉系统（YOLO）集成
- [ ] 支持更复杂的抓取姿态

---

## 📚 相关文档

- `MIGRATION_GUIDE.md` - MoveIt2迁移指南
- `STARTUP_PLAYBOOK.md` - LeoRover启动指南
- `QUICK_START.md` - 快速开始

---

**祝测试顺利！🎉**

如有问题，请检查：
- Gazebo 是否完全启动
- 控制器状态：`ros2 control list_controllers`
- 节点运行状态：`ros2 node list`
- 话题连接：`ros2 topic list`
