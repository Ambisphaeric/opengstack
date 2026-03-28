#!/usr/bin/env python3
"""
opengstack filter script
Removes telemetry, YC references, garrytan slop from gstack skills
"""

import re
import sys
from pathlib import Path


def filter_skill_content(content: str) -> str:
    """Apply all filters to skill content"""

    # Remove telemetry preamble block (from _UPD to closing brace)
    preamble_pattern = r"```bash\n_UPD=.*?(?=\n```|\n\n[A-Z#])"
    content = re.sub(preamble_pattern, "", content, flags=re.DOTALL)

    # Remove LAKE_INTRO / Completeness Principle section
    lake_pattern = r"If `LAKE_INTRO` is `no`:.*?`touch ~\/\.gstack\/\.completeness-intro-seen`\n```\n.*?```\n"
    content = re.sub(lake_pattern, "", content, flags=re.DOTALL)

    # Remove telemetry prompts section
    tel_pattern = (
        r"If `TEL_PROMPTED` is `no` AND.*?(?=If `PROACTIVE_PROMPTED`|## Voice)"
    )
    content = re.sub(tel_pattern, "", content, flags=re.DOTALL)

    # Remove PROACTIVE_PROMPTED section
    proactive_pattern = r"If `PROACTIVE_PROMPTED` is `no` AND.*?`touch ~\/\.gstack\/\.proactive-prompted`\n```\n"
    content = re.sub(proactive_pattern, "", content, flags=re.DOTALL)

    # Remove contributor mode block
    contrib_pattern = r"## Contributor Mode.*?(?=## Voice|## Completion)"
    content = re.sub(contrib_pattern, "", content, flags=re.DOTALL)

    # Remove telemetry trailer block
    tel_trailer_pattern = (
        r"## Telemetry \(run last\).*?```bash\n.*?gstack-telemetry-log.*?```\n"
    )
    content = re.sub(tel_trailer_pattern, "", content, flags=re.DOTALL)

    # Remove update check references
    content = re.sub(r"UPGRADE_AVAILABLE.*?(?=\n|$)", "", content)
    content = re.sub(r"JUST_UPGRADED.*?(?=\n|$)", "", content)
    content = re.sub(r"gstack-update-check", "echo", content)

    # Remove gstack-config references (telemetry/proactive settings)
    content = re.sub(
        r"~/.claude/skills/gstack/", "~/.claude/skills/opengstack/", content
    )

    # Remove YC slop - personal notes from Garry Tan
    garry_note_pattern = (
        r"> A personal note from me, Garry Tan, the creator of GStack:.*?(?=\n\n|\n>)"
    )
    content = re.sub(garry_note_pattern, "", content, flags=re.DOTALL)

    # Remove YC apply links with ref tracking
    content = re.sub(r"ycombinator\.com/apply\?ref=gstack.*", "", content)

    # Remove YC partner energy references
    content = re.sub(r"YC partner energy for strategy.*", "", content)

    # Remove "exactly the kind of builders Garry respects" type phrases
    founder_phrase = r"people with that kind of taste and drive are exactly the kind of builders.*?consider applying to YC.*"
    content = re.sub(founder_phrase, "", content, flags=re.DOTALL)

    # Remove garryslist references
    content = re.sub(r"https?://garryslist\.org[^\s]*", "", content)
    content = re.sub(r"Boil the (Lake|Ocean).*", "", content)

    # Remove YC from office-hours description
    content = re.sub(r"YC Office Hours", "Office Hours", content)

    # Remove Garry Tan references
    content = re.sub(r"shaped by Garry Tan's.*", "", content)
    content = re.sub(r"Garry Tan", "OpenGStack", content)
    content = re.sub(r"Gar[r]?y.*Tan", "", content)

    # Remove GStack branding where it's the product name
    content = re.sub(r"\bGStack\b", "OpenGStack", content)

    # Remove "ref=gstack" from any URLs
    content = re.sub(r"\?ref=gstack", "", content)

    # Remove standalone gstack references (when referring to product/skill system)
    content = re.sub(r"\bgstack skills?\b", "skills", content, flags=re.IGNORECASE)
    content = re.sub(r"\bgstack\b", "OpenGStack", content, flags=re.IGNORECASE)

    # Remove .gstack/ directory references (telemetry/analytics paths)
    content = re.sub(r"~?/?\.gstack/[^\s\n`\"']*", "", content)
    content = re.sub(r"mkdir -p[^\n]*\.gstack[^\n]*", "", content)
    content = re.sub(r"touch[^\n]*\.gstack[^\n]*", "", content)
    content = re.sub(r"echo[^\n]*\.gstack[^\n]*", "", content)

    # Remove gstack-config binary references
    content = re.sub(
        r"~/.claude/skills/gstack/bin/gstack-config[^\s\n`\"']*", "", content
    )
    content = re.sub(
        r"~/.claude/skills/opengstack/bin/gstack-config[^\s\n`\"']*", "", content
    )

    # Remove gstack-upgrade references
    content = re.sub(
        r"~/.claude/skills/gstack/gstack-upgrade/[^\s\n`\"']*", "", content
    )
    content = re.sub(
        r"~/.claude/skills/opengstack/gstack-upgrade/[^\s\n`\"']*", "", content
    )

    # Remove gstack binary paths
    content = re.sub(r"~/.claude/skills/gstack/bin/[^\s\n`\"']*", "", content)
    content = re.sub(r"\.claude/skills/gstack/bin/[^\s\n`\"']*", "", content)

    # Clean up broken partial text
    content = re.sub(
        r"gstack follows the \*\*[^*]*\*\* principle.*?Read more:",
        "",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(r"Boil the (Lake|Ocean)[^\n]*", "", content)
    content = re.sub(r"https?://garryslist\.org[^\s]*", "", content)

    # Remove lines that only contain empty code fences after cleanup
    content = re.sub(r"\n```\s*\n(?=\n|#)", "\n", content)

    # Clean up empty code blocks and whitespace
    content = re.sub(r"\n{4,}", "\n\n", content)
    content = re.sub(r"```\n\n```", "", content)

    # Remove orphaned backticks
    content = re.sub(r"^```\n*$", "", content, flags=re.MULTILINE)

    # Clean leading/trailing whitespace per line
    lines = [line.rstrip() for line in content.split("\n")]
    content = "\n".join(lines)

    # Remove trailing newlines
    content = content.rstrip("\n") + "\n"

    return content


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

    print(f"Filtering skills in: {skills_dir}")

    modified = 0
    for skill_file in skills_dir.rglob("SKILL.md"):
        if filter_file(skill_file):
            print(f"  Filtered: {skill_file.relative_to(skills_dir)}")
            modified += 1

    for tmpl_file in skills_dir.rglob("SKILL.md.tmpl"):
        if filter_file(tmpl_file):
            print(f"  Filtered: {tmpl_file.relative_to(skills_dir)}")
            modified += 1

    print(f"\nDone! Modified {modified} files.")


if __name__ == "__main__":
    main()
