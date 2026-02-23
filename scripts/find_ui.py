#!/usr/bin/env python3
"""
Find UI elements on screen via the macOS Accessibility API.

Usage:
  find_ui.py [--app APP_NAME] [--role ROLE] [--title TITLE] [--label LABEL] [--limit N]

Output: JSON array of matching elements, each with:
  { "title": str, "role": str, "label": str,
    "position": {"x": int, "y": int},
    "size": {"w": int, "h": int},
    "center": {"x": int, "y": int} }

Common roles:
  AXButton, AXTextField, AXTextArea, AXStaticText, AXMenuItem,
  AXWindow, AXCheckBox, AXRadioButton, AXLink, AXImage, AXGroup

Examples:
  # Find all buttons in Safari
  find_ui.py --app Safari --role AXButton

  # Find a specific button by title
  find_ui.py --app Safari --role AXButton --title "Back"

  # Find all text fields in frontmost app
  find_ui.py --role AXTextField

  # Use center coordinates for clicking:
  #   python3 mouse.py click <center.x> <center.y>

Requires: pip install atomacos
Requires: Accessibility permission granted
"""

import argparse
import json
import sys

try:
    import atomacos
    from atomacos import errors as axerrors
except ImportError:
    sys.exit("Error: atomacos not installed. Run: pip install atomacos")


def serialize_element(el):
    try:
        pos = el.AXPosition
        size = el.AXSize
        x, y = int(pos.x), int(pos.y)
        w, h = int(size.width), int(size.height)
    except Exception:
        x = y = w = h = 0

    def safe_attr(attr):
        try:
            v = getattr(el, attr)
            return str(v) if v is not None else ""
        except Exception:
            return ""

    cx = x + w // 2
    cy = y + h // 2

    return {
        "title": safe_attr("AXTitle"),
        "role": safe_attr("AXRole"),
        "label": safe_attr("AXDescription"),
        "value": safe_attr("AXValue"),
        "position": {"x": x, "y": y},
        "size": {"w": w, "h": h},
        "center": {"x": cx, "y": cy},
    }


def matches(el, role=None, title=None, label=None):
    def safe(attr):
        try:
            v = getattr(el, attr)
            return str(v).lower() if v else ""
        except Exception:
            return ""

    if role and role.lower() not in safe("AXRole"):
        return False
    if title and title.lower() not in safe("AXTitle"):
        return False
    if label and label.lower() not in safe("AXDescription"):
        return False
    return True


def walk(el, role, title, label, results, limit):
    if len(results) >= limit:
        return
    if matches(el, role, title, label):
        results.append(serialize_element(el))
    try:
        children = el.AXChildren
        if children:
            for child in children:
                if len(results) >= limit:
                    break
                walk(child, role, title, label, results, limit)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Find UI elements via Accessibility API")
    parser.add_argument("--app", help="App name (e.g. 'Safari', 'Finder'). Default: frontmost app.")
    parser.add_argument("--role", help="AX role filter (e.g. AXButton, AXTextField)")
    parser.add_argument("--title", help="AXTitle substring filter (case-insensitive)")
    parser.add_argument("--label", help="AXDescription substring filter (case-insensitive)")
    parser.add_argument("--limit", type=int, default=50, help="Max results (default 50)")
    args = parser.parse_args()

    try:
        if args.app:
            try:
                app = atomacos.getAppRefByLocalizedName(args.app)
            except Exception:
                # Try bundle ID style names
                app = atomacos.NativeUIElement.getAppRefByLocalizedName(args.app)
        else:
            app = atomacos.getFrontmostApp()
    except axerrors.AXErrorAPIDisabled:
        sys.exit("Error: Accessibility permission not granted. "
                 "Go to System Settings > Privacy & Security > Accessibility and add your terminal.")
    except Exception as e:
        sys.exit(f"Error getting app: {e}")

    results = []
    walk(app, args.role, args.title, args.label, results, args.limit)

    print(json.dumps(results, indent=2))
    sys.stderr.write(f"Found {len(results)} element(s)\n")


if __name__ == "__main__":
    main()
