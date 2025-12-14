# MyCobot MoveIt2 迁移指南 (Migration Guide)

本文档旨在指导如何将 `mycobot_ros2` 工作区中的 MoveIt2 功能完整迁移到包含 LeoRover 和 Nav2 的导航工作区中。

## 1. 需要复制的核心包 (Packages to Copy)

请将以下文件夹从 `~/mycobot/src/mycobot_ros2/` 复制到你导航工作区的 `src` 目录下：

1.  **`mycobot_description`**: 包含机械臂的 URDF 模型和 Mesh 文件。
2.  **`mycobot_moveit_config`**: 包含 MoveIt2 的配置文件 (SRDF, controllers.yaml, ompl_planning.yaml)。
3.  **`mycobot_mtc_pick_place_demo`**: 包含你想要保留的 MTC 抓取代码。
4.  **`mycobot_interfaces`**: (如果有) 自定义消息接口。

```bash
# ⚠️ 注意：由于权限限制，我无法直接访问你的 Leorover 目录。
# 请在你的终端中运行以下命令，将这些包复制过去：

# 1. 确保目标目录存在
mkdir -p /home/student26/Leorover/src

# 2. 复制核心包
cp -r ~/mycobot/src/mycobot_ros2/mycobot_description /home/student26/Leorover/src/
cp -r ~/mycobot/src/mycobot_ros2/mycobot_moveit_config /home/student26/Leorover/src/
cp -r ~/mycobot/src/mycobot_ros2/mycobot_mtc_pick_place_demo /home/student26/Leorover/src/
cp -r ~/mycobot/src/mycobot_ros2/mycobot_interfaces /home/student26/Leorover/src/

# 3. 复制完成后，记得在 Leorover 工作区编译
# cd /home/student26/Leorover
# colcon build
```

---

## 2. URDF 合并指南 (URDF Integration)

这是最关键的一步。你需要把机械臂“安装”到小车上，并告诉 MoveIt 如何控制它。

### 2.1 修改 `leorover.urdf.xacro`

在你的导航工作区中，找到小车的 URDF 文件（通常是 `leorover.urdf.xacro`），做以下修改：

**第一步：引入 MyCobot 文件**
```xml
<!-- 在文件顶部引入 -->
<xacro:include filename="$(find mycobot_description)/urdf/mycobot_280_pi/mycobot_280_pi.urdf.xacro" />
```

**第二步：实例化机械臂**
```xml
<!-- 在小车主体定义之后，添加机械臂 -->
<!-- 假设安装在 base_link 上，位置需要根据实际情况调整 -->
<xacro:mycobot_280_pi parent="base_link" prefix="arm_">
    <origin xyz="0.1 0 0.2" rpy="0 0 0" /> <!-- 调整这里的 xyz 以匹配真实安装位置 -->
</xacro:mycobot_280_pi>
```

**第三步：添加 ros2_control 标签 (关键！)**
MoveIt 需要通过 `ros2_control` 控制机械臂。你需要确保合并后的 URDF 包含机械臂的 `ros2_control` 配置。
*   如果 `mycobot_280_pi.urdf.xacro` 里已经自带了 `<ros2_control>` 标签，通常可以直接用。
*   **注意**：检查 `hardware` 插件。如果是仿真，确保使用的是 `gazebo_ros2_control/GazeboSystem`。

---

## 3. Launch 文件合并 (Launch Integration)

你需要创建一个新的 Launch 文件（例如 `mobile_manipulation.launch.py`），同时启动 Nav2 和 MoveIt。

### 核心思路
不要试图把所有节点写在一个文件里。使用 `IncludeLaunchDescription` 引用现有的 Launch 文件。

```python
# mobile_manipulation.launch.py 伪代码

def generate_launch_description():
    # 1. 启动 Nav2 (引用你现有的 nav2 launch)
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([nav2_pkg_dir, '/launch/navigation_launch.py']),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # 2. 启动 MoveIt (引用 mycobot_moveit_config 的 demo.launch.py 或 move_group.launch.py)
    # 注意：需要传递合并后的 robot_description
    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([moveit_pkg_dir, '/launch/move_group.launch.py']),
        launch_arguments={
            'use_sim_time': 'true',
            'robot_description': robot_description_content # 需要加载合并后的 URDF
        }.items()
    )
    
    return LaunchDescription([nav2_launch, moveit_launch])
```

---

## 4. 控制器配置 (Controller Configuration)

MoveIt 和 Nav2 可能会争抢 `ros2_control` 的控制器管理器。

**最佳实践：**
1.  **统一控制器配置文件**：创建一个新的 `merged_controllers.yaml`。
    *   把小车的控制器（`diff_drive_controller`, `joint_state_broadcaster`）放进去。
    *   把机械臂的控制器（`arm_controller`, `gripper_controller`）放进去。
2.  **统一启动 Controller Manager**：只启动一个 `controller_manager` 节点，加载这个合并后的 yaml 文件。

---

## 5. 常见坑与解决方案

1.  **TF 树断裂**：确保 URDF 里机械臂的 `parent` 链接（如 `base_link`）在小车 URDF 里是存在的。
2.  **命名空间冲突**：如果机械臂加了 `prefix="arm_"`，记得去 `mycobot_moveit_config/config/mycobot_280_pi.srdf` 里把所有关节名字也都加上 `arm_` 前缀，否则 MoveIt 找不到关节。
3.  **资源占用**：同时跑 Nav2 + MoveIt + Gazebo 非常吃内存。如果没有 GPU，可能会很卡。

---

## 6. 给 Agent 的指令 (Prompt for Agent)

你可以把下面这段话发给另一个 Agent：

> "请帮我把 `mycobot_ros2` 里的 MoveIt 功能迁移到当前 Nav2 工作区。
> 1. 参考 `MIGRATION_GUIDE.md`，复制指定的 4 个包。
> 2. 修改 `leorover.urdf.xacro`，把 `mycobot_280_pi.urdf.xacro` include 进去，并连接到 `base_link`。
> 3. 创建一个 `merged_controllers.yaml`，合并小车和机械臂的控制器配置。
> 4. 创建一个 `bringup_all.launch.py`，同时启动 Gazebo, Nav2 和 MoveIt MoveGroup。"
