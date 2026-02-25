#!/usr/bin/env python3
"""
Take a macOS screenshot and save it to a file.

Usage:
  screenshot.py [--output PATH] [--window TITLE] [--region X Y W H]

Output: prints the saved file path to stdout.
Requires Screen Recording permission.
"""

import argparse
import os
import sys
import time

def main():
    parser = argparse.ArgumentParser(description="Take a macOS screenshot")
    parser.add_argument("--output", help="Output file path (default: /tmp/openclaw-screenshot-<ts>.png)")
    parser.add_argument("--window", help="Capture a specific window by title substring (case-insensitive)")
    parser.add_argument("--region", nargs=4, type=int, metavar=("X", "Y", "W", "H"),
                        help="Capture a screen region: x y width height")
    args = parser.parse_args()

    ts = int(time.time())
    output_path = args.output or f"/tmp/openclaw-screenshot-{ts}.png"

    if args.window:
        _capture_window(args.window, output_path)
    elif args.region:
        x, y, w, h = args.region
        _capture_region(x, y, w, h, output_path)
    else:
        _capture_fullscreen(output_path)

    print(output_path)


def _capture_fullscreen(output_path):
    try:
        import mss
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor (0 = all monitors combined)
            img = sct.grab(monitor)
            _save_mss(img, output_path)
    except ImportError:
        # Fallback: screencapture CLI
        _screencapture(output_path)


def _capture_region(x, y, w, h, output_path):
    try:
        import mss
        with mss.mss() as sct:
            region = {"left": x, "top": y, "width": w, "height": h}
            img = sct.grab(region)
            _save_mss(img, output_path)
    except ImportError:
        _screencapture(output_path, region=f"{x},{y},{w},{h}")


def _capture_window(title, output_path):
    """Capture a named window using screencapture -l (window ID)."""
    import subprocess, json

    # Get window list via AppleScript / CGWindowList
    script = '''
    use framework "Foundation"
    use framework "CoreGraphics"
    use scripting additions

    set wList to {}
    set ws to current application's CGWindowListCopyWindowInfo(current application's kCGWindowListOptionOnScreenOnly, current application's kCGNullWindowID)
    repeat with w in ws
        set wName to (w's valueForKey:"kCGWindowName") as text
        set wOwner to (w's valueForKey:"kCGWindowOwnerName") as text
        set wId to (w's valueForKey:"kCGWindowNumber") as integer
        set end of wList to (wId as text) & "|" & wOwner & "|" & wName
    end repeat
    return wList
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        # Fall back to full screen
        sys.stderr.write(f"Window lookup failed, falling back to full screen: {result.stderr}\n")
        _capture_fullscreen(output_path)
        return

    target_lower = title.lower()
    window_id = None
    for line in result.stdout.strip().split(", "):
        line = line.strip().strip('"')
        parts = line.split("|")
        if len(parts) == 3:
            wid, owner, wname = parts
            if target_lower in owner.lower() or target_lower in wname.lower():
                window_id = wid.strip()
                break

    if window_id:
        subprocess.run(["screencapture", "-l", window_id, "-x", output_path],
                       check=True, capture_output=True)
    else:
        sys.stderr.write(f"Window '{title}' not found, falling back to full screen.\n")
        _capture_fullscreen(output_path)


def _save_mss(img, output_path):
    from PIL import Image
    import io
    # mss returns BGRA; convert to RGB PNG
    pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
    pil_img.save(output_path, "PNG")


def _screencapture(output_path, region=None):
    import subprocess
    # Use full path to avoid PATH issues
    cmd = ["/usr/sbin/screencapture", "-x"]
    if region:
        cmd += ["-R", region]
    cmd.append(output_path)
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
