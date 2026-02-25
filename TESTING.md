# 🧪 测试指南

## 测试 interactive_ai.py

### 前提条件

1. **确保 Freeform 已安装**
   ```bash
   open -a "Freeform"
   ```

2. **确保权限已授予**
   - Screen Recording: System Settings → Privacy & Security
   - Accessibility: 同上

3. **激活虚拟环境**
   ```bash
   cd ~/.openclaw/workspace/skills/macos-computer-use
   source .venv/bin/activate
   ```

---

### 测试步骤

**在终端中运行：**

```bash
python3 scripts/interactive_ai.py -t "在 Freeform 中画一个圆"
```

**脚本会提示：**

```
按回车开始...
```

**按回车后，脚本会：**

1. 自动截图
2. 显示截图路径
3. 提示你在聊天中发送 `image` 分析请求

**在聊天中发送：**

```
image /tmp/macos-ai-session/step-01-xxx.png "当前界面状态？下一步应该做什么？请返回 JSON 指令。"
```

**AI 会返回 JSON 指令，例如：**

```json
{"action": "hotkey", "params": {"keys": ["cmd", "n"]}, "reason": "新建画布"}
```

**将 JSON 粘贴到脚本提示处：**

```
请输入 AI 返回的指令 (JSON 格式，或 'q' 退出): {"action": "hotkey", "params": {"keys": ["cmd", "n"]}, "reason": "新建画布"}
```

**脚本执行后，会提示验证：**

```
操作成功了吗？(y/n/q): y
```

**输入 `y` 确认成功，继续下一步。**

---

### 完整测试流程示例

```bash
# 步骤 1: 新建画布
image /tmp/.../step-01.png "Freeform 界面，如何新建画布？"
→ {"action": "hotkey", "params": {"keys": ["cmd", "n"]}}

# 步骤 2: 选择画笔
image /tmp/.../step-02.png "画布打开了吗？如何选择画笔？"
→ {"action": "hotkey", "params": {"keys": ["cmd", "2"]}}

# 步骤 3: 画圆
image /tmp/.../step-03.png "画笔选中了吗？如何画圆？坐标？"
→ {"action": "drag", "params": {"from": [1400, 700], "to": [1600, 900]}}

# 步骤 4: 验证完成
image /tmp/.../step-04.png "圆画好了吗？"
→ {"action": "done", "params": {"message": "任务完成！"}}
```

---

### 验证成功标准

- ✅ AI 真正看到了截图（通过 `image` 工具）
- ✅ AI 返回了精准的坐标
- ✅ 每步操作后都验证了成功
- ✅ 最终画出了预期的图形

---

### 常见问题

**Q: 脚本说 EOFError**
A: 脚本需要交互式运行，不能在后台执行。确保在终端中直接运行。

**Q: AI 返回的不是 JSON 格式**
A: 请 AI 以 JSON 格式返回指令。可以这样说："请返回 JSON 格式的指令"。

**Q: 坐标点击不准**
A: 可能是 Retina 屏幕问题。请 AI 考虑屏幕分辨率。

**Q: 如何退出**
A: 输入 `q` 或按 Ctrl+C。

---

## 测试检查清单

- [ ] 脚本成功启动
- [ ] 截图成功保存
- [ ] 在聊天中使用 `image` 工具分析
- [ ] AI 返回 JSON 指令
- [ ] 粘贴指令后脚本正确执行
- [ ] 验证步骤正常工作
- [ ] 最终任务完成

**全部通过后，测试成功！** ✅
