# MyCobot机械臂控制说明

## 概述

已成功为LeoRover上的MyCobot 280机械臂添加ros2_control支持，提供两种工作模式：

1. **固定姿态模式 (导航测试)** - 默认启用
   - 机械臂保持向上折叠姿态
   - 避免干扰2D激光雷达扫描
   - 适用于SLAM和导航测试

2. **坐标控制模式 (抓取测试)** - 需要手动启用
   - 接收目标坐标指令
   - 使用简单IK计算关节角度
   - 模拟pymycobot的`send_coords()`功能
   - 适用于视觉抓取测试

## 快速开始

### 1. 导航测试模式 (默认)

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# 启动仿真 - 机械臂将自动保持向上姿态
ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

**预期效果：**
- Gazebo中机械臂向上折叠，不干扰前方雷达
- 机械臂保持固定姿态，不会因重力下垂
- 可以安全进行导航和SLAM测试

### 2. 抓取测试模式

**步骤：**

1. 编辑launch文件启用坐标控制器：
```bash
# 编辑 launch/spawn_robot.launch.py
# 找到这两行并按注释操作：
# 1. 注释掉: launchDescriptionObject.add_action(arm_hold_pose_node)
# 2. 取消注释: launchDescriptionObject.add_action(arm_coordinate_controller_node)
```

2. 重新构建并启动：
```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash  
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

3. 发送目标坐标：
```bash
# 发布目标位置让机械臂移动
ros2 topic pub -1 /target_object_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'base_link'},
  pose: {
    position: {x: 0.15, y: 0.0, z: 0.08},
    orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
  }
}"
```

## 与YOLO集成

将来集成YOLO视觉识别时：

```python
# 在你的YOLO节点中发布检测到的目标坐标
from geometry_msgs.msg import PoseStamped

pose_pub = self.create_publisher(PoseStamped, '/target_object_pose', 10)

# 检测到目标后发布
target_pose = PoseStamped()
target_pose.header.frame_id = 'base_link'
target_pose.pose.position.x = detected_x  # 基于相机转换到base_link坐标系
target_pose.pose.position.y = detected_y
target_pose.pose.position.z = detected_z
pose_pub.publish(target_pose)
```

机械臂将自动移动到目标位置。

## 验证控制器状态

```bash
# 检查控制器是否正常运行
ros2 control list_controllers

# 应该看到：
# joint_state_broadcaster[joint_state_broadcaster/JointStateBroadcaster] active
# arm_controller[joint_trajectory_controller/JointTrajectoryController] active

# 查看关节状态
ros2 topic echo /joint_states --once

# 查看机械臂控制话题
ros2 topic list | grep arm
```

## 真实机器人迁移

迁移到真实LeoRover+MyCobot时：

1. **导航部分**：直接部署，无需修改
2. **机械臂控制**：使用你现有的pymycobot代码
   - 仿真：`arm_coordinate_controller.py` (基于ros2_control)
   - 真实：`test_real_coordinate_grasp.py` (基于pymycobot)
3. **YOLO接口保持不变**：仍然发布到`/target_object_pose`

## 故障排除

### 问题1：机械臂未保持姿态
```bash
# 检查arm_hold_pose节点是否运行
ros2 node list | grep arm_hold

# 查看节点输出
ros2 node info /arm_hold_pose
```

### 问题2：控制器未启动
```bash
# 检查gazebo_ros2_control插件是否加载
ros2 topic list | grep controller

# 重新spawn控制器
ros2 run controller_manager spawner arm_controller
```

### 问题3：IK求解失败
- 确保目标坐标在机械臂工作空间内
- MyCobot 280的有效范围约为：
  - X: 50-280mm
  - Y: -200 to 200mm  
  - Z: -100 to 200mm (相对于base)

## 文件结构

```
bme_ros2_navigation/
├── urdf/
│   └── mycobot/
│       └── mycobot_280_arm.urdf.xacro  # ✨ 添加了ros2_control
├── config/
│   └── mycobot_controllers.yaml        # ✨ 新建：控制器配置
├── scripts/
│   ├── arm_hold_pose.py                # ✨ 新建：固定姿态节点
│   └── arm_coordinate_controller.py    # ✨ 新建：坐标控制节点
└── launch/
    └── spawn_robot.launch.py           # ✨ 修改：添加控制器启动
```

## 下一步

1. ✅ 当前：机械臂已配置ros2_control，可用于导航测试
2. 🔜 集成YOLO：添加目标检测发布`/target_object_pose`
3. 🔜 完整测试：导航到目标 + 机械臂抓取
4. 🔜 真实部署：使用pymycobot替换仿真控制器
