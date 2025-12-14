# 🤖 MoveIt2 MTC 坐标抓取完整指南

> LeoRover + MyCobot + MoveIt2 + MTC 完整抓取系统

---

## 📋 系统组成

- **LeoRover** - 移动底盘
- **MyCobot 280** - 6自由度机械臂 + Adaptive Gripper
- **MoveIt2** - 运动规划框架
- **MTC** (MoveIt Task Constructor) - 任务规划系统
- **Gazebo** - 物理仿真环境

---

## 🚀 快速启动

### 第一步：启动完整系统

打开终端1，启动 Gazebo + MoveIt + MTC：

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch mycobot_mtc_pick_place_demo mtc_grasp_leorover.launch.py
```

**系统启动顺序**：
1. ⏱️ 0s - Gazebo + LeoRover + MyCobot 启动
2. ⏱️ 10s - MoveIt Move Group启动
3. ⏱️ 10s - RViz可视化启动
4. ⏱️ 10s - MTC抓取节点启动

**预计启动时间**：15-20秒

**启动成功标志**：
- Gazebo窗口显示LeoRover + 机械臂 + 夹爪
- RViz窗口显示机器人模型
- 终端显示：`Waiting for object pose on /object_pose topic...`

---

### 第二步：发送目标坐标

等待系统完全启动后，打开新终端2，发送测试坐标：

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# 使用预设位置（推荐）
ros2 run mycobot_mtc_pick_place_demo send_object_pose.py --preset near
```

**可用预设位置**：

| 预设名称 | 描述 | 坐标 (m) |
|---------|------|---------|
| `near` | 靠近位置（最容易） | X=0.12, Y=0.0, Z=0.10 |
| `front` | 前方地面位置 | X=0.20, Y=0.0, Z=0.05 |
| `front_high` | 前方较高位置 | X=0.18, Y=0.0, Z=0.15 |
| `left` | 左前方位置 | X=0.15, Y=0.10, Z=0.08 |
| `right` | 右前方位置 | X=0.15, Y=-0.10, Z=0.08 |

---

### 第三步：观察抓取执行

**在RViz中观察**：
- MTC规划的轨迹将显示为彩色路径
- 可以看到完整的抓取stages

**在Gazebo中观察**：
- 机械臂移动到目标上方
- 向下approach
- 夹爪闭合
- 抬起物体

---

## 📍 自定义坐标

### 发送自定义坐标

```bash
ros2 run mycobot_mtc_pick_place_demo send_object_pose.py --x 0.15 --y 0.05 --z 0.12
```

### 查看所有预设

```bash
ros2 run mycobot_mtc_pick_place_demo send_object_pose.py --list
```

### 工作空间范围

**推荐范围**（相对base_link）：
- **X**: 0.12 ~ 0.25 米（前方）
- **Y**: -0.15 ~ 0.15 米（左右）
- **Z**: 0.05 ~ 0.20 米（高度）

**坐标系说明**：
- 原点：`base_link`（小车中心）
- X轴：向前
- Y轴：向左
- Z轴：向上

---

## 🔧 Launch 参数

### 可选参数

```bash
ros2 launch mycobot_mtc_pick_place_demo mtc_grasp_leorover.launch.py \
    world:=home.sdf \
    use_sim_time:=true
```

**参数说明**：
- `world`: Gazebo世界文件（默认：`empty.sdf`）
- `use_sim_time`: 使用仿真时间（默认：`true`）

---

## 🎯 MTC 抓取流程

### 完整的抓取Stages

```
1. Current State          - 获取当前状态
2. Open Gripper          - 打开夹爪
3. Move to Pick          - 移动到抓取区域
4. Generate Grasp Pose   - 生成顶抓姿态
5. Compute IK            - 计算逆运动学
6. Approach Object       - 向下靠近物体
7. Allow Collision       - 允许夹爪-物体碰撞
8. Close Gripper         - 闭合夹爪
9. Attach Object         - 附着物体
10. Lift Object          - 抬起物体
```

### 顶抓配置

系统配置为**垂直向下抓取**：
- 夹爪方向：Z轴向下
- Approach方向：世界坐标系-Z方向
- 适合抓取地面或桌面物体

---

## 📊 系统架构

```
┌─────────────────────┐
│ send_object_pose.py │ ──▶ /object_pose
└─────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────┐
│ mtc_grasp_pose_node                   │
│ - 订阅物体坐标                         │
│ - 添加碰撞物体到场景                   │
│ - MTC任务规划（10 stages）             │
│ - MoveGroupInterface执行               │
└──────────────────────────────────────┘
                            │
                            ↓
              ┌─────────────┴─────────────┐
              │                           │
              ↓                           ↓
    ┌──────────────────┐      ┌──────────────────┐
    │ arm_controller    │      │ gripper_action   │
    │                   │      │ _controller      │
    └──────────────────┘      └──────────────────┘
              │                           │
              └─────────────┬─────────────┘
                            ↓
                    Gazebo Simulation
```

---

## 🛠️ 常见问题

### Q1: MTC规划失败？

**A**: 检查以下几点：
1. 目标坐标是否在工作空间内？
   ```bash
   # 使用near预设测试（最容易到达）
   ros2 run mycobot_mtc_pick_place_demo send_object_pose.py --preset near
   ```

2. 查看MTC节点日志：
   ```bash
   ros2 topic echo /rosout | grep mtc_grasp_pose
   ```

3. 在RViz中检查：
   - 机器人当前姿态
   - Planning Scene中的碰撞物体

### Q2: 夹爪不动作？

**A**: 检查控制器状态：
```bash
ros2 control list_controllers
```
应该看到：
- `gripper_action_controller` (active)
- `arm_controller` (active)

### Q3: Gazebo卡顿？

**A**: 降低仿真复杂度：
- 使用`empty.sdf`世界
- 关闭RViz中不必要的显示

### Q4: 如何调试IK失败？

**A**: 
1. 降低目标高度（Z值）
2. 靠近base_link（减小X, Y）
3. 查看RViz中的IK解

---

## 🎨 RViz 可视化

### 重要显示面板

- **MotionPlanning** - MTC任务可视化
- **PlanningScene** - 碰撞物体显示
- **TF** - 坐标系变换树
- **RobotModel** - 机器人模型

### MTC Task显示

在RViz中可以看到：
- ✅ 成功的stages（绿色）
- ❌ 失败的stages（红色）
- 📊 每个stage的代价

---

## 📝 技术参数

### MTC节点参数

```yaml
execute: true
object_type: "cylinder"
object_dimensions: [0.1, 0.0125]  # [height, radius]

arm_group_name: "arm"
gripper_group_name: "gripper"
gripper_frame: "mycobot_link6_flange"
gripper_open_pose: "open"
gripper_close_pose: "half_closed"

approach_object_min_dist: 0.001
approach_object_max_dist: 0.15
lift_object_min_dist: 0.005
lift_object_max_dist: 0.15

top_grasp_orientation: [1.0, 0.0, 0.0, 0.0]  # 向下
```

### 物体类型

当前支持：
- **Cylinder** (圆柱体) - 默认
- **Box** (长方体)

修改物体尺寸：
- 编辑 `mtc_grasp_leorover.launch.py`
- 修改 `object_dimensions` 参数

---

## 🚦 下一步开发

- [ ] 添加Place stage（放置物体）
- [ ] 集成视觉系统（YOLO物体检测）
- [ ] 支持多种抓取姿态
- [ ] 添加碰撞检测优化
- [ ] 集成导航系统（移动到抓取位置）

---

## 📚 参考文档

- [MoveIt2 文档](https://moveit.ros.org/)
- [MTC Tutorial](https://moveit.picknik.ai/main/doc/tutorials/pick_and_place_with_moveit_task_constructor/pick_and_place_with_moveit_task_constructor.html)
- [MyCobot 280 文档](https://docs.elephantrobotics.com/docs/mycobot-280-pi-2023en/)

---

**祝测试顺利！🎉**
