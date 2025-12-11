#!/bin/bash
# myCobot网络诊断和连接脚本

echo "=========================================="
echo "🔍 myCobot 网络诊断"
echo "=========================================="

ETH="enp0s31f6"

# 1. 检查物理连接
echo ""
echo "📡 步骤1: 检查物理连接"
LINK_STATUS=$(ip link show $ETH | grep -o "state [A-Z]*" | awk '{print $2}')
echo "   网卡状态: $LINK_STATUS"

if [ "$LINK_STATUS" != "UP" ]; then
    echo "   ❌ 网卡未激活，尝试启动..."
    sudo ip link set $ETH up
    sleep 2
fi

# 2. 尝试静态IP方式
echo ""
echo "🔧 步骤2: 配置静态IP (10.3.14.100)"
sudo ip addr flush dev $ETH 2>/dev/null
sudo ip addr add 10.3.14.100/24 dev $ETH
sudo ip link set $ETH up

echo "   等待5秒..."
sleep 5

echo ""
echo "📍 步骤3: 测试树莓派 (10.3.14.59)"
ping -c 2 -W 2 10.3.14.59

if [ $? -eq 0 ]; then
    echo "   ✅ 找到树莓派！IP: 10.3.14.59"
    echo ""
    echo "🤖 连接SSH..."
    ssh elephant@10.3.14.59
    exit 0
fi

echo "   ⚠️  静态IP方式失败"

# 3. 尝试DHCP方式
echo ""
echo "🔧 步骤4: 尝试DHCP自动获取IP"
sudo ip addr flush dev $ETH
sudo dhclient -v $ETH 2>&1 | head -10 &
DHCP_PID=$!

echo "   等待10秒获取IP..."
sleep 10

# 检查是否获取到IP
MY_IP=$(ip addr show $ETH | grep "inet " | awk '{print $2}' | cut -d/ -f1)
echo "   我的IP: $MY_IP"

if [ -n "$MY_IP" ]; then
    # 扫描同网段
    NETWORK=$(echo $MY_IP | cut -d. -f1-3)
    echo ""
    echo "📡 步骤5: 扫描网段 $NETWORK.0/24"
    echo "   尝试ping常见IP..."
    
    for i in 1 59 100 254; do
        TARGET="$NETWORK.$i"
        if ping -c 1 -W 1 $TARGET &>/dev/null; then
            echo "   ✅ 发现设备: $TARGET"
            
            # 尝试SSH
            timeout 3 ssh -o ConnectTimeout=2 -o StrictHostKeyChecking=no elephant@$TARGET "hostname" 2>/dev/null
            if [ $? -eq 0 ]; then
                echo "   🎉 这是myCobot的树莓派！"
                echo ""
                echo "🤖 连接SSH..."
                ssh elephant@$TARGET
                exit 0
            fi
        fi
    done
fi

# 4. 手动扫描
echo ""
echo "=========================================="
echo "❓ 自动连接失败"
echo "=========================================="
echo ""
echo "可能的原因："
echo "1. 树莓派SD卡没插好或系统没启动"
echo "2. 网线连接的不是正确的以太网口"
echo "3. 树莓派使用了不同的网络配置"
echo ""
echo "建议："
echo "1. 检查机械臂底座是否有LED灯闪烁（树莓派启动标志）"
echo "2. 等待60秒后重新运行此脚本"
echo "3. 确认网线插在底座**前面**的以太网口"
echo "4. 尝试重启机械臂（关电源，等5秒，再开）"
echo ""
echo "重新运行: bash diagnose_network.sh"
echo "=========================================="
