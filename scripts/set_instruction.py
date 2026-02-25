#!/usr/bin/env python3
"""
快速写入 AI 指令到当前指令文件

用法:
  set_instruction.py '{"action":"click","params":{"x":500,"y":300}}'
  set_instruction.py click 500 300
  set_instruction.py done "任务完成"
"""

import json
import sys
from pathlib import Path

SCREENSHOT_DIR = Path("~/Projects/macos-ai-loop").expanduser()
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
INSTRUCTION_FILE = SCREENSHOT_DIR / "current-instruction.json"


def write_instruction(instruction: dict):
    """写入指令文件"""
    with open(INSTRUCTION_FILE, 'w', encoding='utf-8') as f:
        json.dump(instruction, f, ensure_ascii=False, indent=2)
    print(f"✅ 指令已写入：{INSTRUCTION_FILE}")
    print(f"   内容：{json.dumps(instruction, ensure_ascii=False)}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    # 模式 1: 直接传入 JSON
    if sys.argv[1].startswith('{'):
        try:
            instruction = json.loads(sys.argv[1])
            write_instruction(instruction)
            return
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败：{e}")
            sys.exit(1)
    
    # 模式 2: 快捷命令
    action = sys.argv[1]
    
    if action == "click" and len(sys.argv) >= 4:
        x, y = int(sys.argv[2]), int(sys.argv[3])
        reason = sys.argv[4] if len(sys.argv) > 4 else "点击"
        write_instruction({
            "action": "click",
            "params": {"x": x, "y": y},
            "reason": reason
        })
    
    elif action == "drag" and len(sys.argv) >= 6:
        x1, y1 = int(sys.argv[2]), int(sys.argv[3])
        x2, y2 = int(sys.argv[4]), int(sys.argv[5])
        reason = sys.argv[6] if len(sys.argv) > 6 else "拖拽"
        write_instruction({
            "action": "drag",
            "params": {"from": [x1, y1], "to": [x2, y2]},
            "reason": reason
        })
    
    elif action == "hotkey" and len(sys.argv) >= 3:
        keys = sys.argv[2:]
        write_instruction({
            "action": "hotkey",
            "params": {"keys": keys},
            "reason": f"快捷键：{'+'.join(keys)}"
        })
    
    elif action == "type" and len(sys.argv) >= 3:
        text = sys.argv[2]
        write_instruction({
            "action": "type",
            "params": {"text": text},
            "reason": "输入文字"
        })
    
    elif action == "wait" and len(sys.argv) >= 3:
        seconds = int(sys.argv[2])
        write_instruction({
            "action": "wait",
            "params": {"seconds": seconds},
            "reason": "等待"
        })
    
    elif action == "done":
        message = sys.argv[2] if len(sys.argv) > 2 else "任务完成"
        write_instruction({
            "action": "done",
            "params": {"message": message},
            "reason": "完成任务"
        })
    
    else:
        print(f"❌ 未知命令或参数不足：{sys.argv}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
