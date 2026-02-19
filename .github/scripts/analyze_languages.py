#!/usr/bin/env python3
"""
Analyze language statistics based on commits and PRs across all repositories.
Counts lines of code added by language across all commits in all user repositories.
"""

import os
import subprocess
import json
import re
import tempfile
import shutil
from collections import defaultdict
from pathlib import Path
from github import Github
import time

# Language file extensions mapping
# Only includes actual coding languages, excludes markup/config files
LANGUAGE_EXTENSIONS = {
    '.py': 'Python',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript',
    '.java': 'Java',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.c': 'C',
    '.h': 'C/C++',
    '.hpp': 'C++',
    '.cu': 'CUDA',
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

def analyze_repository_commits(repo_path):
    """Analyze commits in a specific repository."""
    language_stats = defaultdict(int)
    original_dir = os.getcwd()
    
    try:
        os.chdir(repo_path)
        
        # Get all commits
        result = subprocess.run(
            ['git', 'log', '--all', '--pretty=format:%H'],
            capture_output=True,
            text=True,
            check=True
        )
        
        if not result.stdout.strip():
            return language_stats
        
        commits = [c for c in result.stdout.strip().split('\n') if c]
        
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
    
    finally:
        os.chdir(original_dir)
    
    return language_stats

def clone_and_analyze_repo(repo, temp_dir, username):
    """Clone a repository and analyze its commits."""
    repo_name = repo.full_name
    print(f"  Analyzing {repo_name}...")
    
    # Skip forks unless they have unique commits
    if repo.fork and repo.owner.login == username:
        print(f"    Skipping fork: {repo_name}")
        return defaultdict(int)
    
    # Create a subdirectory for this repo
    repo_dir = os.path.join(temp_dir, repo.name)
    
    try:
        # Clone the repository
        clone_url = repo.clone_url
        if 'GITHUB_TOKEN' in os.environ:
            # Use token for authentication
            token = os.environ['GITHUB_TOKEN']
            clone_url = clone_url.replace('https://', f'https://{token}@')
        
        result = subprocess.run(
            ['git', 'clone', '--quiet', clone_url, repo_dir],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            print(f"    Failed to clone {repo_name}")
            return defaultdict(int)
        
        # Analyze the repository
        stats = analyze_repository_commits(repo_dir)
        
        # Clean up
        shutil.rmtree(repo_dir, ignore_errors=True)
        
        return stats
        
    except Exception as e:
        print(f"    Error analyzing {repo_name}: {e}")
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir, ignore_errors=True)
        return defaultdict(int)

def analyze_all_repositories():
    """Analyze all repositories for the authenticated user."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("ERROR: GITHUB_TOKEN environment variable not set")
        return defaultdict(int)
    
    print("Connecting to GitHub API...")
    g = Github(token)
    user = g.get_user()
    username = user.login
    
    print(f"Fetching repositories for {username}...")
    
    # Get all repositories (both public and private)
    repos = list(user.get_repos(affiliation='owner'))
    print(f"Found {len(repos)} repositories")
    
    # Create temporary directory for cloning
    temp_dir = tempfile.mkdtemp(prefix='github_lang_stats_')
    print(f"Using temporary directory: {temp_dir}")
    
    combined_stats = defaultdict(int)
    
    try:
        for i, repo in enumerate(repos, 1):
            print(f"\n[{i}/{len(repos)}] {repo.full_name}")
            
            repo_stats = clone_and_analyze_repo(repo, temp_dir, username)
            
            # Merge stats
            for language, lines in repo_stats.items():
                combined_stats[language] += lines
            
            # Rate limiting: be nice to GitHub
            if i % 10 == 0:
                print("  Pausing to respect rate limits...")
                time.sleep(2)
    
    finally:
        # Clean up temp directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    return combined_stats

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
    
    if not result.stdout.strip():
        print("No commits found in repository.")
        return language_stats
    
    commits = [c for c in result.stdout.strip().split('\n') if c]
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
    print("=" * 60)
    print("GitHub Language Statistics Analyzer")
    print("=" * 60)
    
    # Check if we should analyze all repositories or just the current one
    analyze_all = os.environ.get('ANALYZE_ALL_REPOS', 'true').lower() == 'true'
    
    if analyze_all:
        print("\nMode: Analyzing ALL repositories (public and private)")
        stats = analyze_all_repositories()
    else:
        print("\nMode: Analyzing current repository only")
        stats = analyze_commits()
    
    if not stats:
        print("\nNo language statistics found.")
        stats = {}
    
    save_statistics(stats)
    print(f"\nStatistics saved to .github/language_stats.json")
    print("=" * 60)

if __name__ == '__main__':
    main()
