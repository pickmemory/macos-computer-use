#!/usr/bin/env python3
"""
Mouse control for macOS.

Usage:
  mouse.py click  X Y [--button left|right|middle] [--double]
  mouse.py move   X Y [--duration SECS]
  mouse.py scroll X Y [--dx CLICKS] [--dy CLICKS]
  mouse.py drag   X1 Y1 X2 Y2 [--duration SECS]

Coordinates are screen pixels (0,0 = top-left corner).
Scroll: --dy negative = scroll down, positive = scroll up.
Requires Accessibility permission.
"""

import argparse
import sys
import time

try:
    import pyautogui
    pyautogui.FAILSAFE = True   # Move mouse to (0,0) to abort
    pyautogui.PAUSE = 0.05      # Small delay between actions for stability
except ImportError:
    sys.exit("Error: pyautogui not installed. Run setup.sh first.")


def cmd_click(args):
    if args.double:
        pyautogui.doubleClick(args.X, args.Y, button=args.button)
    else:
        pyautogui.click(args.X, args.Y, button=args.button)
    print(f"clicked ({args.X}, {args.Y}) button={args.button} double={args.double}")


def cmd_move(args):
    pyautogui.moveTo(args.X, args.Y, duration=args.duration)
    print(f"moved to ({args.X}, {args.Y})")


def cmd_scroll(args):
    pyautogui.moveTo(args.X, args.Y)
    if args.dx:
        pyautogui.hscroll(args.dx)
    if args.dy:
        pyautogui.scroll(args.dy)
    print(f"scrolled at ({args.X}, {args.Y}) dx={args.dx} dy={args.dy}")


def cmd_drag(args):
    pyautogui.moveTo(args.X1, args.Y1, duration=0.3)
    pyautogui.dragTo(args.X2, args.Y2, duration=args.duration, button="left")
    print(f"dragged ({args.X1},{args.Y1}) → ({args.X2},{args.Y2})")


def main():
    parser = argparse.ArgumentParser(description="Mouse control")
    sub = parser.add_subparsers(dest="command", required=True)

    # click
    p_click = sub.add_parser("click", help="Click at X Y")
    p_click.add_argument("X", type=int)
    p_click.add_argument("Y", type=int)
    p_click.add_argument("--button", choices=["left", "right", "middle"], default="left")
    p_click.add_argument("--double", action="store_true")

    # move
    p_move = sub.add_parser("move", help="Move mouse to X Y")
    p_move.add_argument("X", type=int)
    p_move.add_argument("Y", type=int)
    p_move.add_argument("--duration", type=float, default=0.3)

    # scroll
    p_scroll = sub.add_parser("scroll", help="Scroll at X Y")
    p_scroll.add_argument("X", type=int)
    p_scroll.add_argument("Y", type=int)
    p_scroll.add_argument("--dx", type=int, default=0, help="Horizontal scroll clicks")
    p_scroll.add_argument("--dy", type=int, default=0, help="Vertical scroll clicks (negative=down)")

    # drag
    p_drag = sub.add_parser("drag", help="Drag from X1 Y1 to X2 Y2")
    p_drag.add_argument("X1", type=int)
    p_drag.add_argument("Y1", type=int)
    p_drag.add_argument("X2", type=int)
    p_drag.add_argument("Y2", type=int)
    p_drag.add_argument("--duration", type=float, default=0.5)

    args = parser.parse_args()
    dispatch = {"click": cmd_click, "move": cmd_move, "scroll": cmd_scroll, "drag": cmd_drag}
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
