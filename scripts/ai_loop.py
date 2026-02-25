#!/usr/bin/env python3
"""
AI Loop - 真正的 AI 增强版 (v2)

核心架构变更：
- 不再尝试在脚本内调用 AI
- 截图后输出路径，等待用户在聊天中使用 `image` 工具分析
- AI 返回指令后，脚本读取指令文件并执行
- 形成：截图 → image 工具分析 → 执行 → 验证 的循环

使用流程：
1. 运行此脚本，传入任务描述
2. 脚本截图并等待
3. 用户在聊天中看到截图路径，使用 `image` 工具分析
4. AI 返回指令，写入指令文件
5. 脚本读取指令并执行
6. 循环直到任务完成
"""

import argparse
import json
import subprocess
import time
import sys
from pathlib import Path
from datetime import datetime

# 配置
SCREENSHOT_DIR = Path("~/Projects/macos-ai-loop").expanduser()
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

SCRIPTS_DIR = Path(__file__).parent

# 指令文件路径
INSTRUCTION_FILE = SCREENSHOT_DIR / "current-instruction.json"


def take_screenshot(name: str) -> str:
    """截图并返回路径"""
    ts = int(time.time())
    path = SCREENSHOT_DIR / f"{name}-{ts}.png"
    
    # 使用系统 screencapture 命令
    subprocess.run(
        ['screencapture', '-x', str(path)],
        capture_output=True,
        check=True
    )
    print(f"\n📸 截图已保存：{path}")
    return str(path)


def execute_action(action_type: str, params: dict) -> bool:
    """执行操作"""
    print(f"\n🤖 执行：{action_type}")
    
    try:
        if action_type == "click":
            x, y = params["x"], params["y"]
            subprocess.run(
                ['python3', str(SCRIPTS_DIR / 'mouse.py'), 'click', str(x), str(y)],
                capture_output=True,
                check=True
            )
            print(f"   🖱️  点击：({x}, {y})")
            
        elif action_type == "drag":
            x1, y1 = params["from"]
            x2, y2 = params["to"]
            duration = params.get("duration", 0.5)
            subprocess.run(
                ['python3', str(SCRIPTS_DIR / 'mouse.py'), 'drag', 
                 str(x1), str(y1), str(x2), str(y2), '--duration', str(duration)],
                capture_output=True,
                check=True
            )
            print(f"   🖱️  拖拽：({x1}, {y1}) → ({x2}, {y2})")
            
        elif action_type == "hotkey":
            keys = params["keys"]
            subprocess.run(
                ['python3', str(SCRIPTS_DIR / 'keyboard.py'), 'hotkey'] + keys,
                capture_output=True,
                check=True
            )
            print(f"   ⌨️  快捷键：{'+'.join(keys)}")
            
        elif action_type == "type":
            text = params["text"]
            subprocess.run(
                ['python3', str(SCRIPTS_DIR / 'keyboard.py'), 'type', text],
                capture_output=True,
                check=True
            )
            print(f"   ⌨️  输入：{text[:50]}...")
            
        elif action_type == "wait":
            seconds = params.get("seconds", 1)
            print(f"   ⏳ 等待 {seconds} 秒")
            time.sleep(seconds)
            
        elif action_type == "done":
            print(f"   ✅ {params.get('message', '任务完成')}")
            return True
            
        return False
        
    except Exception as e:
        print(f"   ❌ 执行失败：{e}")
        return False


def wait_for_instruction(timeout: int = 300) -> dict:
    """
    等待 AI 指令
    
    用户需要在聊天中：
    1. 使用 `image` 工具分析截图
    2. 将 AI 返回的指令写入 INSTRUCTION_FILE
    
    指令格式:
    {
        "action": "click|drag|hotkey|type|wait|done",
        "params": {...},
        "reason": "分析理由"
    }
    """
    print(f"\n⏳ 等待 AI 指令... (timeout: {timeout}s)")
    print(f"   请在聊天中使用 `image` 工具分析截图，然后写入指令到:")
    print(f"   {INSTRUCTION_FILE}")
    print(f"\n   指令格式示例:")
    print(f'   {{"action": "click", "params": {{"x": 500, "y": 300}}, "reason": "点击按钮"}}')
    print(f'   或 {{"action": "done", "params": {{"message": "任务完成"}}}}')
    
    start_time = time.time()
    
    # 如果指令文件已存在，先删除
    if INSTRUCTION_FILE.exists():
        INSTRUCTION_FILE.unlink()
    
    while time.time() - start_time < timeout:
        time.sleep(1)
        if INSTRUCTION_FILE.exists():
            try:
                with open(INSTRUCTION_FILE, 'r', encoding='utf-8') as f:
                    instruction = json.load(f)
                print(f"\n✅ 收到 AI 指令!")
                return instruction
            except Exception as e:
                print(f"   读取指令失败：{e}")
                INSTRUCTION_FILE.unlink()
    
    raise TimeoutError(f"等待 AI 指令超时 ({timeout}s)")


def run_ai_loop(task: str, max_steps: int = 20, timeout: int = 300):
    """
    AI 协作循环
    
    每步：
    1. 截图
    2. 等待用户使用 `image` 工具分析并写入指令
    3. 读取指令并执行
    4. 验证（再次截图）
    5. 循环直到完成
    """
    print(f"\n{'='*70}")
    print(f"🚀 AI 协作任务：{task}")
    print(f"📁 截图目录：{SCREENSHOT_DIR}")
    print(f"📝 指令文件：{INSTRUCTION_FILE}")
    print(f"{'='*70}")
    print(f"\n📋 使用说明:")
    print(f"1. 脚本会自动截图")
    print(f"2. 在聊天中使用 `image` 工具分析截图（不要用 `read`！）")
    print(f"3. AI 返回指令后，脚本会自动读取并执行")
    print(f"4. 循环直到任务完成")
    print(f"\n按 Ctrl+C 随时退出")
    
    step = 0
    prev_screenshot = None
    
    try:
        while step < max_steps:
            step += 1
            step_name = f"step-{step:02d}"
            
            print(f"\n{'='*70}")
            print(f"📍 步骤 {step}/{max_steps}")
            print(f"{'='*70}")
            
            # 1. 截图
            screenshot_path = take_screenshot(step_name)
            
            # 2. 等待 AI 指令（用户使用 image 工具分析）
            try:
                instruction = wait_for_instruction(timeout=timeout)
            except TimeoutError as e:
                print(f"\n❌ {e}")
                break
            
            print(f"\n📋 AI 指令:")
            print(f"   动作：{instruction.get('action')}")
            print(f"   理由：{instruction.get('reason', '无')}")
            
            # 3. 执行操作
            done = execute_action(instruction.get('action'), instruction.get('params', {}))
            if done:
                print(f"\n🎉 任务完成!")
                break
            
            # 4. 操作后截图验证
            after_path = take_screenshot(f"{step_name}-after")
            print(f"\n✅ 操作完成，验证截图：{after_path}")
            
            prev_screenshot = after_path
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print(f"\n\n⚠️  用户中断")
    
    # 总结
    print(f"\n{'='*70}")
    print(f"📊 任务总结")
    print(f"{'='*70}")
    print(f"任务：{task}")
    print(f"执行步骤：{step}")
    print(f"截图保存：{SCREENSHOT_DIR}")
    print(f"{'='*70}")


def main():
    parser = argparse.ArgumentParser(
        description="AI 协作循环 - 使用 `image` 工具分析截图",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -t "在 Freeform 中画一个圆"
  %(prog)s -t "关闭所有窗口" --steps 10
  %(prog)s -t "探索系统设置" --timeout 600

重要：
  - 截图后，在聊天中使用 `image` 工具分析（不要用 `read`！）
  - AI 返回指令后，写入到指令文件，脚本会自动执行
        """
    )
    parser.add_argument("--task", "-t", required=True, help="任务描述")
    parser.add_argument("--steps", "-s", type=int, default=20, help="最大步骤数")
    parser.add_argument("--timeout", type=int, default=300, help="等待指令超时时间（秒）")
    
    args = parser.parse_args()
    
    run_ai_loop(args.task, max_steps=args.steps, timeout=args.timeout)


if __name__ == "__main__":
    main()
