#!/usr/bin/env python3
"""
Run AppleScript via osascript.

Usage:
  applescript.py -e 'AppleScript expression'
  applescript.py -f /path/to/script.applescript

Output: stdout from osascript (result of the script).

Examples:
  # Activate an app
  applescript.py -e 'tell application "Safari" to activate'

  # Get frontmost app name
  applescript.py -e 'tell application "System Events" to return name of first application process whose frontmost is true'

  # Open a URL in Safari
  applescript.py -e 'tell application "Safari" to open location "https://example.com"'

  # Click a menu item
  applescript.py -e 'tell application "System Events" to tell process "Finder" to click menu item "New Folder" of menu "File" of menu bar 1'

  # Get clipboard contents
  applescript.py -e 'return the clipboard'

  # Set clipboard contents
  applescript.py -e 'set the clipboard to "text to copy"'

Note: osascript is always available on macOS; no extra permissions needed for most operations.
App control (System Events) may require Accessibility permission.
"""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Run AppleScript via osascript")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--expression", help="AppleScript expression to evaluate")
    group.add_argument("-f", "--file", help="Path to .applescript file")
    args = parser.parse_args()

    cmd = ["osascript"]
    if args.expression:
        cmd += ["-e", args.expression]
    else:
        cmd.append(args.file)

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        sys.exit(result.returncode)

    if result.stdout:
        print(result.stdout.rstrip())


if __name__ == "__main__":
    main()
