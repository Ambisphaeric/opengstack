#!/usr/bin/env python3
"""
opengstack cleanup script
Fixes broken fragments after filtering
"""

import re
import sys
from pathlib import Path


def cleanup_skill_content(content: str) -> str:
    """Clean up broken fragments from filtering"""

    lines = content.split("\n")
    cleaned = []
    skip_until_blank = False

    for i, line in enumerate(lines):
        # Skip lines that are clearly broken fragments
        if re.match(r"^If output shows `$", line):
            skip_until_blank = True
            continue

        if skip_until_blank:
            if line.strip() == "":
                skip_until_blank = False
            continue

        # Fix broken gstack-config references
        line = re.sub(r"~/.claude/skills/opengstack/bin/gstack-config", "echo", line)

        # Fix broken URLs
        line = re.sub(r"open https?://$", "", line)
        line = re.sub(r"https?://garryslist\.org.*", "", line)

        # Fix broken markdown links
        line = re.sub(r"\[.*?\]\s*$", "", line)

        # Remove lines that are just fragments
        if re.match(r"^thing when AI", line):
            continue
        if re.match(r"^Boil the", line):
            continue
        if re.match(r"^open$", line.strip()):
            continue
        if re.match(r"^\*\*.*\*\*$", line) and len(line) < 20:
            continue
        if re.match(r"^Tell the user", line) and not line.strip().endswith(
            (".", "?", "!")
        ):
            continue
        if re.match(r"^gstack follows the", line):
            continue
        if re.match(r"^>\s*$", line):
            continue

        cleaned.append(line)

    content = "\n".join(cleaned)

    # Remove multiple consecutive blank lines
    content = re.sub(r"\n{4,}", "\n\n\n", content)

    # Remove trailing whitespace
    content = "\n".join(line.rstrip() for line in content.split("\n"))

    return content.rstrip("\n") + "\n"


def cleanup_file(filepath: Path) -> bool:
    """Cleanup a single file"""
    if not filepath.exists():
        return False

    original = filepath.read_text()
    cleaned = cleanup_skill_content(original)

    if cleaned != original:
        filepath.write_text(cleaned)
        return True
    return False


def main():
    root = Path(__file__).parent.parent

    print(f"Cleaning up skills in: {root}")

    modified = 0
    for skill_file in root.rglob("SKILL.md"):
        if cleanup_file(skill_file):
            print(f"  Cleaned: {skill_file.relative_to(root)}")
            modified += 1

    print(f"\nDone! Cleaned {modified} files.")


if __name__ == "__main__":
    main()
