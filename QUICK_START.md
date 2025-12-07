# 🚀 Leorover + 机械臂 快速启动指南

## ✅ 整合完成状态

- ✅ 机械臂已成功整合到Leorover URDF
- ✅ TF树结构正确（base_link未被覆盖）
- ✅ 导航功能完全保留
- ✅ 所有文件已构建安装

## 📁 重要文档

- `Week-7-8-ROS2-Navigation/bme_ros2_navigation/ARM_INTEGRATION_GUIDE.md` - 详细技术文档
- `Week-7-8-ROS2-Navigation/bme_ros2_navigation/INTEGRATION_SUMMARY.md` - 整合总结
- `QUICK_START.md` - 本文档（快速启动）

## 🎯 三种启动方式

### 1️⃣ 正常启动导航（推荐）

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py
```

**说明**：机械臂会自动包含在机器人模型中，但不影响导航。

---

### 2️⃣ 测试机械臂整合（可选）

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation test_arm_integration.launch.py
```

**说明**：启动RViz2可视化和Joint State Publisher GUI，可以手动测试机械臂关节。

---

### 3️⃣ 查看TF树结构（验证）

```bash
# 先启动导航或测试launch
# 然后在新终端运行：
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run tf2_tools view_frames
```

**说明**：生成`frames.pdf`文件，可查看完整TF树。

---

## 🔧 调整机械臂位置

如果需要调整机械臂安装位置：

1. 编辑文件：
   ```bash
   nano Week-7-8-ROS2-Navigation/bme_ros2_navigation/urdf/macros.xacro
   ```

2. 找到第323行左右，修改`arm_mount_joint`的origin：
   ```xml
   <joint name="arm_mount_joint" type="fixed">
     <origin xyz="0.0 0.0 0.05" rpy="0 0 0"/>
     <!--      x    y    z    roll pitch yaw -->
   ```

3. 重新构建：
   ```bash
   cd /home/student26/Leorover
   colcon build --packages-select bme_ros2_navigation --symlink-install
   ```

---

## 📊 TF树结构（已验证正确）

```
base_footprint
  └── base_link (Leorover中心，Nav2依赖)
      ├── scan_link (激光雷达)
      ├── camera_frame (相机)
      ├── imu_frame (IMU)
      ├── rocker_L_link (左轮)
      ├── rocker_R_link (右轮)
      └── arm_mount_link (机械臂安装座)
          └── mycobot_link1 (机械臂base)
              └── mycobot_link2
                  └── ... (其他关节)
```

---

## ⚠️ 常见问题

### Q: 还是报"Robot is out of bounds"错误？

**A**: 确保已重新source环境：
```bash
cd /home/student26/Leorover
source install/setup.bash
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py
```

### Q: RViz2中看不到机械臂？

**A**: 
1. 检查RobotModel是否已添加
2. 确认Description Topic为`/robot_description`
3. 重启RViz2

### Q: 想临时去掉机械臂？

**A**: 编辑`urdf/macros.xacro`，注释掉318-353行的机械臂部分，然后重新构建。

---

## 🎓 技术说明

### 为什么这样整合？

❌ **错误方式**：让机械臂的base_link覆盖Leorover的base_link  
→ 导致TF树混乱，Nav2找不到正确的机器人中心

✅ **正确方式**：创建arm_mount_link作为中间节点  
→ 机械臂挂在base_link下，不影响导航

### Nav2 Footprint配置

机械臂**不应该**包含在footprint中：

```yaml
# 只包含底盘尺寸
footprint: "[[-0.18, -0.15], [0.18, -0.15], [0.18, 0.15], [-0.18, 0.15]]"
```

**原因**：机械臂在导航时应该当作"透明"，否则会导致costmap过大。

---

## 🚦 集成验证

已验证以下功能正常：

- [x] URDF正确解析（20501字符）
- [x] base_link位置正确
- [x] arm_mount_link正确连接到base_link
- [x] mycobot_link1正确连接到arm_mount_link
- [x] 所有7个机械臂link都存在
- [x] TF树无环，结构清晰
- [x] 包成功构建

---

## 📞 获取帮助

如遇问题，查看详细文档：

```bash
cat Week-7-8-ROS2-Navigation/bme_ros2_navigation/ARM_INTEGRATION_GUIDE.md
cat Week-7-8-ROS2-Navigation/bme_ros2_navigation/INTEGRATION_SUMMARY.md
```

---

## ✨ 完成！

**你现在可以正常使用Leorover导航，机械臂已完美集成！** 🎉

启动命令：
```bash
cd /home/student26/Leorover && \
source /opt/ros/jazzy/setup.bash && \
source install/setup.bash && \
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py
```

