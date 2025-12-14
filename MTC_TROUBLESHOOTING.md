# MTC 抓取问题修复说明

## 🔴 当前问题

MTC无法成功规划抓取，原因是：
1. **arm_hold_pose.py 干扰** - 该节点会固定机械臂姿态，阻止MTC控制
2. **抓取高度偏移不足** - 需要在物体上方设置grasp点

## ✅ 临时解决方案

### 方案1：手动禁用 arm_hold_pose（推荐）

编辑 `/home/student26/Leorover/Week-7-8-ROS2-Navigation/bme_ros2_navigation/launch/spawn_robot.launch.py`

找到第275行：
```python
launchDescriptionObject.add_action(arm_hold_pose_node)
```

改为注释：
```python
# launchDescriptionObject.add_action(arm_hold_pose_node)  # Disabled for MTC
```

然后重新编译：
```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
colcon build --packages-select bme_ros2_navigation
```

### 方案2：测试时手动kill节点

启动后在新终端运行：
```bash
ros2 node list | grep arm_hold
ros2 lifecycle set /arm_hold_pose shutdown
# 或
pkill -f arm_hold_pose
```

## 🚀 测试MTC

禁用arm_hold_pose后：

```bash
# 终端1
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch mycobot_mtc_pick_place_demo mtc_grasp_leorover.launch.py
```

等待25秒后，在**终端2**：
```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# 测试简单位置
ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'base_link'},
  pose: {
    position: {x: 0.15, y: 0.0, z: 0.05},
    orientation: {w: 1.0}
  }
}"
```

## 📊 已优化的参数

```python
'approach_object_min_dist': 0.005,
'approach_object_max_dist': 0.20,
'grasp_frame_transform_z': 0.08,  # 在物体上方8cm设置grasp点
```

## 🎯 预期行为

禁用arm_hold_pose后，MTC应该能够：
1. ✅ 规划完整的抓取轨迹
2. ✅ 先移动到物体上方
3. ✅ 垂直向下approach
4. ✅ 闭合夹爪
5. ✅ 向上lift

## 🔄 恢复正常使用

如果不用MTC，想恢复arm_hold_pose：
1. 取消spawn_robot.launch.py中的注释
2. 重新编译bme_ros2_navigation

---

**注意**：这是临时方案。长期解决需要：
- 创建专门的MTC launch文件，不启动arm_hold_pose
- 或让arm_hold_pose检测MTC活动并自动禁用
