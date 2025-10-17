#!/usr/bin/env python3
"""
Generate RESEARCH-01-02-03-PRELIMINARY-RESULTS-LINKS.md with collapsible prompt sections.
"""

import os
import re
from pathlib import Path

def extract_url_from_file(filepath):
    """Extract URL from first line of markdown file (assumes <URL> format)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        # Remove angle brackets if present
        match = re.match(r'^<(.+)>$', first_line)
        if match:
            return match.group(1)
        return first_line

def get_prompt_title(prompt_file):
    """Extract title from prompt filename."""
    basename = os.path.basename(prompt_file)
    # Pattern: RESEARCH-PROMPT-XX--title.md
    match = re.match(r'RESEARCH-PROMPT-(\d+)--(.+)\.md$', basename)
    if match:
        num = match.group(1)
        title = match.group(2).replace('-', ' ').title()
        return f"Research Prompt {num}: {title}"
    return basename

def get_provider_model_name(result_file):
    """Extract provider and model from result filename."""
    basename = os.path.basename(result_file)
    # Pattern: RESEARCH-RESULTS-FOR-PROMPT-XX-251017-Provider-Model.md
    match = re.match(r'RESEARCH-RESULTS-FOR-PROMPT-\d+-\d+-(.+)\.md$', basename)
    if match:
        provider_model = match.group(1)
        # Replace hyphens with spaces, but preserve structure
        return provider_model.replace('-', ' - ')
    return basename

def main():
    base_dir = Path('to-triage')
    output_file = base_dir / 'RESEARCH-01-02-03-PRELIMINARY-RESULTS-LINKS.md'

    with open(output_file, 'w', encoding='utf-8') as out:
        # Header
        out.write("# Research Prompts & Results Links\n\n")
        out.write("This document contains all three research prompts and links to results from different AI providers.\n\n")
        out.write("---\n\n")

        # Process each prompt (01, 02, 03)
        for prompt_num in ['01', '02', '03']:
            # Find the prompt file
            prompt_files = list(base_dir.glob(f'RESEARCH-PROMPT-{prompt_num}--*.md'))
            if not prompt_files:
                continue

            prompt_file = prompt_files[0]
            prompt_title = get_prompt_title(prompt_file)

            out.write(f"## {prompt_title}\n\n")

            # Read the full prompt content
            with open(prompt_file, 'r', encoding='utf-8') as pf:
                prompt_content = pf.read()

            # Write prompt in collapsible section
            out.write("<details>\n")
            out.write(f"<summary>View Full Prompt (click to expand)</summary>\n\n")
            out.write("```markdown\n")
            out.write(prompt_content)
            out.write("```\n\n")
            out.write("</details>\n\n")

            # Find all result files for this prompt
            result_files = sorted(base_dir.glob(f'RESEARCH-RESULTS-FOR-PROMPT-{prompt_num}-*.md'))

            if result_files:
                out.write("### Results:\n\n")
                for result_file in result_files:
                    provider_model = get_provider_model_name(result_file)
                    url = extract_url_from_file(result_file)
                    out.write(f"* **{provider_model}**: {url}\n")
                out.write("\n")

            out.write("---\n\n")

    print(f"Generated: {output_file}")

if __name__ == '__main__':
    main()
