#!/usr/bin/env python3
"""
Keyboard control for macOS.

Usage:
  keyboard.py type   TEXT [--interval SECS]
  keyboard.py press  KEY [KEY ...]
  keyboard.py hotkey KEY [KEY ...]

Key names (pyautogui): return, escape, tab, space, backspace, delete,
  cmd, ctrl, shift, alt/option, fn, up, down, left, right,
  home, end, pageup, pagedown, f1..f12, a..z, 0..9

Examples:
  keyboard.py type "Hello, world!"
  keyboard.py press return
  keyboard.py press escape
  keyboard.py hotkey cmd c          # Copy
  keyboard.py hotkey cmd shift s    # Save As
  keyboard.py hotkey cmd alt esc    # Force Quit dialog

Requires Accessibility permission.
"""

import argparse
import sys

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.05
except ImportError:
    sys.exit("Error: pyautogui not installed. Run setup.sh first.")


def cmd_type(args):
    pyautogui.typewrite(args.text, interval=args.interval)
    # typewrite doesn't handle unicode well; use pyperclip for non-ASCII
    print(f"typed: {args.text!r}")


def cmd_press(args):
    for key in args.keys:
        pyautogui.press(key)
    print(f"pressed: {' '.join(args.keys)}")


def cmd_hotkey(args):
    pyautogui.hotkey(*args.keys)
    print(f"hotkey: {'+'.join(args.keys)}")


def main():
    parser = argparse.ArgumentParser(description="Keyboard control")
    sub = parser.add_subparsers(dest="command", required=True)

    p_type = sub.add_parser("type", help="Type a string")
    p_type.add_argument("text")
    p_type.add_argument("--interval", type=float, default=0.03,
                        help="Seconds between keystrokes (default 0.03)")

    p_press = sub.add_parser("press", help="Press key(s) in sequence")
    p_press.add_argument("keys", nargs="+")

    p_hotkey = sub.add_parser("hotkey", help="Press keys simultaneously")
    p_hotkey.add_argument("keys", nargs="+")

    args = parser.parse_args()
    dispatch = {"type": cmd_type, "press": cmd_press, "hotkey": cmd_hotkey}
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
