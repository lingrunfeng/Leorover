#!/bin/bash
# 修复网络连接并SSH到机械臂

echo "🔧 修复网络连接..."

# 清除旧IP
sudo ip addr flush dev enp0s31f6 2>/dev/null

# 设置静态IP
sudo ip addr add 10.3.14.100/24 dev enp0s31f6
sudo ip link set enp0s31f6 up

echo "✅ 网络已重新配置"
echo ""
echo "📡 测试连接..."
ping -c 2 10.3.14.59

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 网络连接正常！"
    echo ""
    echo "🤖 现在连接SSH..."
    echo "   密码：trunk"
    echo ""
    ssh elephant@10.3.14.59
else
    echo ""
    echo "❌ 网络连接失败"
    echo ""
    echo "请检查："
    echo "1. 网线是否插好"
    echo "2. 机械臂是否上电"
    echo "3. 等待30秒让树莓派启动完成"
fi
