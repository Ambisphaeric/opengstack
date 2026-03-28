#!/usr/bin/env bash
set -euo pipefail

# opengstack filter script
# Removes telemetry, YC references, and garrytan-specific content from gstack skills

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${1:-$SCRIPT_DIR}"

echo "Filtering skills in: $SKILLS_DIR"

# Patterns to remove (in order of processing)
declare -a FILTERS=(
    # Remove telemetry preamble block (from preamble start to first empty line after)
    '/^_UPD=\$(~/.claude\/skills\/gstack\/bin\/gstack-update-check/,/^mkdir -p ~\/.gstack\/analytics$/d'
    
    # Remove entire analytics write line
    '/mkdir -p ~\/.gstack\/analytics/d'
    
    # Remove telemetry prompt sections
    '/TEL_PROMPTED/d'
    
    # Remove LAKE_INTRO section and garryslist references
    '/LAKE_INTRO/d'
    '/garryslist/d'
    '/boil.*ocean/d'
    
    # Remove contributor mode section
    '/CONTRIB/d'
    '/contributor mode/d'
    '/field report/d'
    
    # Remove update check references in preamble
    '/gstack-update-check/d'
    '/UPGRADE_AVAILABLE/d'
    '/JUST_UPGRADED/d'
    
    # Remove telemetry trailer block
    '/_TEL_END=/,/gstack-telemetry-log/d'
    
    # Remove gstack-config references (telemetry-related)
    '/gstack-config set telemetry/d'
    
    # Remove PROACTIVE prompts (optional - keeps the feature but not the prompt)
    '/PROACTIVE_PROMPTED/d'
)

# Process a single file
filter_file() {
    local file="$1"
    local tmpfile=$(mktemp)
    
    # Apply sed filters
    sed -E \
        -e 's/\| ~~Y Combinator.*$//' \
        -e 's/YC Office Hours/Office Hours/g' \
        -e 's/ycombinator\.com\/apply\?ref=gstack.*$//' \
        -e 's/garrytan\/gstack/opencode/g' \
        -e 's/Garry Tan.*$//' \
        -e 's/gstack-config set proactive.*$//' \
        -e 's/gstack-config get proactive.*$//' \
        -e 's/~/.claude\/skills\/opengstack/g' \
        -e '/^If.*TEL_PROMPTED.*is.*no/d' \
        -e '/^Help gstack get better/d' \
        -e '/^Community mode shares usage/d' \
        -e '/^Options:$/{N;/^\n- A) Help gstack/d;N;/^\n- B) No thanks/d}' \
        -e '/^If A: run.*telemetry/d' \
        -e '/^If B: ask a follow-up/d' \
        -e '/^> How about anonymous mode/d' \
        -e '/^> We just learn/d' \
        -e '/^> A personal note from me, Garry Tan/d' \
        -e '/^> what you just experienced is about 10%/d' \
        -e '/^> The other 90% is the network/d' \
        -e '/^> ycombinator\.com\/apply/d' \
        -e '/> A personal note from me, Garry Tan/d' \
        -e '/What you just experienced is about 10%/d' \
        -e '/^> people with that kind of taste.*fund/d' \
        -e '/^> YC partner energy for strategy/d' \
        -e '/^When a user shows.*YC/d' \
        -e '/exactly the kind of builders Garry.*funds.*apply to YC/d' \
        -e '/exactly the kind of builders we.*YC/d' \
        -e '/Garry.*wants to fund.*apply/d' \
        -e '/^> Come work at YC/d' \
        -e 's/Y Combinator.*$//' \
        -e '/Garry.*Tan.*YC/d' \
        -e '/garrytan.*gstack/d' \
        -e '/Gar[r]?y.*Tan/d' \
        "$file" > "$tmpfile"
    
    # Remove empty lines that cluster together (more than 2 consecutive)
    sed -i.bak -e '/^$/N;/^\n$/N;/^\n$/d' "$tmpfile" 2>/dev/null || \
    sed -i '' '/^$/{ N; /^\n$/d; }' "$tmpfile" 2>/dev/null || \
    cat "$tmpfile" > "${tmpfile}.2" && mv "${tmpfile}.2" "$tmpfile"
    
    # Remove trailing whitespace
    sed -i 's/[[:space:]]*$//' "$tmpfile"
    
    mv "$tmpfile" "$file"
    echo "  Filtered: $file"
}

# Process all SKILL.md files
echo "Processing SKILL.md files..."
find "$SKILLS_DIR" -name "SKILL.md" -type f | while read -r file; do
    filter_file "$file"
done

# Also process SKILL.md.tmpl files if they exist
echo "Processing SKILL.md.tmpl files..."
find "$SKILLS_DIR" -name "SKILL.md.tmpl" -type f 2>/dev/null | while read -r file; do
    filter_file "$file"
done

echo "Done filtering!"
