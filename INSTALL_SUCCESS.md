# ✅ macos-computer-use 安装成功！

## 安装状态

- ✅ 代码已克隆：`~/.openclaw/workspace/skills/macos-computer-use`
- ✅ 依赖已安装：虚拟环境 `.venv/` 已创建
- ✅ 配置已更新：`openclaw.json` 中已启用技能
- ✅ 基础测试通过：截图、UI 元素查找正常工作

---

## 核心脚本

| 脚本 | 功能 | 示例 |
|------|------|------|
| `screenshot.py` | 截图 | `python3 scripts/screenshot.py --output /tmp/screen.png` |
| `mouse.py` | 鼠标控制 | `python3 scripts/mouse.py click 500 300` |
| `keyboard.py` | 键盘控制 | `python3 scripts/keyboard.py type "Hello"` |
| `find_ui.py` | 查找 UI 元素 | `python3 scripts/find_ui.py --role AXButton --title "登录"` |
| `applescript.py` | 执行 AppleScript | `python3 scripts/applescript.py -e 'tell app "Safari" to activate'` |

---

## 快速开始

### 1. 截图（看屏幕）

```bash
cd ~/.openclaw/workspace/skills/macos-computer-use
source .venv/bin/activate

# 全屏截图
python3 scripts/screenshot.py

# 指定窗口
python3 scripts/screenshot.py --window "Chrome"

# 指定区域 (x y width height)
python3 scripts/screenshot.py --region 0 0 800 600
```

### 2. 查找 UI 元素（推荐方式）

```bash
# 查找所有按钮
python3 scripts/find_ui.py --role AXButton

# 查找特定应用的按钮
python3 scripts/find_ui.py --app "Google Chrome" --role AXButton

# 查找带标题的按钮
python3 scripts/find_ui.py --role AXButton --title "Back"

# 返回 JSON，包含 center.x / center.y 用于点击
```

### 3. 点击

```bash
# 直接坐标点击
python3 scripts/mouse.py click 500 300

# 右键点击
python3 scripts/mouse.py click 500 300 --button right

# 双击
python3 scripts/mouse.py click 500 300 --double

# 移动鼠标（不点击）
python3 scripts/mouse.py move 200 400

# 拖拽
python3 scripts/mouse.py drag 100 100 400 400

# 滚动
python3 scripts/mouse.py scroll 500 300 --dy -5
```

### 4. 键盘输入

```bash
# 输入文本
python3 scripts/keyboard.py type "Hello World"

# 按键
python3 scripts/keyboard.py press return
python3 scripts/keyboard.py press escape

# 快捷键
python3 scripts/keyboard.py hotkey cmd c      # 复制
python3 scripts/keyboard.py hotkey cmd v      # 粘贴
python3 scripts/keyboard.py hotkey cmd shift s  # 另存为
```

---

## 完整的 Computer-Use 循环

```bash
# 1. 截图查看当前状态
python3 scripts/screenshot.py --output /tmp/before.png

# 2. 查找目标 UI 元素
python3 scripts/find_ui.py --app "Google Chrome" --role AXButton --title "登录"
# 返回：{"center": {"x": 94, "y": 64}}

# 3. 点击
python3 scripts/mouse.py click 94 64

# 4. 截图验证
python3 scripts/screenshot.py --output /tmp/after.png
```

---

## 权限要求

需要两个 macOS 权限：

1. **辅助功能**（Accessibility）
   - 系统设置 → 隐私与安全性 → 辅助功能
   - 添加终端或 OpenClaw

2. **屏幕录制**（Screen Recording）
   - 系统设置 → 隐私与安全性 → 屏幕录制
   - 添加终端或 OpenClaw

---

## 故障排除

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| 截图是黑色 | 屏幕录制权限未授予 | 系统设置 → 隐私 → 屏幕录制 |
| 鼠标/键盘无反应 | 辅助功能权限未授予 | 系统设置 → 隐私 → 辅助功能 |
| find_ui 返回空 | 应用名称不匹配 | 用精确的应用名（查看活动监视器） |

---

## 与 mac-vision-auto 的对比

| 特性 | mac-vision-auto | macos-computer-use |
|------|-----------------|-------------------|
| 元素识别 | ❌ 仅坐标/颜色 | ✅ Accessibility API |
| 坐标系统 | ⚠️ 手动转换 (÷2) | ✅ 自动 (返回 center) |
| 可靠性 | ⚠️ 依赖截图精度 | ✅ 系统级 API |
| 推荐度 | ⚠️ 备用 | ✅ 首选 |

---

## 下一步

1. **测试点击准确性** - 找一个已知位置的按钮测试
2. **集成到 OpenClaw** - 重启 Gateway 让技能生效
3. **开始使用** - 让 AI 帮你自动化桌面任务

需要我帮你测试具体功能吗？🖥️
