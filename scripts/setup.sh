#!/usr/bin/env bash
# macos-computer-use setup
# Installs Python dependencies and checks macOS permissions.

set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BOLD}==> macos-computer-use setup${NC}"
echo ""

# --- Python deps ---
echo -e "${BOLD}[1/3] Installing Python dependencies...${NC}"
pip3 install -q pyautogui mss pillow atomacos
echo -e "${GREEN}✓ Python packages installed${NC}"
echo ""

# --- Screen Recording check ---
echo -e "${BOLD}[2/3] Checking Screen Recording permission...${NC}"
SCREENSHOT_TEST=$(python3 - <<'EOF'
import mss, sys
try:
    with mss.mss() as sct:
        img = sct.grab(sct.monitors[1])
    # If all pixels are black the permission is denied
    import struct
    raw = bytes(img.rgb)
    if all(b == 0 for b in raw[:300]):
        print("denied")
    else:
        print("granted")
except Exception as e:
    print(f"error: {e}")
EOF
)

if [[ "$SCREENSHOT_TEST" == "granted" ]]; then
    echo -e "${GREEN}✓ Screen Recording: granted${NC}"
else
    echo -e "${RED}✗ Screen Recording: not granted (screenshot returns black image)${NC}"
    echo -e "${YELLOW}  → Open: System Settings > Privacy & Security > Screen Recording"
    echo -e "  → Add your terminal app (e.g. Terminal, iTerm2) or the OpenClaw binary${NC}"
fi
echo ""

# --- Accessibility check ---
echo -e "${BOLD}[3/3] Checking Accessibility permission...${NC}"
ACCESSIBILITY_TEST=$(python3 - <<'EOF'
import subprocess, sys
result = subprocess.run(
    ["python3", "-c", "import pyautogui; pyautogui.position()"],
    capture_output=True, text=True, timeout=5
)
if result.returncode == 0:
    print("granted")
else:
    out = (result.stdout + result.stderr).lower()
    if "accessibility" in out or "axerror" in out or "permission" in out:
        print("denied")
    else:
        print("granted")  # position() may succeed even without, errors show on action
EOF
)

# More reliable: try to use atomacos
ATOM_TEST=$(python3 - <<'EOF'
try:
    import atomacos
    atomacos.getAppRefByBundleId("com.apple.finder")
    print("granted")
except atomacos.errors.AXErrorAPIDisabled:
    print("denied")
except Exception:
    print("granted")
EOF
)

if [[ "$ATOM_TEST" == "granted" ]]; then
    echo -e "${GREEN}✓ Accessibility: granted${NC}"
else
    echo -e "${RED}✗ Accessibility: not granted (UI control will silently fail)${NC}"
    echo -e "${YELLOW}  → Open: System Settings > Privacy & Security > Accessibility"
    echo -e "  → Add your terminal app (e.g. Terminal, iTerm2) or the OpenClaw binary${NC}"
fi

echo ""
echo -e "${BOLD}Done.${NC} Rerun this script after granting permissions to verify."
