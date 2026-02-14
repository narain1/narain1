#!/usr/bin/env python3
"""
Analyze language statistics based on commits and PRs.
Counts lines of code added by language across all commits.
"""

import os
import subprocess
import json
import re
from collections import defaultdict
from pathlib import Path

# Language file extensions mapping
LANGUAGE_EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'JavaScript',
    '.tsx': 'TypeScript',
    '.java': 'Java',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.c': 'C',
    '.h': 'C/C++',
    '.hpp': 'C++',
    '.cs': 'C#',
    '.go': 'Go',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
    '.r': 'R',
    '.R': 'R',
    '.m': 'Objective-C',
    '.sh': 'Shell',
    '.bash': 'Shell',
    '.sql': 'SQL',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'SASS',
    '.md': 'Markdown',
    '.json': 'JSON',
    '.xml': 'XML',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.toml': 'TOML',
    '.vue': 'Vue',
    '.dart': 'Dart',
    '.lua': 'Lua',
    '.perl': 'Perl',
    '.pl': 'Perl',
}

def get_file_language(filename):
    """Determine the language based on file extension."""
    ext = Path(filename).suffix.lower()
    return LANGUAGE_EXTENSIONS.get(ext, None)

def analyze_commits():
    """Analyze all commits and count lines added per language."""
    language_stats = defaultdict(int)
    
    # Get all commits
    result = subprocess.run(
        ['git', 'log', '--all', '--pretty=format:%H'],
        capture_output=True,
        text=True,
        check=True
    )
    
    commits = result.stdout.strip().split('\n')
    print(f"Analyzing {len(commits)} commits...")
    
    for commit_hash in commits:
        if not commit_hash:
            continue
            
        # Get diff stats for this commit
        try:
            result = subprocess.run(
                ['git', 'show', '--numstat', '--format=', commit_hash],
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if not line:
                    continue
                    
                parts = line.split('\t')
                if len(parts) < 3:
                    continue
                    
                added, deleted, filename = parts[0], parts[1], parts[2]
                
                # Skip binary files
                if added == '-' or deleted == '-':
                    continue
                    
                # Get language for file
                language = get_file_language(filename)
                if language:
                    try:
                        language_stats[language] += int(added)
                    except ValueError:
                        continue
                        
        except subprocess.CalledProcessError:
            continue
    
    return language_stats

def save_statistics(stats):
    """Save statistics to a JSON file."""
    # Sort by lines of code
    sorted_stats = dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))
    
    output_file = '.github/language_stats.json'
    with open(output_file, 'w') as f:
        json.dump(sorted_stats, f, indent=2)
    
    print(f"\nLanguage Statistics (Lines Added):")
    print("=" * 50)
    for lang, lines in sorted_stats.items():
        print(f"{lang:20} {lines:>10,} lines")
    print("=" * 50)
    
    return sorted_stats

def main():
    """Main function to analyze and save language statistics."""
    print("Analyzing language statistics from commits...")
    stats = analyze_commits()
    
    if not stats:
        print("No language statistics found.")
        stats = {}
    
    save_statistics(stats)
    print(f"\nStatistics saved to .github/language_stats.json")

if __name__ == '__main__':
    main()
