# 💬 聊天指导模式 - 推荐工作流程

## 核心理念

**AI 助手（我）本身就是多模态模型，在聊天中分析截图是最自然、最可靠的方式。**

不需要复杂的自动化脚本。你截图 → 发给我分析 → 我返回指令 → 你执行。

---

## 工作流程

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│  1. 截图    │ ──→ │ 2. 用 image  │ ──→ │ 3. AI 分析  │ ──→ │ 4. 执行指令 │
│             │     │   工具分析   │     │   返回指令   │     │             │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ↓
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│  6. 完成    │ ←── │ 5. 再次截图  │ ←── │   验证效果   │ ←── │   循环继续   │
└─────────────┘     └──────────────┘     └──────────────┘     └─────────────┘
```

---

## 快速开始

### 步骤 1: 截图

```bash
# 全屏截图
screencapture -x /tmp/screen.png

# 或使用脚本
python3 scripts/screenshot.py --output /tmp/screen.png
```

### 步骤 2: 在聊天中发送

```
image /tmp/screen.png "请分析当前界面，下一步应该点什么？"
```

⚠️ **重要**: 使用 `image` 工具，**不是** `read` 工具！

### 步骤 3: AI 返回指令

例如：
```
我看到 Freeform 应用已打开，显示空白画布。

顶部工具栏有画笔工具，建议点击坐标 (1440, 100) 选择画笔。

执行：python3 mouse.py click 1440 100
```

### 步骤 4: 执行指令

```bash
python3 mouse.py click 1440 100
```

### 步骤 5: 验证

```bash
# 再次截图
screencapture -x /tmp/screen2.png

# 发送验证
image /tmp/screen2.png "画笔选中了吗？"
```

### 步骤 6: 循环直到完成

---

## 完整示例：在 Freeform 中画一只猫

### 第 1 步：打开 Freeform 并截图

```bash
open -a "Freeform"
sleep 2
screencapture -x /tmp/cat-step1.png
```

**在聊天中发送：**
```
image /tmp/cat-step1.png "任务：在 Freeform 中画一只猫。当前是什么界面？第一步应该做什么？"
```

**AI 分析：**
```
我看到 Freeform 显示"所有看板"视图，不是编辑画布。

第一步：新建看板
- 按 Cmd+N 快捷键
- 或点击屏幕中央的"+"按钮

建议：按 Cmd+N 更快
```

**执行：**
```bash
python3 keyboard.py hotkey cmd n
```

---

### 第 2 步：确认画布打开

```bash
screencapture -x /tmp/cat-step2.png
```

**在聊天中发送：**
```
image /tmp/cat-step2.png "画布打开了吗？如何选择画笔？"
```

**AI 分析：**
```
✅ 画布已打开，是空白的。

选择画笔：
- 按 Cmd+2 选择画笔工具
- 或点击顶部工具栏的画笔图标

建议：按 Cmd+2
```

**执行：**
```bash
python3 keyboard.py hotkey cmd 2
```

---

### 第 3 步：画猫头（圆形）

```bash
screencapture -x /tmp/cat-step3.png
```

**在聊天中发送：**
```
image /tmp/cat-step3.png "画笔选中了吗？如何画猫头（圆形）？"
```

**AI 分析：**
```
✅ 画笔已选中（有蓝色高亮）。

画猫头（圆形）：
- 从画布中央 (1440, 800) 开始
- 拖拽到 (1640, 1000) 画圆
-  duration 0.8 秒让线条更圆滑

执行：python3 mouse.py drag 1440 800 1640 1000 --duration 0.8
```

**执行：**
```bash
python3 mouse.py drag 1440 800 1640 1000 --duration 0.8
```

---

### 第 4 步：画猫耳朵（三角形）

```bash
screencapture -x /tmp/cat-step4.png
```

**在聊天中发送：**
```
image /tmp/cat-step4.png "猫头画好了吗？如何画耳朵？"
```

**AI 分析：**
```
✅ 猫头（圆形）已画好。

画左耳朵（三角形）：
- 从 (1400, 750) 开始
- 拖拽到 (1350, 650)
- 再拖拽到 (1450, 750) 完成三角形

执行：
python3 mouse.py drag 1400 750 1350 650 --duration 0.5
python3 mouse.py drag 1350 650 1450 750 --duration 0.5
```

**执行：**
```bash
python3 mouse.py drag 1400 750 1350 650 --duration 0.5
python3 mouse.py drag 1350 650 1450 750 --duration 0.5
```

---

### 第 5 步：继续画其他部分

重复以上流程，直到完成：
- 右耳朵
- 眼睛
- 鼻子
- 嘴巴
- 胡须
- 身体
- 尾巴

---

### 第 6 步：完成验证

```bash
screencapture -x /tmp/cat-final.png
```

**在聊天中发送：**
```
image /tmp/cat-final.png "猫画好了吗？还有什么需要改进的？"
```

**AI 分析：**
```
🎉 猫画好了！

我看到：
✅ 头部（圆形）
✅ 耳朵（两个三角形）
✅ 眼睛、鼻子、嘴巴
✅ 身体和尾巴

可以添加颜色让猫更生动！
```

---

## 快捷指令工具

使用 `set_instruction.py` 快速执行常见操作：

```bash
# 点击
python3 scripts/set_instruction.py click 500 300 "点击按钮"

# 拖拽
python3 scripts/set_instruction.py drag 100 200 400 200 "画线"

# 快捷键
python3 scripts/set_instruction.py hotkey cmd n "新建"

# 输入
python3 scripts/set_instruction.py type "Hello" "输入文字"

# 完成
python3 scripts/set_instruction.py done "任务完成"
```

---

## 优势对比

| 自动化循环模式 | 聊天指导模式 |
|---------------|-------------|
| ❌ 脚本等待超时 | ✅ 自然对话节奏 |
| ❌ 无法实时分析 | ✅ AI 真正看到截图 |
| ❌ 盲写指令 | ✅ 每步都有验证 |
| ❌ 复杂文件操作 | ✅ 简单直接 |
| ❌ 调试困难 | ✅ 问题即时发现 |

---

## 常见问题

### Q: 为什么不自动化？
**A**: AI 需要真正看到截图才能做出正确决策。自动化脚本无法替代视觉分析。

### Q: 每次都要截图很麻烦
**A**: 可以用快捷键 `Cmd+Shift+3` 快速截图，或使用脚本自动化截图。

### Q: 坐标不准怎么办
**A**: Retina 屏幕坐标需要除以 2。使用 `find_ui.py` 自动获取准确坐标。

### Q: 能完全自动化吗
**A**: 可以，但需要集成视觉 API（如 GLM-4V），增加复杂度。聊天模式最简单可靠。

---

## 总结

**聊天指导模式的核心**：

1. 📸 **你截图** - 捕获当前界面
2. 🧠 **我分析** - 使用 `image` 工具真正理解截图
3. 🎯 **我指导** - 返回具体操作指令
4. 🤖 **你执行** - 运行命令
5. ✅ **我验证** - 对比前后变化
6. 🔄 **循环** - 直到任务完成

**简单、可靠、有效！** 🚀
