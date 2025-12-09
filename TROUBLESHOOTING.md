# 🔧 Leorover 故障排除指南

## ❌ 问题：启动Gazebo后看不到Leorover机器人

### 症状
- Gazebo启动了但是看不到Leorover模型
- robot_state_publisher节点没有运行
- `/robot_description`话题没有数据

### 原因
机械臂整合导致URDF加载失败（机械臂xacro调用方式有问题）

### ✅ 解决方案（已实施）

**机械臂已被临时禁用**，现在Leorover应该可以正常显示。

---

## 🚀 现在可以正常使用

### 重新启动Gazebo

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

**Leorover应该会正常出现在Gazebo中！**

---

## 🔄 如何重新启用机械臂（需要修复）

机械臂整合代码已被注释，位置在：
```
Week-7-8-ROS2-Navigation/bme_ros2_navigation/urdf/macros.xacro
第318-350行
```

### 要重新启用需要：

1. **检查机械臂URDF文件**
   ```bash
   cd /home/student26/Leorover/Week-7-8-ROS2-Navigation/bme_ros2_navigation/urdf/mycobot/
   cat mycobot_280_arm.urdf.xacro
   ```

2. **问题可能在于**：
   - 机械臂macro的参数传递不正确
   - base_link参数应该直接传link名称而非变量
   - mesh文件路径可能有问题

3. **修复建议**：
   创建一个简化的机械臂macro测试文件，验证可以正确生成URDF

---

## 📋 验证Leorover是否正常

### 1. 检查节点
```bash
ros2 node list
```

应该看到：
- `/robot_state_publisher`
- `/ekf_filter_node`
- `/mogi_trajectory_server`
- `/ros_gz_sim`
- 等等

### 2. 检查TF
```bash
ros2 run tf2_tools view_frames
```

应该生成TF树，包含：
- `base_footprint`
- `base_link`
- `scan_link`
- 车轮links

### 3. 检查话题
```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|robot_description"
```

应该看到：
- `/cmd_vel`
- `/odom`
- `/scan`
- `/robot_description`

### 4. 在Gazebo中查看
- 应该看到Leorover机器人模型
- 车轮应该可以转动
- 激光雷达应该在工作

---

## 🎮 现在可以开始玩了

### 边导航边建图
```bash
# 终端1: Gazebo（应该已经在运行）
# 如果没有运行：
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: 导航+SLAM
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py
```

### 自动探索
```bash
# 终端1: Gazebo
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: 探索
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation navigation_slam_exploration.launch.py
```

### 键盘控制
```bash
# 终端1: Gazebo
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端2: 键盘
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---

## 🔍 其他常见问题

### Q: Gazebo很慢/卡顿
**A**: 
- 关闭不必要的程序
- 降低Gazebo图形质量：Edit → View → Wireframe
- 使用empty世界而非home世界

### Q: 键盘控制无响应
**A**:
- 确保键盘控制终端是活动状态
- 点击终端窗口
- 检查是否有其他节点在发布`/cmd_vel`

### Q: map frame不存在
**A**:
- 等待10-30秒让SLAM初始化
- 在RViz中临时将Fixed Frame改为`odom`

### Q: 导航无法规划路径
**A**:
- 使用"2D Pose Estimate"设置初始位姿
- 确保目标点在自由空间
- 检查costmap是否更新

---

## 📝 机械臂问题记录

### 当前状态
- ❌ 机械臂整合失败（已禁用）
- ✅ Leorover基础功能正常

### 需要修复
1. 检查机械臂macro定义
2. 修正base_link参数传递
3. 验证mesh文件路径
4. 测试单独的机械臂URDF

### 修复后需要
1. 取消macros.xacro中的注释（318-350行）
2. 重新构建：`colcon build --packages-select bme_ros2_navigation`
3. 测试URDF：`xacro urdf/leo_sim.urdf.xacro | grep -c "mycobot"`
4. 重新启动Gazebo验证

---

## 📚 相关文档

- **启动玩法**: `STARTUP_PLAYBOOK.md`
- **快速参考**: `QUICK_REFERENCE.md`
- **快速启动**: `QUICK_START.md`

---

**现在Leorover应该可以正常工作了！** 🎉

如有其他问题，请检查上述验证步骤。



