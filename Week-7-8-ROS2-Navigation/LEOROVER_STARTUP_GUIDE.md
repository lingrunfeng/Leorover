# LeoRover 启动指南

本指南说明如何启动 LeoRover 机器人的三种工作模式：
1. **边导航边建图**（SLAM + Navigation）
2. **自动导航**（使用已有地图）
3. **键盘操控**

---

## 准备工作

### 1. 安装依赖

确保已安装必要的 ROS2 包：

```bash
sudo apt install ros-jazzy-teleop-twist-keyboard
sudo apt install ros-jazzy-interactive-marker-twist-server
```

### 2. 编译工作空间

```bash
cd ~/aleorover
colcon build
source install/setup.bash
```

---

## 模式 1：边导航边建图（SLAM + Navigation）

此模式允许机器人在未知环境中同时进行建图和导航。

### 启动步骤

#### 终端 1：启动 Gazebo 和机器人

```bash
cd ~/aleorover
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

**等待 Gazebo 完全启动**，看到 LeoRover 机器人出现在场景中。

#### 终端 2：启动 SLAM 和导航（包含 RViz）

```bash
cd ~/aleorover
source install/setup.bash
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py
```

### 使用说明

1. **等待初始化**（10-30 秒）：
   - SLAM 需要接收激光扫描数据后才会发布 `map` frame
   - 在 RViz 中，等待 `map` frame 出现

2. **在 RViz 中操作**：
   - 使用 **"2D Goal Pose"** 工具点击地图上的位置
   - 机器人会自动导航到目标位置
   - 移动过程中会同时进行 SLAM 建图
   - 地图会实时更新

3. **RViz 显示内容**：
   - **LaserScan**：红色点表示激光扫描数据
   - **Map**：逐渐构建的地图（灰色=未知，白色=自由空间，黑色=障碍物）
   - **RobotModel**：LeoRover 机器人模型
   - **Global Costmap**：全局代价地图
   - **Local Costmap**：局部代价地图

### 可选参数

```bash
# 更换世界场景
ros2 launch bme_ros2_navigation spawn_robot.launch.py world:=home.sdf

# 调整机器人初始位置
ros2 launch bme_ros2_navigation spawn_robot.launch.py x:=0.0 y:=0.0 yaw:=0.0

# 关闭 RViz（如果不需要可视化）
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py rviz:=false
```

---

## 模式 2：自动导航（使用已有地图）

此模式使用预先构建的地图进行导航，适用于已知环境。

### 启动步骤

#### 终端 1：启动 Gazebo 和机器人

```bash
cd ~/aleorover
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

#### 终端 2：启动定位和导航（包含 RViz）

```bash
cd ~/aleorover
source install/setup.bash
ros2 launch bme_ros2_navigation navigation.launch.py
```

### 使用说明

1. **设置初始位姿**：
   - 在 RViz 中使用 **"2D Pose Estimate"** 工具
   - 点击地图上机器人实际所在的位置
   - 拖动鼠标设置机器人朝向

2. **设置导航目标**：
   - 使用 **"2D Nav Goal"** 工具
   - 点击地图上想要到达的位置
   - 机器人会自动规划路径并导航到目标

3. **路径规划**：
   - 机器人会显示全局路径（绿色线）
   - 局部路径会根据实时障碍物调整
   - 如果路径被阻挡，机器人会自动重新规划

### 地图文件位置

地图文件保存在：
```
~/aleorover/Week-7-8-ROS2-Navigation/bme_ros2_navigation/maps/
```

---

## 模式 3：键盘操控

此模式允许使用键盘直接控制机器人移动，适用于手动探索或测试。

### 启动步骤

#### 终端 1：启动 Gazebo 和机器人

```bash
cd ~/aleorover
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

#### 终端 2：启动键盘控制

```bash
cd ~/aleorover
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### 键盘控制说明

启动键盘控制后，终端会显示控制说明：

```
Reading from the keyboard and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
space key, k : force stop
anything else : stop smoothly

CTRL-C to quit
```

### 控制键位

- **移动控制**：
  - `i` - 前进
  - `,` - 后退
  - `j` - 左转
  - `l` - 右转
  - `u` - 左前
  - `o` - 右前
  - `m` - 左后
  - `.` - 右后
  - `k` 或 `空格` - 停止

- **速度调整**：
  - `q` - 增加最大速度 10%
  - `z` - 减少最大速度 10%
  - `w` - 增加线速度 10%
  - `x` - 减少线速度 10%
  - `e` - 增加角速度 10%
  - `c` - 减少角速度 10%

### 可选：同时启动 RViz 可视化

如果需要可视化，可以在第三个终端启动：

```bash
cd ~/aleorover
source install/setup.bash
ros2 launch bme_ros2_navigation spawn_robot.launch.py
# 然后在另一个终端
rviz2 -d $(ros2 pkg prefix bme_ros2_navigation)/share/bme_ros2_navigation/rviz/rviz.rviz
```

---

## 常见问题排查

### 1. 看不到机器人模型

**检查**：
```bash
# 检查话题
ros2 topic list | grep robot_description

# 检查 TF 树
ros2 run tf2_ros tf2_echo map base_link
```

**解决**：
- 确保已重新编译：`colcon build --packages-select bme_ros2_navigation`
- 在 RViz 中检查 RobotModel 的 "Robot Description" 是否为 `/robot_description`

### 2. 没有激光扫描数据

**检查**：
```bash
ros2 topic echo /scan --once
```

**解决**：
- 确保激光雷达已正确添加到 URDF
- 检查 Gazebo 中是否能看到激光扫描可视化

### 3. map frame 不存在

**原因**：SLAM 需要时间初始化

**解决**：
- 等待 10-30 秒
- 确保机器人有激光扫描数据
- 在 RViz 中临时将 Fixed Frame 设置为 `odom`，等 map 出现后再改回 `map`

### 4. 导航无法规划路径

**检查**：
```bash
# 检查 costmap
ros2 topic echo /global_costmap/costmap --once

# 检查地图
ros2 topic echo /map --once
```

**解决**：
- 确保已设置初始位姿（模式 2）
- 检查目标点是否在自由空间内
- 检查 costmap 是否正确更新

### 5. 键盘控制无响应

**检查**：
```bash
# 检查 cmd_vel 话题
ros2 topic echo /cmd_vel

# 检查话题连接
ros2 topic info /cmd_vel
```

**解决**：
- 确保键盘控制节点正在运行
- 检查终端是否处于活动状态（点击终端窗口）
- 确保没有其他节点在发布 cmd_vel

---

## 话题列表

### 主要话题

- `/cmd_vel` - 速度控制命令（geometry_msgs/msg/Twist）
- `/odom` - 里程计信息（nav_msgs/msg/Odometry）
- `/scan` - 激光扫描数据（sensor_msgs/msg/LaserScan）
- `/map` - 地图数据（nav_msgs/msg/OccupancyGrid）
- `/robot_description` - 机器人 URDF 描述
- `/tf` - TF 变换树

### TF 树结构

```
map
 └── odom
      └── base_footprint
           └── base_link
                ├── scan_link
                ├── camera_frame
                └── imu_frame
```

---

## 保存地图

在 SLAM 模式下，可以使用以下命令保存地图：

```bash
# 在运行 SLAM 的终端中按 Ctrl+C 停止
# 或者使用 map_saver（如果已安装）
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```

地图会保存为：
- `~/my_map.pgm` - 地图图像
- `~/my_map.yaml` - 地图元数据

---

## 快速参考

### 模式 1：边导航边建图
```bash
# 终端 1
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端 2
ros2 launch bme_ros2_navigation navigation_with_slam.launch.py
```

### 模式 2：自动导航
```bash
# 终端 1
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端 2
ros2 launch bme_ros2_navigation navigation.launch.py
```

### 模式 3：键盘操控
```bash
# 终端 1
ros2 launch bme_ros2_navigation spawn_robot.launch.py

# 终端 2
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---

## 提示

1. **启动顺序很重要**：先启动 Gazebo，再启动其他节点
2. **等待初始化**：SLAM 和导航需要几秒钟初始化
3. **检查终端输出**：注意错误和警告信息
4. **使用 RViz**：可视化有助于理解系统状态
5. **保存工作**：定期保存地图，避免丢失

---

## 联系与支持

如有问题，请检查：
- ROS2 版本：`ros2 --version`
- 包是否正确安装：`ros2 pkg list | grep bme_ros2_navigation`
- 日志文件：`~/.ros/log/`

---

**祝使用愉快！** 🚀

