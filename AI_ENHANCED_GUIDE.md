# 🧠 AI 增强版使用指南

## 核心原则

**每步都必须真正读取截图并分析**，不能机械执行预设命令！

## 完整流程示例

### 任务：在 Freeform 中画一只猫

```bash
cd ~/.openclaw/workspace/skills/macos-computer-use
source .venv/bin/activate
```

---

### 步骤 1: 打开应用并截图

```bash
# 打开 Freeform
open -a "Freeform"
sleep 2

# 截图
python3 scripts/screenshot.py --output ~/Projects/macos-ai-test/step1.png
```

**现在 AI 助手需要做**:
1. 读取截图：`read ~/Projects/macos-ai-test/step1.png`
2. 分析看到的内容
3. 返回下一步指令

**正确的 AI 分析应该是**:
```
我看到 Freeform 应用已打开，但显示的是"所有看板"视图，不是编辑画布。

需要先新建看板：
- 点击"新建看板"按钮
- 或者按 Cmd+N

建议操作：点击屏幕中央的"新建看板"按钮
```

---

### 步骤 2: 新建画布

根据 AI 分析执行：

```bash
# 如果 AI 说需要点"新建看板"
python3 scripts/mouse.py click 720 420

# 再次截图
python3 scripts/screenshot.py --output ~/Projects/macos-ai-test/step2.png
```

**AI 再次读取分析**:
```
我看到画布已创建，是空白的。

现在需要选择画笔工具：
- 顶部工具栏有画笔图标
- 或者按 Cmd+2 选择工具

建议操作：按 Cmd+2 选择画笔工具
```

---

### 步骤 3: 选择画笔

```bash
python3 scripts/keyboard.py hotkey cmd 2

# 截图验证
python3 scripts/screenshot.py --output ~/Projects/macos-ai-test/step3.png
```

**AI 读取验证**:
```
我看到画笔工具已选中（有蓝色高亮）。

现在可以开始画了。先画头部（圆形）：
- 从画布中央开始
- 拖拽画圆

建议操作：从 (600, 350) 拖拽到 (700, 450) 画圆
```

---

### 步骤 4: 开始画画

```bash
# 画头部
python3 scripts/mouse.py drag 600 350 700 450 --duration 0.5

# 截图验证
python3 scripts/screenshot.py --output ~/Projects/macos-ai-test/step4.png
```

**AI 读取验证**:
```
我看到画布上出现了一条线！画笔工作正常。

继续画猫的其他部分...
```

---

## 关键区别

### ❌ 我之前错误的做法

```
1. 截图（但没读）
2. 直接执行预设命令
3. 最后才看一眼结果
4. 发现什么都没画出来
```

### ✅ 正确的做法

```
1. 截图
2. AI 真正读取截图分析
3. 基于分析返回指令
4. 执行指令
5. 再次截图
6. AI 读取验证效果
7. 决定下一步
8. 循环直到完成
```

---

## AI 助手检查清单

在每步分析时，AI 必须回答：

1. **我看到了什么？** - 描述截图内容
2. **当前状态是什么？** - 应用/画布/工具状态
3. **下一步应该做什么？** - 具体操作
4. **为什么？** - 解释理由
5. **如何验证成功？** - 预期看到什么变化

---

## 快速测试

```bash
# 1. 打开 Freeform 并截图
open -a "Freeform" && sleep 2
python3 scripts/screenshot.py --output ~/Projects/macos-ai-test/test1.png

# 2. AI 读取分析
# → 在聊天中发送：read ~/Projects/macos-ai-test/test1.png
# → AI 分析并返回指令

# 3. 执行指令
# → 根据 AI 返回的指令执行

# 4. 验证
python3 scripts/screenshot.py --output ~/Projects/macos-ai-test/test2.png
# → AI 再次读取对比
```

---

## 总结

**AI 增强版的核心价值**：

| 传统脚本 | AI 增强版 |
|---------|----------|
| 预设坐标 | AI 看截图识别 |
| 无法验证 | AI 读图验证 |
| 失败不知 | AI 观察调整 |
| 机械执行 | 动态决策 |

**但前提是 AI 必须真正读取截图分析！**

---

开始测试吧！记住：**先读图，再决策，后执行** 📸🧠🤖
