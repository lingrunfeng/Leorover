# LeoRover MTC 顶抓功能测试指南

## 🎯 功能说明

系统可以接收目标物体坐标，自动规划并执行**垂直向下的顶抓**动作。

---

## 🚀 启动系统

### 终端 1：启动 MTC 抓取系统
```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch mycobot_mtc_pick_place_demo mtc_grasp_leorover.launch.py
```

**启动顺序**：
1. ⏱️ 0-10s: Gazebo + LeoRover + MyCobot 启动
2. ⏱️ 10-20s: MoveIt + RViz 启动  
3. ⏱️ 20-25s: MTC 节点启动

**成功标志**：
- Gazebo: 看到 LeoRover + 机械臂 + 夹爪
- RViz: 看到完整机器人模型
- 终端: `Waiting for object pose on /object_pose topic...`

---

## 📍 发送测试坐标

等待系统完全启动后（约25秒），在**新终端 2**中测试：

### 方法1：使用预设位置（推荐）

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# 测试1: 近距离位置（最容易成功）
ros2 run mycobot_mtc_pick_place_demo send_object_pose.py --preset near

# 测试2: 前方位置
ros2 run mycobot_mtc_pick_place_demo send_object_pose.py --preset front

# 测试3: 较高位置
ros2 run mycobot_mtc_pick_place_demo send_object_pose.py --preset front_high
```

### 方法2：使用ros2 topic pub（原始方式）

```bash
# 测试 A: 中等高度物体 (z=0.05)
ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'base_link'},
  pose: {
    position: {x: 0.15, y: 0.0, z: 0.05},
    orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
  }
}"

# 测试 B: 较高位置物体 (z=0.1)
ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'base_link'},
  pose: {
    position: {x: 0.15, y: 0.0, z: 0.1},
    orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
  }
}"

# 测试 C: 左侧位置
ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'base_link'},
  pose: {
    position: {x: 0.1, y: 0.1, z: 0.05},
    orientation: {w: 1.0}
  }
}"
```

### 方法3：自定义坐标

```bash
ros2 run mycobot_mtc_pick_place_demo send_object_pose.py --x 0.15 --y 0.0 --z 0.08
```

---

## ✅ 预期行为

### 在终端中观察：
```
[mtc_grasp_pose_node]: Received object pose: [0.15, 0.0, 0.05]
[mtc_grasp_pose_node]: Added collision object...
[mtc_grasp_pose_node]: Task planning succeeded
[mtc_grasp_pose_node]: Executing Stage 1: Open Gripper
[mtc_grasp_pose_node]: Executing Stage 2: Move to Pick
...
[mtc_grasp_pose_node]: All stages executed successfully
[mtc_grasp_pose_node]: Grasp completed successfully
```

### 在RViz中观察：
- ✅ 可以看到MTC规划的完整轨迹
- ✅ Approach方向是**垂直向下**（沿世界坐标系-Z轴）
- ✅ 夹爪姿态始终朝下
- ✅ 轨迹包括：打开夹爪 → 移动到上方 → 向下approach → 闭合 → 向上lift

### 在Gazebo中观察：
- ✅ 机械臂从物体**正上方**接近
- ✅ 垂直向下移动到物体位置
- ✅ 夹爪闭合（虽然可能看起来有点松散）
- ✅ 向上抬起

---

## 🎮 可用预设位置

| 名称 | 坐标 (x, y, z) | 描述 |
|------|---------------|------|
| `near` | (0.12, 0.0, 0.10) | 靠近位置，最容易成功 |
| `front` | (0.20, 0.0, 0.05) | 前方地面位置 |
| `front_high` | (0.18, 0.0, 0.15) | 前方较高位置 |
| `left` | (0.15, 0.10, 0.08) | 左前方位置 |
| `right` | (0.15, -0.10, 0.08) | 右前方位置 |

查看所有预设：
```bash
ros2 run mycobot_mtc_pick_place_demo send_object_pose.py --list
```

---

## 📊 工作空间范围

**推荐坐标范围**（相对base_link）：
- **X轴**: 0.12 ~ 0.25 米（前方）
- **Y轴**: -0.15 ~ 0.15 米（左右）
- **Z轴**: 0.05 ~ 0.20 米（高度）

超出范围可能导致IK求解失败。

---

## 🔍 MTC抓取流程（10个Stages）

1. **Current State** - 获取当前机器人状态
2. **Open Gripper** - 打开夹爪到"open"姿态
3. **Move to Pick** - 移动到抓取准备区域
4. **Generate Grasp Pose** - 生成顶抓姿态（垂直向下）
5. **Compute IK** - 计算到达目标的逆运动学解
6. **Approach Object** - 沿-Z方向向下接近物体
7. **Allow Collision** - 允许夹爪与物体碰撞
8. **Close Gripper** - 闭合夹爪到"half_closed"
9. **Attach Object** - 将物体附着到夹爪
10. **Lift Object** - 向上抬起物体

---

## 🛠️ 故障排除

### 问题1：IK求解失败
**症状**：`Task planning failed`
**原因**：目标超出机械臂可达范围
**解决**：
```bash
# 使用更容易到达的预设
ros2 run mycobot_mtc_pick_place_demo send_object_pose.py --preset near
```

### 问题2：No message received
**症状**：发送坐标后没有反应
**检查**：
```bash
# 检查MTC节点是否running
ros2 node list | grep mtc

# 检查话题是否存在
ros2 topic list | grep object_pose

# 检查控制器状态
ros2 control list_controllers
```

### 问题3：规划成功但执行失败
**症状**：Planning succeeded但Execute failed
**原因**：Controllers未正确连接
**解决**：重启系统，确保controllers全部active

### 问题4：夹爪看起来松散
**说明**：这是Gazebo对mimic joints的已知限制
**影响**：不影响MTC规划和执行，只是视觉效果
**可接受**：功能正常即可

---

## 📸 成功标准

- ✅ 系统启动无错误
- ✅ 至少2个预设位置测试成功
- ✅ RViz中轨迹为垂直向下
- ✅ Gazebo中机械臂执行完整动作
- ✅ 夹爪姿态始终朝下

---

## 🎓 对比：顶抓 vs 侧抓

| 特性 | 侧抓 | 顶抓（当前） |
|------|------|------------|
| Approach方向 | 沿gripper_frame | 沿世界坐标系-Z |
| Orientation | 多角度尝试 | 固定垂直向下 |
| 适用场景 | 侧面可达 | 平面物体，上方可达 |
| 实现方式 | GenerateGraspPose | GeneratePose (fixed) |

---

## 📝 测试记录模板

```
测试日期：____/____/____
测试人：________________

[ ] 测试1: near预设 - 成功/失败
[ ] 测试2: front预设 - 成功/失败  
[ ] 测试3: front_high预设 - 成功/失败
[ ] 测试4: 自定义坐标(x,y,z) - 成功/失败

观察结果：
- RViz中轨迹方向：____________________
- Gazebo中执行情况：___________________
- 特殊问题记录：______________________

总体评价：⭐⭐⭐⭐⭐
```

---

**祝测试顺利！🎉**
