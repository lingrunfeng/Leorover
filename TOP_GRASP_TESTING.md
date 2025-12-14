# 顶抓功能测试指南

## 测试目标

验证修改后的系统能够正确执行从上往下的顶抓，使用从 RViz 手动示教获取的固定姿态。

## 启动系统

### 终端 1：启动演示环境

```bash
cd ~/mycobot
source install/setup.bash
ros2 launch mycobot_mtc_pick_place_demo mtc_grasp_pose.launch.py
```

等待系统完全启动（大约 15 秒），确保看到：
- Gazebo 仿真窗口
- RViz 可视化界面
- 终端显示 "Waiting for object pose on /object_pose topic..."

## 测试用例

### 测试 1：中等高度物体 (z=0.05)

在新终端运行：

```bash
cd ~/mycobot
source install/setup.bash
ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'base_link'},
  pose: {
    position: {x: 0.15, y: 0.0, z: 0.05},
    orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
  }
}"
```

**预期结果**：
- ✅ 机械臂规划从上方垂直向下的轨迹
- ✅ Approach 方向垂直向下（沿世界坐标系 -Z 轴）
- ✅ 爪子朝向与 RViz 中示教的姿态一致
- ✅ 成功抓取物体并提起

---

### 测试 2：较高位置物体 (z=0.1)

```bash
ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'base_link'},
  pose: {
    position: {x: 0.15, y: 0.0, z: 0.1},
    orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
  }
}"
```

**预期结果**：
- ✅ 同样的顶抓姿态
- ✅ 在更高位置成功抓取

---

### 测试 3：地面物体 (z=0.0125，圆柱体半径)

```bash
ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'base_link'},
  pose: {
    position: {x: 0.15, y: 0.0, z: 0.0125},
    orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
  }
}"
```

**预期结果**：
- ✅ 能够到达接近地面的低位置
- ✅ 顶抓姿态保持一致
- ⚠️ 如果 IK 求解失败，可能是机械臂到达极限（这是正常的物理限制）

---

### 测试 4：不同 X-Y 位置

```bash
# 测试位置 A: 左侧
ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'base_link'},
  pose: {position: {x: 0.1, y: 0.1, z: 0.05}, orientation: {w: 1.0}}
}"

# 等待完成后测试位置 B: 右侧
ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'base_link'},
  pose: {position: {x: 0.1, y: -0.1, z: 0.05}, orientation: {w: 1.0}}
}"
```

**预期结果**：
- ✅ 在不同水平位置都使用相同的顶抓姿态
- ✅ Orientation 不随位置变化

---

## 检查点

在 RViz 中观察：

### 1. 轨迹可视化
- [ ] Approach 轨迹是垂直向下的（不是从侧面）
- [ ] 末端执行器姿态固定（爪子一直朝下）

### 2. Gazebo 仿真
- [ ] 机械臂从物体上方接近
- [ ] 爪子方向垂直向下
- [ ] 成功闭合抓取物体
- [ ] 成功提起物体

### 3. 终端输出
```
[mtc_grasp_pose_node]: Received object pose: [x, y, z]
[mtc_grasp_pose_node]: Added collision object...
[mtc_grasp_pose_node]: Task planning succeeded
[mtc_grasp_pose_node]: Executing Stage X
...
[mtc_grasp_pose_node]: All stages executed successfully
[mtc_grasp_pose_node]: Grasp completed successfully
```

---

## 故障排除

### 问题：IK 求解失败
**症状**：`Task planning failed`
**解决方案**：
1. 检查物体位置是否在机械臂可达范围内
2. 尝试调整物体 Z 坐标（增加高度）
3. 可能需要调整 `approach_object_max_dist` 参数

### 问题：姿态不是垂直向下
**症状**：机械臂从侧面接近
**检查**：
1. 确认代码已重新编译并 source 了新的环境
2. 检查参数是否正确传递到 node

### 问题：碰撞检测失败
**症状**：Planning 中显示碰撞
**解决方案**：
1. 调整 `grasp_frame_transform` 的 Z 偏移
2. 检查物体高度设置

---

## 对比验证

### 之前（侧抓）vs 现在（顶抓）

| 特性 | 侧抓（之前） | 顶抓（现在） |
|------|------------|------------|
| Approach 方向 | 沿 gripper_frame Z 轴 | 沿世界坐标系 -Z 轴 |
| Orientation | 围绕物体生成多个角度 | 固定的手动示教姿态 |
| 适用场景 | 侧面可达的物体 | 上方可达的平面物体 |
| Grasp 生成方式 | GenerateGraspPose | GeneratePose (fixed) |

---

## 成功标准

- [x] 编译无错误
- [ ] 至少 2 个测试用例成功
- [ ] RViz 中轨迹为垂直向下
- [ ] Gazebo 中成功抓取物体
- [ ] 姿态与手动示教的一致

完成所有测试后，顶抓功能即验证成功！
