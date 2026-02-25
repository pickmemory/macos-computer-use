#!/usr/bin/env python3
"""
AI 交互式指导模式 - 强制每步都用 image 工具分析

核心流程：
1. 截图
2. 显示截图路径，提示用户在聊天中使用 image 工具分析
3. 等待用户输入 AI 返回的指令
4. 执行指令
5. 验证（再次截图）
6. 循环直到完成

这是真正的 Fail Fast 模式 - 每步都必须验证！
"""

import argparse
import json
import subprocess
import time
from pathlib import Path

# 配置
SCREENSHOT_DIR = Path("/tmp/macos-ai-session")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

SCRIPTS_DIR = Path(__file__).parent


def take_screenshot(name: str) -> str:
    """截图并返回路径"""
    ts = int(time.time())
    path = SCREENSHOT_DIR / f"{name}-{ts}.png"
    
    subprocess.run(
        ['/usr/sbin/screencapture', '-x', str(path)],
        capture_output=True,
        check=True
    )
    print(f"\n📸 截图已保存：{path}")
    return str(path)


def get_screen_info() -> str:
    """获取屏幕分辨率信息"""
    try:
        result = subprocess.run(
            ['/usr/sbin/system_profiler', 'SPDisplaysDataType'],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.split('\n'):
            if 'Resolution' in line:
                # 提取分辨率，如 "Resolution: 2560 x 1600 Retina"
                return line.strip()
    except Exception:
        pass
    return "屏幕信息未知"


def analyze_with_image(screenshot_path: str, task: str) -> dict:
    """
    提示用户在聊天中使用 image 工具分析
    
    这是核心函数 - 强制 AI 真正看到截图
    """
    screen_info = get_screen_info()
    
    print(f"\n{'='*70}")
    print(f"🧠 AI 分析步骤")
    print(f"{'='*70}")
    print(f"\n📋 任务：{task}")
    print(f"\n🖥️  屏幕：{screen_info}")
    print(f"⚠️  坐标基于实际截图像素（Retina 2x 缩放）")
    print(f"\n📸 截图：{screenshot_path}")
    print(f"\n{'='*70}")
    print(f"⚠️  请在聊天中发送以下内容（使用 image 工具，不是 read！）:")
    print(f"{'='*70}")
    print()
    print(f'image {screenshot_path} "{task} 屏幕：{screen_info}。请返回基于截图实际像素的坐标（Retina 2x）。"}')
    print()
    print(f"{'='*70}")
    print(f"⏳ 等待 AI 分析并返回指令...")
    print(f"{'='*70}")
    print()
    print(f"AI 应该返回类似：")
    print(f'{{"action": "click", "params": {{"x": 2880, "y": 200}}, "reason": "点击画笔工具"}}')
    print(f'注意：坐标是实际像素值（2560x1600 Retina = 5120x3200 实际）')
    print()
    
    # 等待用户输入指令
    while True:
        user_input = input("请输入 AI 返回的指令 (JSON 格式，或 'q' 退出): ").strip()
        
        if user_input.lower() == 'q':
            return {"action": "done", "params": {"message": "用户退出"}}
        
        try:
            instruction = json.loads(user_input)
            
            # 验证指令格式
            if "action" not in instruction:
                print("❌ 指令缺少 'action' 字段，请重新输入")
                continue
            
            print(f"✅ 收到指令：{instruction.get('action')}")
            return instruction
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败：{e}")
            print("请重新输入正确的 JSON 格式")


def execute_action(action_type: str, params: dict) -> bool:
    """执行操作"""
    print(f"\n{'='*70}")
    print(f"🤖 执行：{action_type}")
    print(f"{'='*70}")
    
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
            message = params.get("message", "任务完成")
            print(f"   ✅ {message}")
            return True
            
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ 执行失败：{e}")
        print(f"   请检查坐标是否正确，或应用是否有响应")
        return False
    except Exception as e:
        print(f"   ❌ 未知错误：{e}")
        return False


def verify_step(step_name: str, check_question: str) -> bool:
    """
    验证步骤是否成功
    
    用户需要在聊天中用 image 工具验证
    """
    screenshot_path = take_screenshot(f"{step_name}-verify")
    
    print(f"\n{'='*70}")
    print(f"✅ 验证步骤")
    print(f"{'='*70}")
    print(f"\n📸 截图：{screenshot_path}")
    print(f"\n{'='*70}")
    print(f"⚠️  请在聊天中发送：")
    print(f"{'='*70}")
    print()
    print(f'image {screenshot_path} "{check_question}"')
    print()
    print(f"{'='*70}")
    
    while True:
        user_input = input("操作成功了吗？(y/n/q): ").strip().lower()
        
        if user_input == 'y':
            print("✅ 验证通过，继续下一步")
            return True
        elif user_input == 'n':
            print("❌ 验证失败，请调整指令")
            return False
        elif user_input == 'q':
            print("⚠️  用户退出")
            return False
        else:
            print("请输入 y/n/q")


def run_interactive_loop(task: str, max_steps: int = 20):
    """
    交互式 AI 协作循环
    
    每步：
    1. 截图
    2. 用户在聊天中使用 image 工具分析
    3. 输入 AI 返回的指令
    4. 执行
    5. 验证
    6. 循环直到完成
    """
    print(f"\n{'='*70}")
    print(f"🚀 AI 交互式协作任务：{task}")
    print(f"📁 截图目录：{SCREENSHOT_DIR}")
    print(f"{'='*70}")
    print(f"\n📋 工作流程:")
    print(f"1. 脚本自动截图")
    print(f"2. 在聊天中使用 `image` 工具分析截图（不要用 `read`！）")
    print(f"3. AI 返回指令后，输入 JSON 格式指令")
    print(f"4. 脚本执行指令")
    print(f"5. 验证是否成功")
    print(f"6. 循环直到任务完成")
    print(f"\n⚡ Fail Fast: 每步都必须验证，失败立即调整！")
    print(f"\n按 Ctrl+C 随时退出")
    input("按回车开始...")
    
    step = 0
    
    try:
        while step < max_steps:
            step += 1
            step_name = f"step-{step:02d}"
            
            print(f"\n{'='*70}")
            print(f"📍 步骤 {step}/{max_steps}")
            print(f"{'='*70}")
            
            # 1. 截图
            screenshot_path = take_screenshot(step_name)
            
            # 2. AI 分析（关键：用户必须在聊天中使用 image 工具）
            instruction = analyze_with_image(
                screenshot_path=screenshot_path,
                task=f"当前界面状态？下一步应该做什么？请返回 JSON 指令。"
            )
            
            # 3. 执行操作
            done = execute_action(instruction.get('action'), instruction.get('params', {}))
            if done or instruction.get('action') == 'done':
                print(f"\n🎉 任务完成!")
                break
            
            # 4. 验证
            verify_question = instruction.get('reason', '操作成功了吗？')
            success = verify_step(step_name, verify_question)
            
            if not success:
                print(f"\n⚠️  步骤 {step} 失败，请重新分析")
                continue
            
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
        description="AI 交互式指导模式 - 强制每步都用 image 工具分析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -t "在 Freeform 中画一个圆"
  %(prog)s -t "关闭所有窗口" --steps 10

重要:
  - 截图后，必须在聊天中使用 `image` 工具分析（不要用 `read`！）
  - AI 返回指令后，输入 JSON 格式指令
  - 每步都必须验证，遵循 Fail Fast 原则
        """
    )
    parser.add_argument("--task", "-t", required=True, help="任务描述")
    parser.add_argument("--steps", "-s", type=int, default=20, help="最大步骤数")
    
    args = parser.parse_args()
    
    run_interactive_loop(args.task, max_steps=args.steps)


if __name__ == "__main__":
    main()
