#!/bin/bash
# 设置网络连接到myCobot的树莓派
# 树莓派IP: 10.3.14.59
# 需要密码: Ling20021.2.0.8

echo "=========================================="
echo "🌐 myCobot网络连接设置"
echo "=========================================="

# 检测以太网接口
ETH_INTERFACE="enp0s31f6"  # 你的有线网卡

echo ""
echo "📡 检测网络接口..."
ip link show $ETH_INTERFACE

if [ $? -ne 0 ]; then
    echo "❌ 找不到网络接口 $ETH_INTERFACE"
    echo "请运行: ip addr 查看你的网络接口名称"
    exit 1
fi

echo ""
echo "🔧 配置静态IP..."
echo "   你的电脑IP: 10.3.14.100"
echo "   树莓派IP:   10.3.14.59"
echo ""
echo "需要sudo权限，请输入密码: Ling20021.2.0.8"

# 设置静态IP
sudo ip addr add 10.3.14.100/24 dev $ETH_INTERFACE 2>/dev/null
sudo ip link set $ETH_INTERFACE up

echo ""
echo "✅ 网络配置完成！"
echo ""
echo "📍 测试连接..."
ping -c 3 10.3.14.59

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "🎉 连接成功！"
    echo "=========================================="
    echo ""
    echo "📝 可以使用的命令："
    echo "   1. SSH连接树莓派："
    echo "      ssh elephant@10.3.14.59"
    echo "      密码: trunk"
    echo ""
    echo "   2. 测试ROS2话题："
    echo "      ros2 topic list"
    echo ""
    echo "   3. 运行机械臂控制："
    echo "      ssh elephant@10.3.14.59"
    echo "      然后在树莓派上："
    echo "      ros2 launch mycobot_280pi slider_control.launch.py"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "⚠️  无法ping通树莓派"
    echo "=========================================="
    echo ""
    echo "请检查："
    echo "1. 网线是否插好（两端都要插紧）"
    echo "2. 机械臂是否上电"
    echo "3. 树莓派是否启动（等待30秒后重试）"
    echo ""
    echo "重新运行此脚本："
    echo "   bash setup_network_connection.sh"
    echo "=========================================="
fi
