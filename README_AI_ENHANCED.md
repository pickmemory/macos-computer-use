# 🧠 Macos Computer Use - AI 增强版

## 核心理念

**不需要额外的模型或 API** —— AI 助手（我）本身就是多模态大模型，可以直接：
- 📸 看截图理解 UI
- 🧠 分析当前状态
- 🎯 指导下一步操作
- ✅ 验证执行结果

## 增强方式

在原有 `macos-computer-use` 基础上，增加**AI 协作模式**：

```bash
# 1. 截图
python3 scripts/screenshot.py --output /tmp/test.png

# 2. 把截图发送给 AI 助手（我）
# → 我直接看图片分析

# 3. 我返回操作指令
# → "点击位置 (850, 40)，这应该是画笔工具"

# 4. 执行
python3 scripts/mouse.py click 850 40

# 5. 再次截图验证
python3 scripts/screenshot.py --output /tmp/test2.png

# 6. 我对比两张图判断成功
```

## 使用流程

### 场景 1: AI 指导模式

```bash
# 用户：帮我探索 Freeform 应用

# 1. 截图
python3 scripts/screenshot.py --output /tmp/freeform-1.png

# 2. 发送截图给 AI（我）
# 在聊天中说："这是 Freeform 的截图，帮我分析如何开始画画"

# 3. 我分析后返回
# "我看到顶部工具栏，点击 (850, 40) 选择画笔工具"

# 4. 执行
python3 scripts/mouse.py click 850 40

# 5. 再次截图
python3 scripts/screenshot.py --output /tmp/freeform-2.png

# 6. 我验证
# "画笔已选中，现在可以拖拽画线了"
```

### 场景 2: 自主探索（AI 主导）

```bash
# 用户：在 Freeform 中画一个红色的圆

# 我（AI）主导整个流程：
# 1. 让你执行截图
# 2. 我分析截图
# 3. 我告诉你执行什么命令
# 4. 你执行后再次截图
# 5. 我验证并决定下一步
# 6. 循环直到完成
```

## 核心脚本（继承原版）

| 脚本 | 功能 | 说明 |
|------|------|------|
| `screenshot.py` | 截图 | 保存 PNG，返回路径 |
| `mouse.py` | 鼠标控制 | click/drag/scroll |
| `keyboard.py` | 键盘控制 | type/hotkey/press |
| `find_ui.py` | UI 发现 | Accessibility API |
| `applescript.py` | AppleScript | 应用级控制 |

## AI 分析示例

### 示例 1: 识别应用

**截图**: Freeform 应用，空白画布

**我分析**:
```
应用类型：画图应用（无边记）
界面布局：
  - 顶部：工具栏（有画笔、形状、文字等工具）
  - 中间：空白画布
  - 左侧：工具面板（颜色、线条粗细）
  
当前状态：新建的空白看板，可以开始画画

建议操作：
  1. 先选择画笔工具（顶部工具栏）
  2. 选择颜色（左侧面板）
  3. 在画布上拖拽画线
```

### 示例 2: 对比验证

**截图 1**（操作前）: 空白画布

**截图 2**（操作后）: 画布上有一条线

**我对比**:
```
变化检测：
  - 画布中央出现一条黑色线条
  - 从 (500, 350) 到 (600, 350)
  
判断：✅ 画线操作成功

下一步：可以继续画其他部分，或改变颜色
```

## 优势对比

| 原版 | AI 增强版 |
|------|---------|
| 需要预先知道坐标 | AI 看截图识别位置 |
| 固定脚本流程 | AI 动态调整策略 |
| 无法验证结果 | AI 对比截图验证 |
| 失败无法恢复 | AI 观察失败并尝试其他方法 |
| 需要 Accessibility 支持 | AI 视觉识别（无 API 也能用） |

## 快速开始

```bash
cd ~/.openclaw/workspace/skills/macos-computer-use
source .venv/bin/activate

# 1. 截图
python3 scripts/screenshot.py --output /tmp/screen.png

# 2. 发送截图给 AI 助手（在聊天中）
# "这是当前屏幕截图，帮我分析如何操作"

# 3. AI 返回指令后执行
python3 scripts/mouse.py click X Y

# 4. 再次截图验证
python3 scripts/screenshot.py --output /tmp/screen2.png
```

## 实际案例

### 案例：在 Freeform 中画猫

```
用户：帮我画一只猫

AI 主导流程:

1. [AI] 请截图当前 Freeform 界面
2. [用户] 执行截图 → /tmp/cat-1.png
3. [AI] 分析截图 → "点击 (850, 40) 选择画笔"
4. [用户] 执行 → python3 mouse.py click 850 40
5. [AI] 请截图验证
6. [用户] 执行截图 → /tmp/cat-2.png
7. [AI] 对比验证 → "画笔已选中，现在拖拽画圆"
8. [用户] 执行拖拽 → python3 mouse.py drag 500 350 600 350
9. ... 循环直到完成
10. [AI] "猫画好了！✅"
```

## 文件结构

```
macos-computer-use/
├── scripts/
│   ├── screenshot.py      # 截图
│   ├── mouse.py           # 鼠标
│   ├── keyboard.py        # 键盘
│   ├── find_ui.py         # UI 发现
│   └── applescript.py     # AppleScript
└── README_AI_ENHANCED.md  # 本文档
```

## 总结

**AI 增强版的核心**：

1. 📸 脚本负责**执行**（截图、点击、输入）
2. 🧠 **AI 负责思考**（分析、决策、验证）
3. 🔄 形成**协作循环**（截图→分析→执行→验证→重复）

**不需要额外的模型 API** —— AI 助手本身就是多模态大模型，直接看截图就能理解 UI、指导操作！

---

**开始使用吧！** 截图发给我，我来帮你分析如何操作 🚀
