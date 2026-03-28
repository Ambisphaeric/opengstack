#!/usr/bin/env python3
"""
opengstack filter script - NUKE MODE
Removes ALL telemetry, YC references, Garry Tan content, and gstack branding
"""

import re
import sys
from pathlib import Path


def filter_skill_content(content: str) -> str:
    """NUKE all gstack slop from skills"""

    # STEP 1: Remove entire telemetry preamble blocks
    # Match from ```bash to next ```, containing telemetry variables
    content = re.sub(r"```bash\s*\n_UPD=.*?```\s*\n", "", content, flags=re.DOTALL)

    # Remove any remaining bash blocks with .gstack/ references
    content = re.sub(
        r"```bash\s*\n.*?\.gstack/.*?(?=```)", "", content, flags=re.DOTALL
    )

    # STEP 2: Remove entire sections about telemetry/config
    content = re.sub(
        r"If `TEL_PROMPTED` is.*?touch ~/.gstack/\.telemetry-prompted.*?```\s*\n?",
        "",
        content,
        flags=re.DOTALL,
    )

    content = re.sub(
        r"If `PROACTIVE_PROMPTED` is.*?touch ~/.gstack/\.proactive-prompted.*?```\s*\n?",
        "",
        content,
        flags=re.DOTALL,
    )

    content = re.sub(
        r"If `LAKE_INTRO` is.*?touch ~/.gstack/\.completeness-intro-seen.*?```\s*\n?",
        "",
        content,
        flags=re.DOTALL,
    )

    # STEP 3: Remove ## Contributor Mode section
    content = re.sub(
        r"## Contributor Mode.*?## (Voice|Telemetry|Completion)",
        r"## \1",
        content,
        flags=re.DOTALL,
    )

    # STEP 4: Remove ## Telemetry section entirely
    content = re.sub(r"## Telemetry.*?```.*?```\s*\n", "", content, flags=re.DOTALL)

    # STEP 5: NUKE all gstack binary references
    content = re.sub(r"`?~/.claude/skills/gstack/bin/[^\s`]+`?", "", content)

    # STEP 6: Replace gstack paths with opengstack
    content = re.sub(
        r"~/.claude/skills/gstack/", "~/.claude/skills/opengstack/", content
    )

    # STEP 7: Remove all .gstack/ directory references
    content = re.sub(r"~?/?\.gstack/[^\s`\n]*", "", content)

    # STEP 8: Remove mkdir/touch commands for .gstack
    content = re.sub(r"mkdir -p[^\n]*\.gstack[^\n]*\n?", "", content)
    content = re.sub(r"touch[^\n]*\.gstack[^\n]*\n?", "", content)

    # STEP 9: NUKE Garry Tan completely
    content = re.sub(
        r"> A personal note from me, Garry Tan.*?(?=\n\n|## )",
        "",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(r"shaped by Garry Tan\'s[^.]*\.", "", content)
    content = re.sub(r"Garry Tan", "", content)
    content = re.sub(r"YC partner energy for strategy[^.]*\.", "", content)

    # STEP 10: NUKE YC references
    content = re.sub(r"YC Office Hours", "Office Hours", content)
    content = re.sub(r"ycombinator\.com/apply\?ref=[^\s]*", "", content)
    content = re.sub(r"consider applying to YC[^.]*\.", "", content)

    # STEP 11: NUKE garryslist
    content = re.sub(r"https?://garryslist\.org[^\s]*", "", content)
    content = re.sub(r"Boil the (Lake|Ocean)[^.]*\.?", "", content)

    # STEP 12: Replace GStack with OpenGStack (product name)
    content = re.sub(r"\bGStack\b", "OpenGStack", content)

    # STEP 13: Remove standalone gstack references in prose
    # But keep it in contexts like "skill system" or "framework"
    content = re.sub(r"\bgstack skills?\b", "skills", content, flags=re.IGNORECASE)
    content = re.sub(
        r"\bgstack[- ]?telemetry\b", "telemetry", content, flags=re.IGNORECASE
    )

    # STEP 14: Remove ref=gstack from URLs
    content = re.sub(r"\?ref=gstack", "", content)

    # STEP 15: Remove broken sentence fragments
    content = re.sub(
        r"gstack follows the \*\*[^*]+\*\* principle.*?Read more:",
        "",
        content,
        flags=re.DOTALL,
    )

    # STEP 16: Fix "You are GStack" -> "You are using OpenGStack"
    content = re.sub(r"You are GStack,", "You are using OpenGStack,", content)
    content = re.sub(r"You are OpenGStack,", "You are using OpenGStack,", content)

    # STEP 17: Remove orphaned code fences and clean up
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = re.sub(r"```\s*\n\s*```", "", content)
    content = re.sub(r"^\s*```\s*$", "", content, flags=re.MULTILINE)

    # STEP 18: Clean empty lines at start/end
    content = content.strip()

    return content + "\n"


def filter_file(filepath: Path) -> bool:
    """Filter a single file, returns True if modified"""
    if not filepath.exists():
        return False

    original = filepath.read_text()
    filtered = filter_skill_content(original)

    if filtered != original:
        filepath.write_text(filtered)
        return True
    return False


def main():
    skills_dir = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent
    )

    print(f"NUKING gstack slop from: {skills_dir}")

    modified = 0
    for skill_file in skills_dir.rglob("SKILL.md"):
        if filter_file(skill_file):
            print(f"  NUKED: {skill_file.relative_to(skills_dir)}")
            modified += 1

    for tmpl_file in skills_dir.rglob("SKILL.md.tmpl"):
        if filter_file(tmpl_file):
            print(f"  NUKED: {tmpl_file.relative_to(skills_dir)}")
            modified += 1

    print(f"\nDone! Cleansed {modified} files of gstack slop.")


if __name__ == "__main__":
    main()
