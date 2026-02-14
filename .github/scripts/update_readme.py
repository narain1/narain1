#!/usr/bin/env python3
"""
Update README.md with language statistics.
"""

import json
import re
from pathlib import Path

def load_statistics():
    """Load language statistics from JSON file."""
    stats_file = '.github/language_stats.json'
    if not Path(stats_file).exists():
        print(f"Statistics file {stats_file} not found.")
        return {}
    
    with open(stats_file, 'r') as f:
        return json.load(f)

def calculate_percentages(stats):
    """Calculate percentage for each language."""
    total_lines = sum(stats.values())
    if total_lines == 0:
        return {}
    
    percentages = {}
    for lang, lines in stats.items():
        percentages[lang] = (lines / total_lines) * 100
    
    return percentages

def generate_language_bars(stats, top_n=5):
    """Generate visual progress bars for top languages."""
    percentages = calculate_percentages(stats)
    
    # Get top N languages
    top_langs = sorted(percentages.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    bars = []
    bars.append("### 📊 Top Languages (by lines of code)")
    bars.append("")
    
    for lang, percent in top_langs:
        # Create a visual bar using Unicode block characters
        bar_length = 20
        filled = int((percent / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        bars.append(f"**{lang}** - {percent:.1f}%")
        bars.append(f"```{bar}```")
        bars.append("")
    
    total_lines = sum(stats.values())
    bars.append(f"*Based on {total_lines:,} lines of code added across all commits*")
    bars.append("")
    
    return "\n".join(bars)

def update_readme(language_section):
    """Update README.md with new language statistics."""
    readme_path = 'README.md'
    
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Define markers for our section
    start_marker = "<!-- LANGUAGE-STATS:START -->"
    end_marker = "<!-- LANGUAGE-STATS:END -->"
    
    # Check if markers exist
    if start_marker in content and end_marker in content:
        # Replace existing section
        pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
        replacement = f"{start_marker}\n{language_section}\n{end_marker}"
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # Add section before the existing Top Languages badge
        # Look for the GitHub README Stats badge
        badge_pattern = r'!\[Top Languages\].*?\)'
        if re.search(badge_pattern, content):
            # Insert before the badge
            replacement = f"{start_marker}\n{language_section}\n{end_marker}\n\n"
            new_content = re.sub(badge_pattern, replacement + r'\g<0>', content)
        else:
            # Append to end of file
            new_content = content.rstrip() + f"\n\n{start_marker}\n{language_section}\n{end_marker}\n"
    
    with open(readme_path, 'w') as f:
        f.write(new_content)
    
    print("README.md updated successfully!")

def main():
    """Main function to update README with language statistics."""
    print("Loading language statistics...")
    stats = load_statistics()
    
    if not stats:
        print("No statistics to update.")
        return
    
    print("Generating language bars...")
    language_section = generate_language_bars(stats)
    
    print("Updating README.md...")
    update_readme(language_section)
    
    print("Done!")

if __name__ == '__main__':
    main()
