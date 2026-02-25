#!/bin/bash
# Fail Fast 测试脚本
# 每步操作后立即验证，失败立即停止

set -e  # 任何命令失败立即退出

echo "========================================"
echo "🐱 Fail Fast 测试：在 Freeform 中画猫"
echo "========================================"
echo ""

# 工具函数
step() {
    echo ""
    echo "========================================"
    echo "📍 步骤 $1: $2"
    echo "========================================"
}

verify() {
    local step_name="$1"
    local screenshot="$2"
    local check_cmd="$3"
    
    echo "📸 截图：$screenshot"
    /usr/sbin/screencapture -x "$screenshot"
    
    echo ""
    echo "========================================"
    echo "✅ 请验证："
    echo "========================================"
    echo ""
    echo "image $screenshot \"$check_cmd\""
    echo ""
    echo "========================================"
    echo "⏳ 等待确认... (按回车继续，Ctrl+C 停止)"
    echo "========================================"
    read -p "> "
}

# 检查 Freeform 是否运行
check_freeform() {
    if ! pgrep -x "Freeform" > /dev/null; then
        echo "❌ Freeform 未运行，请先打开应用"
        exit 1
    fi
}

# 开始
cd /Users/heyi/.openclaw/workspace/skills/macos-computer-use
source .venv/bin/activate

step "1" "打开 Freeform"
check_freeform
echo "✅ Freeform 已运行"

step "2" "新建画布 (Cmd+N)"
python3 scripts/keyboard.py hotkey cmd n
sleep 2
verify "2" "/tmp/cat-step2.png" "画布打开了吗？是空白画布吗？"

step "3" "选择画笔工具 (Cmd+2)"
python3 scripts/keyboard.py hotkey cmd 2
sleep 1
verify "3" "/tmp/cat-step3.png" "画笔工具选中了吗？（有蓝色高亮）"

step "4" "画猫头（圆形）"
python3 scripts/mouse.py drag 1400 700 1600 900 --duration 0.8
sleep 1
verify "4" "/tmp/cat-step4.png" "猫头（圆形）画好了吗？位置对吗？"

step "5" "画左耳朵（三角形）"
python3 scripts/mouse.py drag 1380 680 1350 600 --duration 0.3
python3 scripts/mouse.py drag 1350 600 1420 680 --duration 0.3
sleep 1
verify "5" "/tmp/cat-step5.png" "左耳朵画好了吗？"

step "6" "画右耳朵（三角形）"
python3 scripts/mouse.py drag 1580 680 1620 600 --duration 0.3
python3 scripts/mouse.py drag 1620 600 1680 680 --duration 0.3
sleep 1
verify "6" "/tmp/cat-step6.png" "右耳朵画好了吗？"

step "7" "画眼睛（两个点）"
python3 scripts/mouse.py drag 1450 750 1470 770 --duration 0.3
python3 scripts/mouse.py drag 1530 750 1550 770 --duration 0.3
sleep 1
verify "7" "/tmp/cat-step7.png" "眼睛画好了吗？位置对吗？"

step "8" "画鼻子和嘴巴"
python3 scripts/mouse.py drag 1490 780 1510 800 --duration 0.3
python3 scripts/mouse.py drag 1480 810 1520 810 --duration 0.3
sleep 1
verify "8" "/tmp/cat-step8.png" "鼻子和嘴巴画好了吗？"

step "9" "画胡须（左右各三条）"
python3 scripts/mouse.py drag 1440 790 1380 790 --duration 0.3
python3 scripts/mouse.py drag 1440 800 1380 800 --duration 0.3
python3 scripts/mouse.py drag 1440 810 1380 810 --duration 0.3
python3 scripts/mouse.py drag 1560 790 1620 790 --duration 0.3
python3 scripts/mouse.py drag 1560 800 1620 800 --duration 0.3
python3 scripts/mouse.py drag 1560 810 1620 810 --duration 0.3
sleep 1
verify "9" "/tmp/cat-step9.png" "胡须画好了吗？"

step "10" "完成验证"
echo "🎉 猫画完了！"
echo ""
echo "最终截图：/tmp/cat-step9.png"
echo ""
echo "========================================"
echo "✅ 测试完成！"
echo "========================================"
