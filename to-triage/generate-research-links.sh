#!/bin/bash

# Generate RESEARCH-01-02-03-PRELIMINARY-RESULTS-LINKS.md

OUTPUT="to-triage/RESEARCH-01-02-03-PRELIMINARY-RESULTS-LINKS.md"

# Start with header
cat > "$OUTPUT" << 'EOF'
# Research Prompts & Results Links

This document contains all three research prompts and links to results from different AI providers.

---

EOF

# Process each prompt (01, 02, 03)
for PROMPT_NUM in 01 02 03; do
    echo "## Research Prompt $PROMPT_NUM" >> "$OUTPUT"
    echo >> "$OUTPUT"

    # Find the original prompt file
    PROMPT_FILE=$(ls to-triage/RESEARCH-PROMPT-${PROMPT_NUM}--*.md 2>/dev/null | head -n 1)

    if [ -n "$PROMPT_FILE" ]; then
        echo '```markdown' >> "$OUTPUT"
        cat "$PROMPT_FILE" >> "$OUTPUT"
        echo '```' >> "$OUTPUT"
        echo >> "$OUTPUT"
    fi

    echo "### Results:" >> "$OUTPUT"
    echo >> "$OUTPUT"

    # Find all result files for this prompt and extract URLs
    for RESULT_FILE in to-triage/RESEARCH-RESULTS-FOR-PROMPT-${PROMPT_NUM}-*.md; do
        if [ -f "$RESULT_FILE" ]; then
            # Extract provider and model from filename
            # Pattern: RESEARCH-RESULTS-FOR-PROMPT-XX-251017-Provider-Model.md
            BASENAME=$(basename "$RESULT_FILE")
            # Remove prefix and suffix
            PROVIDER_MODEL=$(echo "$BASENAME" | sed 's/RESEARCH-RESULTS-FOR-PROMPT-'${PROMPT_NUM}'-251017-//' | sed 's/\.md$//')

            # Get URL from first line (inside angle brackets)
            URL=$(head -n 1 "$RESULT_FILE" | sed 's/^<\(.*\)>$/\1/')

            # Format provider-model name nicely
            DISPLAY_NAME=$(echo "$PROVIDER_MODEL" | sed 's/-/ - /g')

            echo "* **${DISPLAY_NAME}**: ${URL}" >> "$OUTPUT"
        fi
    done

    echo >> "$OUTPUT"
    echo "---" >> "$OUTPUT"
    echo >> "$OUTPUT"
done

echo "Generated: $OUTPUT"
