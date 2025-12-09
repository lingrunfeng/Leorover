# Leorover + MyCobot 机械臂整合指南

## ✅ 整合完成

机械臂已成功整合到Leorover URDF中，**不会破坏TF树结构和导航功能**。

## 📐 TF树结构

```
base_footprint
    └── base_link               ← Leorover 机器人中心（Nav2依赖）
        ├── rocker_L_link       ← 左侧摇臂
        │   ├── wheel_FL_link
        │   └── wheel_RL_link
        ├── rocker_R_link       ← 右侧摇臂  
        │   ├── wheel_FR_link
        │   └── wheel_RR_link
        ├── camera_frame        ← 相机
        ├── imu_frame           ← IMU
        ├── scan_link           ← 激光雷达
        └── arm_mount_link      ← **机械臂安装座（新增）**
            └── mycobot_link1   ← **机械臂base**
                └── mycobot_link2
                    └── mycobot_link3
                        └── mycobot_link4
                            └── mycobot_link5
                                └── mycobot_link6
                                    └── mycobot_link6_flange
```

## 🔧 关键修改

### 1. 添加的文件

- `urdf/mycobot/mycobot_280_arm.urdf.xacro` - 机械臂URDF定义
- `meshes/mycobot_280/visual/*.dae` - 机械臂可视化mesh文件

### 2. 修改的文件

- `urdf/macros.xacro` - 添加了arm_mount_link和机械臂集成

### 3. 安装位置

机械臂安装在base_link上方0.05米处：

```xml
<joint name="arm_mount_joint" type="fixed">
  <origin xyz="0.0 0.0 0.05" rpy="0 0 0"/>
  <parent link="base_link"/>
  <child link="arm_mount_link"/>
</joint>
```

**可以根据实际机械臂安装位置调整xyz参数。**

## 🚀 使用方法

### 启动导航（不影响）

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py
```

### 测试URDF（可选）

```bash
cd /home/student26/Leorover
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch bme_ros2_navigation test_arm_integration.launch.py
```

这会启动：
- Robot State Publisher
- Joint State Publisher GUI（可手动移动机械臂关节）
- RViz2（可视化机器人模型）

### 查看TF树

```bash
ros2 run tf2_tools view_frames
```

或在RViz2中添加TF显示。

## ⚠️ 重要说明

### 1. 导航footprint配置

**机械臂不应该影响导航footprint！**

在`nav2_params.yaml`中，确保footprint只包含底盘：

```yaml
global_costmap:
  global_costmap:
    ros__parameters:
      # 只包含底盘，不包含机械臂
      footprint: "[[-0.18, -0.15], [0.18, -0.15], [0.18, 0.15], [-0.18, 0.15]]"
      
local_costmap:
  local_costmap:
    ros__parameters:
      # 只包含底盘，不包含机械臂
      footprint: "[[-0.18, -0.15], [0.18, -0.15], [0.18, 0.15], [-0.18, 0.15]]"
```

### 2. 机械臂与导航解耦

- **导航时**：只需要Leorover的URDF，机械臂会自动包含但不影响导航
- **机械臂控制**：如果需要MoveIt，应该在独立的workspace中配置

### 3. base_link保持不变

✅ `base_link`位置没有改变  
✅ Nav2的robot frame仍然是`base_link`  
✅ 雷达、IMU、相机的坐标都没有改变  
✅ 不会再出现"Robot is out of bounds"错误

## 🧪 验证TF结构

运行验证脚本：

```bash
cd /home/student26/Leorover
python3 test_urdf.py
```

应该看到：

```
✅ URDF文件处理成功！
检查关键链接:
  ✓ base_link 存在
  ✓ base_footprint 存在
  ✓ scan_link 存在
  ✓ arm_mount_link 存在
  ✓ mycobot_link1 存在
  ✓ mycobot_link2 存在
  ✓ mycobot_link6 存在
```

## 📝 调整机械臂位置

如果需要调整机械臂安装位置，修改`urdf/macros.xacro`中的：

```xml
<joint name="arm_mount_joint" type="fixed">
  <origin xyz="0.0 0.0 0.05" rpy="0 0 0"/>
  <!--    ^^^^^^^^^^^^^^^^^^^
          x: 前后 (正=向前)
          y: 左右 (正=向左)
          z: 上下 (正=向上)
          
          rpy: roll pitch yaw 旋转角度
  -->
  <parent link="base_link"/>
  <child link="arm_mount_link"/>
</joint>
```

修改后重新构建：

```bash
cd /home/student26/Leorover
colcon build --packages-select bme_ros2_navigation --symlink-install
```

## 🎯 总结

✅ 机械臂已正确集成到Leorover  
✅ TF树结构正确，base_link保持不变  
✅ 导航功能不受影响  
✅ 可以独立控制导航和机械臂  
✅ 符合ROS2最佳实践  

**现在你可以安全地使用导航功能，同时在URDF中保留机械臂模型！**



