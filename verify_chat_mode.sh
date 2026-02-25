#!/bin/bash
# 验证聊天指导模式的工作流程
# 测试任务：在 Freeform 中画一个简单的形状

set -e

echo "========================================"
echo "🧪 验证聊天指导模式"
echo "========================================"
echo ""

# 1. 打开 Freeform
echo "📱 步骤 1: 打开 Freeform..."
open -a "Freeform"
sleep 3

# 2. 截图
echo "📸 步骤 2: 截图..."
SCREENSHOT="/tmp/verify-step1.png"
/usr/sbin/screencapture -x "$SCREENSHOT"
echo "   截图：$SCREENSHOT"

# 3. 显示指令
echo ""
echo "========================================"
echo "📋 现在请在聊天中发送以下内容："
echo "========================================"
echo ""
echo "image $SCREENSHOT \"请分析当前 Freeform 界面，第一步应该做什么？\""
echo ""
echo "========================================"
echo "⏳ 等待 AI 返回指令后，继续执行..."
echo "========================================"
echo ""

# 等待用户确认
read -p "按回车继续..."

# 4. 新建看板（Cmd+N）
echo "⌨️  步骤 4: 新建看板 (Cmd+N)..."
python3 scripts/keyboard.py hotkey cmd n
sleep 2

# 5. 再次截图
echo "📸 步骤 5: 截图验证..."
SCREENSHOT2="/tmp/verify-step2.png"
/usr/sbin/screencapture -x "$SCREENSHOT2"
echo "   截图：$SCREENSHOT2"

echo ""
echo "========================================"
echo "📋 请在聊天中发送："
echo "========================================"
echo ""
echo "image $SCREENSHOT2 \"画布打开了吗？如何选择画笔工具？\""
echo ""
echo "========================================"
echo "⏳ 等待 AI 返回指令..."
echo "========================================"
echo ""

read -p "按回车继续..."

# 6. 选择画笔（Cmd+2）
echo "⌨️  步骤 6: 选择画笔 (Cmd+2)..."
python3 scripts/keyboard.py hotkey cmd 2
sleep 1

# 7. 画一条线
echo "🎨 步骤 7: 画一条测试线..."
python3 scripts/mouse.py drag 1400 800 1600 800 --duration 0.5
sleep 1

# 8. 最终截图
echo "📸 步骤 8: 最终截图验证..."
SCREENSHOT3="/tmp/verify-final.png"
/usr/sbin/screencapture -x "$SCREENSHOT3"
echo "   截图：$SCREENSHOT3"

echo ""
echo "========================================"
echo "📋 请在聊天中发送验证："
echo "========================================"
echo ""
echo "image $SCREENSHOT3 \"画线成功了吗？\""
echo ""
echo "========================================"
echo "✅ 验证完成！"
echo "========================================"
echo ""
echo "截图已保存："
echo "  1. $SCREENSHOT"
echo "  2. $SCREENSHOT2"
echo "  3. $SCREENSHOT3"
echo ""
