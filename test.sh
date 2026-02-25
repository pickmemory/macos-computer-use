#!/bin/bash
# Mac Computer Use - 快速测试脚本

SKILL_DIR="$HOME/.openclaw/workspace/skills/macos-computer-use"
PYTHON="$SKILL_DIR/.venv/bin/python3"

echo "🖥️  Mac Computer Use 快速测试"
echo "=============================="
echo ""

# 测试 1: 截图
echo "📸 测试 1: 截图..."
$PYTHON "$SKILL_DIR/scripts/screenshot.py" --output /tmp/mcu-test.png
echo "   ✅ 截图保存：/tmp/mcu-test.png"
echo ""

# 测试 2: 查找 UI 元素
echo "🔍 测试 2: 查找前台应用的 UI 元素..."
$PYTHON "$SKILL_DIR/scripts/find_ui.py" --limit 3
echo ""

# 测试 3: 获取当前鼠标位置
echo "📍 测试 3: 获取当前鼠标位置..."
$PYTHON "$SKILL_DIR/scripts/mouse.py" getpos
echo ""

echo "=============================="
echo "✅ 所有测试完成！"
echo ""
echo "📚 常用命令:"
echo "   截图：python3 $SKILL_DIR/scripts/screenshot.py"
echo "   点击：python3 $SKILL_DIR/scripts/mouse.py click X Y"
echo "   输入：python3 $SKILL_DIR/scripts/keyboard.py type \"Hello\""
echo "   找元素：python3 $SKILL_DIR/scripts/find_ui.py --app \"Safari\" --role AXButton"
echo ""
