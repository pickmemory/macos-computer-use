---
name: macos-computer-use
description: "Control the macOS UI — take screenshots, click, type, drag, find UI elements, and run AppleScript. Use when asked to interact with the desktop, open apps, fill forms, click buttons, or automate any visual/UI task on this Mac."
homepage: "https://github.com/siddkb/openclaw-skills"
metadata: {
  "clawdbot": {
    "emoji": "🖥️",
    "requires": {
      "bins": ["python3", "osascript"],
      "pip": ["pyautogui", "mss", "pillow", "atomacos"]
    }
  }
}
---

# macOS Computer Use

Gives OpenClaw full control of the macOS UI: screenshots, mouse, keyboard, UI element discovery, and AppleScript. Pairs with Claude's vision to create a complete computer-use loop.

## Setup (run once)

```bash
~/.openclaw/workspace/skills/macos-computer-use/scripts/setup.sh
```

This installs Python dependencies and guides you through granting the two required macOS permissions:
- **Accessibility** → System Settings > Privacy & Security > Accessibility → add your terminal / OpenClaw
- **Screen Recording** → System Settings > Privacy & Security > Screen Recording → add your terminal / OpenClaw

## Quick Reference

| Goal | Script | Example |
|------|--------|---------|
| See the screen | `screenshot.py` | `python3 screenshot.py` |
| Capture a window | `screenshot.py` | `python3 screenshot.py --window "Safari"` |
| Capture a region | `screenshot.py` | `python3 screenshot.py --region 0 0 800 600` |
| Left-click | `mouse.py click` | `python3 mouse.py click 500 300` |
| Right-click | `mouse.py click` | `python3 mouse.py click 500 300 --button right` |
| Double-click | `mouse.py click` | `python3 mouse.py click 500 300 --double` |
| Move mouse | `mouse.py move` | `python3 mouse.py move 200 400` |
| Scroll | `mouse.py scroll` | `python3 mouse.py scroll 500 300 --dy -5` |
| Drag | `mouse.py drag` | `python3 mouse.py drag 100 200 400 200` |
| Type text | `keyboard.py type` | `python3 keyboard.py type "Hello world"` |
| Press a key | `keyboard.py press` | `python3 keyboard.py press return` |
| Keyboard shortcut | `keyboard.py hotkey` | `python3 keyboard.py hotkey cmd shift s` |
| Find a button | `find_ui.py` | `python3 find_ui.py --app "Safari" --role AXButton --title "Back"` |
| List UI elements | `find_ui.py` | `python3 find_ui.py --app "Finder"` |
| Run AppleScript | `applescript.py` | `python3 applescript.py -e 'tell app "Safari" to activate'` |

## Typical Computer-Use Loop

1. `screenshot.py` → examine the screen (Claude sees the image)
2. Identify target coordinates or UI element
3. `mouse.py click X Y` or `keyboard.py type "..."` to act
4. `screenshot.py` again to verify result
5. Repeat until task is complete

## Script Reference

### screenshot.py
```
python3 screenshot.py [--output PATH] [--window TITLE] [--region X Y W H]
```
- Saves PNG and prints the file path to stdout
- Default: full screen saved to `/tmp/openclaw-screenshot-<timestamp>.png`
- `--window` matches by window title substring (case-insensitive)
- `--region` crops to pixel rectangle: x y width height

### mouse.py
```
python3 mouse.py <subcommand> [args]

  click X Y [--button left|right|middle] [--double]
  move  X Y [--duration SECS]
  scroll X Y [--dx CLICKS] [--dy CLICKS]
  drag  X1 Y1 X2 Y2 [--duration SECS]
```
- Coordinates are screen pixels (0,0 = top-left)
- Scroll: negative dy scrolls down, positive scrolls up

### keyboard.py
```
python3 keyboard.py <subcommand> [args]

  type   TEXT [--interval SECS]    # Type a string character by character
  press  KEY [KEY ...]             # Press one or more keys in sequence
  hotkey KEY [KEY ...]             # Press keys simultaneously (e.g. cmd shift s)
```
- Key names follow pyautogui conventions: `return`, `escape`, `tab`, `space`, `cmd`, `ctrl`, `shift`, `alt`, `delete`, `up`, `down`, `left`, `right`, `f1`..`f12`

### find_ui.py
```
python3 find_ui.py [--app APP_NAME] [--role ROLE] [--title TITLE] [--label LABEL] [--limit N]
```
- Returns JSON array of matching elements with: title, role, label, position {x,y}, size {w,h}
- Use position center to compute click coordinates
- Common roles: `AXButton`, `AXTextField`, `AXStaticText`, `AXMenuItem`, `AXWindow`, `AXCheckBox`, `AXLink`
- Requires `atomacos`: `pip install atomacos`

### applescript.py
```
python3 applescript.py -e 'AppleScript expression'
python3 applescript.py -f script.applescript
```
- Runs via `osascript`, returns stdout
- Useful for app-level control, menu commands, file operations

## Safety Notes

- **Mouse/keyboard actions are immediate** — there is no undo
- Always take a screenshot before and after actions to verify
- Prefer `find_ui.py` over hard-coded coordinates when possible — coordinates shift if windows move
- For destructive actions (file deletion, form submission, purchases), confirm with the user first
- `pyautogui` has a failsafe: moving the mouse to the top-left corner (0,0) raises an exception and halts execution

## Permissions Troubleshooting

If screenshot returns a black image → Screen Recording not granted
If mouse/keyboard does nothing → Accessibility not granted
Run `setup.sh` to re-check permission status.
