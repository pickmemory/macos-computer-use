# 🧠 AI 协作工作流程 (v2)

## ⚠️ 重要：使用 `image` 工具，不是 `read`！

**问题**: `read` 工具会丢弃图片原始数据，AI 无法真正"看到"截图。

**解决**: 使用 `image` 工具分析截图，AI 可以真正理解图片内容。

---

## 两种工作模式

### 模式 1: AI 指导模式（推荐）

最简单、最可靠的方式。AI 在聊天中指导你操作。

```bash
# 1. 截图
screencapture -x /tmp/screen.png

# 2. 在聊天中发送
image /tmp/screen.png "帮我分析当前界面，下一步应该点什么？"

# 3. AI 分析后返回
"我看到 Freeform 应用，需要点击'新建看板'按钮。
坐标大约在屏幕中央 (720, 420)。
执行：python3 mouse.py click 720 420"

# 4. 执行指令
python3 mouse.py click 720 420

# 5. 再次截图验证
screencapture -x /tmp/screen2.png
image /tmp/screen2.png "操作成功了吗？"
```

**优点**:
- ✅ 简单直接
- ✅ AI 真正看到截图
- ✅ 随时可以询问
- ✅ 不需要复杂的自动化

---

### 模式 2: 自动化循环模式

使用 `ai_loop.py` 脚本，半自动执行。

```bash
cd ~/.openclaw/workspace/skills/macos-computer-use
source .venv/bin/activate

# 启动 AI 循环
python3 scripts/ai_loop.py -t "在 Freeform 中画一个圆"
```

**工作流程**:

1. **脚本截图** → 保存到 `~/Projects/macos-ai-loop/step-01.png`
2. **等待指令** → 脚本暂停，等待你写入指令文件
3. **AI 分析** → 你在聊天中使用 `image` 工具分析截图
4. **写入指令** → 将 AI 返回的指令写入 `current-instruction.json`
5. **自动执行** → 脚本读取指令并执行
6. **循环** → 回到步骤 1，直到任务完成

**指令文件格式** (`~/Projects/macos-ai-loop/current-instruction.json`):

```json
{
  "action": "click",
  "params": {"x": 720, "y": 420},
  "reason": "点击新建看板按钮"
}
```

**支持的动作**:
- `click`: `{"x": 500, "y": 300}`
- `drag`: `{"from": [100, 200], "to": [400, 200], "duration": 0.5}`
- `hotkey`: `{"keys": ["cmd", "n"]}`
- `type`: `{"text": "Hello"}`
- `wait`: `{"seconds": 2}`
- `done`: `{"message": "任务完成"}`

**快速写入指令** (使用快捷命令):

```bash
# 方式 1: 直接写入
echo '{"action":"click","params":{"x":720,"y":420},"reason":"点击按钮"}' \
  > ~/Projects/macos-ai-loop/current-instruction.json

# 方式 2: 使用 cat
cat > ~/Projects/macos-ai-loop/current-instruction.json << 'EOF'
{"action":"click","params":{"x":720,"y":420},"reason":"点击按钮"}
EOF
```

---

## 📋 AI 分析指令模板

当你在聊天中使用 `image` 工具时，可以这样问：

```
image /tmp/screen.png "
任务：在 Freeform 中画一个红色的圆

请分析：
1. 当前界面是什么状态？
2. 下一步应该执行什么操作？
3. 具体坐标或动作是什么？

请以 JSON 格式返回指令：
{
  "action": "click|drag|hotkey|type|wait|done",
  "params": {...},
  "reason": "..."
}
"
```

---

## 🔧 脚本参考

### screenshot.py
```bash
# 全屏截图
python3 scripts/screenshot.py --output /tmp/screen.png

# 窗口截图
python3 scripts/screenshot.py --window "Freeform" --output /tmp/freeform.png

# 区域截图
python3 scripts/screenshot.py --region 0 0 800 600 --output /tmp/region.png
```

### mouse.py
```bash
# 点击
python3 scripts/mouse.py click 500 300

# 拖拽
python3 scripts/mouse.py drag 100 200 400 200 --duration 0.5

# 滚动
python3 scripts/mouse.py scroll 500 300 --dy -5
```

### keyboard.py
```bash
# 输入文字
python3 scripts/keyboard.py type "Hello world"

# 按键
python3 scripts/keyboard.py press return

# 快捷键
python3 scripts/keyboard.py hotkey cmd shift s
```

### ai_loop.py
```bash
# 基本使用
python3 scripts/ai_loop.py -t "任务描述"

# 自定义参数
python3 scripts/ai_loop.py -t "任务" --steps 10 --timeout 600
```

---

## ✅ 最佳实践

1. **始终使用 `image` 工具** - 不要用 `read` 读取图片
2. **截图后立刻分析** - 避免界面变化导致坐标失效
3. **小步快跑** - 每步只做一件事，验证后再继续
4. **保存截图** - 便于回溯和调试
5. **容错处理** - 如果操作失败，重新截图分析

---

## 🐛 常见问题

### Q: AI 说"无法读取图片"
**A**: 确保使用 `image` 工具，不是 `read` 工具。

### Q: 坐标点击不准
**A**: Retina 屏幕需要坐标转换：`cliclick 坐标 = 截图坐标 ÷ 2`

### Q: 脚本等待超时
**A**: 增加 `--timeout` 参数，或检查指令文件格式是否正确。

### Q: 操作后界面没变化
**A**: 可能需要权限（Accessibility / Screen Recording），运行 `setup.sh` 检查。

---

## 📝 示例会话

**任务**: 在 Freeform 中画一个圆

```
[步骤 1]
你：screencapture -x /tmp/step1.png
你：image /tmp/step1.png "任务：在 Freeform 中画圆。当前状态？下一步？"
AI: "看到 Freeform 欢迎界面。需要点击'新建看板'。坐标 (720, 420)。"
你：python3 mouse.py click 720 420

[步骤 2]
你：screencapture -x /tmp/step2.png
你：image /tmp/step2.png "画布打开了吗？如何选画笔？"
AI: "画布已打开。按 Cmd+2 选择画笔工具。"
你：python3 keyboard.py hotkey cmd 2

[步骤 3]
你：screencapture -x /tmp/step3.png
你：image /tmp/step3.png "画笔选中了吗？如何画圆？"
AI: "画笔已选中。从 (500,350) 拖拽到 (600,450) 画圆。"
你：python3 mouse.py drag 500 350 600 450 --duration 0.5

[步骤 4]
你：screencapture -x /tmp/step4.png
你：image /tmp/step4.png "画好了吗？"
AI: "✅ 圆已画好！任务完成。"
```

---

**开始使用吧！** 记住：**`image` 工具是关键** 📸🧠🤖
