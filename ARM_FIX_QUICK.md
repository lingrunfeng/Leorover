# ⚡ 机械臂导航问题 - 快速修复参考

## 🔴 问题

机器人有导航路径但不动 → **机械臂碰撞地面**

## ✅ 解决方案

提高机械臂安装高度：`0.05m` → `0.15m`

## 🔧 修改步骤

**文件**: `Week-7-8-ROS2-Navigation/bme_ros2_navigation/urdf/macros.xacro`

**找到**: 第337行的`arm_mount_joint`

**修改**:
```xml
<origin xyz="0.0 0.0 0.15" rpy="0 0 0"/>
<!--              ↑
                 从0.05改为0.15
-->
```

**重新构建**:
```bash
cd /home/student26/Leorover
colcon build --packages-select bme_ros2_navigation --symlink-install
```

**重启Gazebo**:
```bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

## 📊 原因

- 机械臂安装太低（5cm）
- 碰撞地面，Gazebo物理引擎阻止移动
- 即使有速度命令，机器人也动不了

## ✅ 结果

- ✅ 机器人正常移动
- ✅ 导航功能正常
- ✅ 可以带机械臂导航

---

**详细文档**: `ARM_NAVIGATION_FIX.md`

