# 🚀 快速测试指南

## 5 分钟测试 AI 协作流程

### 步骤 1: 截图

```bash
cd ~/.openclaw/workspace/skills/macos-computer-use

# 截图
python3 scripts/screenshot.py --output /tmp/test-screen.png
```

### 步骤 2: 使用 `image` 工具分析

在聊天中发送：

```
image /tmp/test-screen.png "请分析这个截图：
1. 这是什么应用/界面？
2. 能看到哪些 UI 元素？
3. 如果要在屏幕上点击一个位置，你会建议点哪里？"
```

⚠️ **重要**: 使用 `image` 工具，**不是** `read` 工具！

### 步骤 3: 执行 AI 建议的操作

AI 会返回类似：
```
我看到这是 macOS 桌面，有多个应用窗口。
建议点击屏幕中央的 Safari 窗口，坐标大约是 (640, 400)。
```

然后执行：
```bash
python3 scripts/mouse.py click 640 400
```

### 步骤 4: 验证

```bash
# 再次截图
python3 scripts/screenshot.py --output /tmp/test-screen2.png

# 发送给 AI 验证
image /tmp/test-screen2.png "操作成功了吗？有什么变化？"
```

---

## 测试 AI Loop 脚本

### 启动 AI Loop

```bash
cd ~/.openclaw/workspace/skills/macos-computer-use
source .venv/bin/activate  # 如果有虚拟环境

python3 scripts/ai_loop.py -t "探索当前界面" --steps 5 --timeout 120
```

### 工作流程

1. 脚本自动截图 → `~/Projects/macos-ai-loop/step-01-xxxxx.png`
2. 脚本等待指令（120 秒超时）
3. 在聊天中使用 `image` 工具分析截图
4. AI 返回指令后，快速写入指令文件：

```bash
# 方式 1: 快捷命令
python3 scripts/set_instruction.py click 640 400 "点击窗口"

# 方式 2: JSON
echo '{"action":"click","params":{"x":640,"y":400},"reason":"点击"}' \
  > ~/Projects/macos-ai-loop/current-instruction.json
```

5. 脚本自动读取并执行
6. 循环继续...

### 结束任务

```bash
python3 scripts/set_instruction.py done "测试完成"
```

---

## 常见问题

### Q: `image` 工具不可用
**A**: 检查 OpenClaw 配置，确保模型支持视觉功能。

### Q: 截图是黑色的
**A**: 需要授予 Screen Recording 权限：
```bash
python3 scripts/setup.sh
```

### Q: 鼠标点击没反应
**A**: 需要授予 Accessibility 权限：
```bash
python3 scripts/setup.sh
```

### Q: 坐标不准
**A**: Retina 屏幕坐标需要除以 2。使用 `find_ui.py` 自动获取准确坐标：
```bash
python3 scripts/find_ui.py --app "Safari" --role AXButton
```

---

## 下一步

- 📖 阅读 [AI_WORKFLOW.md](AI_WORKFLOW.md) 了解完整工作流程
- 📖 阅读 [AI_ENHANCED_GUIDE.md](AI_ENHANCED_GUIDE.md) 了解 AI 增强理念
- 🎯 尝试真实任务：在 Freeform 中画画、自动填写表单等
