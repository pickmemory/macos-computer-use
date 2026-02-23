# macos-computer-use

> A production-ready [OpenClaw](https://openclaw.ai) skill for macOS UI automation — built by [Noesis.tech](https://noesis.tech)

Give your AI agent eyes and hands on macOS. Screenshot the screen, click, type, discover UI elements via the Accessibility API, and run AppleScript — all from a clean, composable script interface.

Pairs with Claude's vision to create a complete **see → decide → act** computer-use loop.

---

## Capabilities

| Script | What it does |
|--------|-------------|
| `screenshot.py` | Capture full screen, a named window, or a pixel region |
| `mouse.py` | Click, double-click, right-click, drag, scroll, move |
| `keyboard.py` | Type text, press keys, fire keyboard shortcuts |
| `find_ui.py` | Discover UI elements by role/title via the macOS Accessibility API |
| `applescript.py` | Run any AppleScript expression or file via `osascript` |

## Requirements

- macOS 12+
- Python 3.9+
- Two macOS permissions (see [Setup](#setup)):
  - **Accessibility** — mouse, keyboard, and UI element control
  - **Screen Recording** — screenshots

## Installation

### Via ClawHub
```bash
clawdhub install macos-computer-use
```

### Manual
```bash
git clone https://github.com/siddkb/macos-computer-use \
  ~/.openclaw/workspace/skills/macos-computer-use
```

Add to `~/.openclaw/openclaw.json`:
```json
"skills": {
  "entries": {
    "macos-computer-use": { "enabled": true }
  }
}
```

## Setup

Run once to install Python dependencies and check permission status:

```bash
~/.openclaw/workspace/skills/macos-computer-use/scripts/setup.sh
```

Then grant the two required permissions:

- **System Settings → Privacy & Security → Accessibility** → add your terminal or OpenClaw binary
- **System Settings → Privacy & Security → Screen Recording** → add your terminal or OpenClaw binary

## Usage

### Screenshot
```bash
python3 scripts/screenshot.py                          # Full screen
python3 scripts/screenshot.py --window "Safari"        # Specific window
python3 scripts/screenshot.py --region 0 0 1280 800    # Pixel region (x y w h)
python3 scripts/screenshot.py --output ~/Desktop/capture.png
```

### Mouse
```bash
python3 scripts/mouse.py click 500 300                 # Left click
python3 scripts/mouse.py click 500 300 --button right  # Right-click
python3 scripts/mouse.py click 500 300 --double        # Double-click
python3 scripts/mouse.py drag 100 200 400 200          # Drag
python3 scripts/mouse.py scroll 500 300 --dy -5        # Scroll down
```

### Keyboard
```bash
python3 scripts/keyboard.py type "Hello, world!"
python3 scripts/keyboard.py press return
python3 scripts/keyboard.py hotkey cmd shift s         # Save As
python3 scripts/keyboard.py hotkey cmd c               # Copy
```

### Find UI Elements
```bash
python3 scripts/find_ui.py --app Safari --role AXButton           # All buttons
python3 scripts/find_ui.py --app Safari --role AXButton --title "Back"  # Specific button
python3 scripts/find_ui.py --role AXTextField                     # Frontmost app fields
```

Returns JSON with coordinates ready to pass to `mouse.py`:
```json
[
  {
    "title": "Back",
    "role": "AXButton",
    "label": "Back",
    "position": {"x": 80, "y": 50},
    "size": {"w": 28, "h": 28},
    "center": {"x": 94, "y": 64}
  }
]
```

Prefer `center.x` / `center.y` as click targets — more reliable than hard-coded coordinates.

### AppleScript
```bash
python3 scripts/applescript.py -e 'tell application "Safari" to activate'
python3 scripts/applescript.py -e 'tell application "Safari" to open location "https://example.com"'
python3 scripts/applescript.py -f my-script.applescript
```

## The Computer-Use Loop

```
1. screenshot.py          →  agent sees current screen state
2. find_ui.py             →  locate element by role + title (preferred)
   — or —
   analyze screenshot     →  identify pixel coordinates visually
3. mouse.py / keyboard.py →  execute the action
4. screenshot.py          →  verify result
5. repeat until done
```

## Safety

- Mouse and keyboard actions execute immediately — there is no undo
- `pyautogui` failsafe: moving the mouse to corner `(0, 0)` raises an exception and halts execution
- Always prefer `find_ui.py` over pixel coordinates — windows move and resize
- For destructive or irreversible actions, confirm with the user before proceeding

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Screenshot is black | Screen Recording not granted | System Settings → Privacy & Security → Screen Recording |
| Mouse/keyboard does nothing | Accessibility not granted | System Settings → Privacy & Security → Accessibility |
| `atomacos` import error | Package not installed | Run `scripts/setup.sh` |
| `find_ui.py` returns empty | App name mismatch | Use the exact name shown in Activity Monitor |

## Roadmap

- `ocr.py` — extract text from screenshots using Apple's Vision framework
- `window.py` — list, focus, and resize windows
- `clipboard.py` — read and write the clipboard
- `notify.py` — post macOS notifications
- Hook integration for event-driven triggers

Contributions welcome — open an issue or PR.

---

## About Noesis.tech

[Noesis.tech](https://noesis.tech) is a product and AI agency. We design and build software products, AI systems, and internal tools for startups and growth-stage companies.

This skill is part of our ongoing work on AI agent infrastructure. We open-source tools we find useful in the hope that others do too.

**Want to work with us or join our team?** Reach out at [noesis.tech](https://noesis.tech).

## License

MIT © [Siddharth Bhansali](https://noesis.tech) — see [LICENSE](LICENSE)
