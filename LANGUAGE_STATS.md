# Language Statistics Feature

This repository includes an automated language statistics tracking system that analyzes all commits and pull requests to calculate the lines of code added for each programming language.

## How It Works

### Components

1. **GitHub Actions Workflow** (`.github/workflows/update-language-stats.yml`)
   - Automatically runs on:
     - Push to `main` branch
     - Merged pull requests
     - Weekly schedule (every Sunday)
     - Manual trigger via workflow dispatch
   
2. **Language Analysis Script** (`.github/scripts/analyze_languages.py`)
   - Analyzes all commits in the repository
   - Counts lines of code added by language based on file extensions
   - Supports 40+ programming languages
   - Generates statistics in JSON format

3. **README Update Script** (`.github/scripts/update_readme.py`)
   - Reads the generated language statistics
   - Creates visual progress bars for top 5 languages
   - Updates the README.md with current statistics
   - Maintains markers: `<!-- LANGUAGE-STATS:START -->` and `<!-- LANGUAGE-STATS:END -->`

### Supported Languages

The system automatically detects and tracks the following languages:
- Python, JavaScript, TypeScript, Java, C++, C, C#
- Go, Rust, Ruby, PHP, Swift, Kotlin, Scala
- R, Objective-C, Shell, SQL
- HTML, CSS, SCSS, SASS, Markdown
- JSON, XML, YAML, TOML
- Vue, Dart, Lua, Perl
- And more...

## Usage

### Automatic Updates

The workflow runs automatically and updates your README with the latest statistics. No manual intervention is required.

### Manual Trigger

You can manually trigger the workflow:
1. Go to the "Actions" tab in your repository
2. Select "Update Language Statistics"
3. Click "Run workflow"

### Custom Configuration

To customize the feature:

1. **Change the number of languages displayed**: Edit `.github/scripts/update_readme.py` and modify the `top_n` parameter in the `generate_language_bars()` function.

2. **Add more language extensions**: Edit `.github/scripts/analyze_languages.py` and add entries to the `LANGUAGE_EXTENSIONS` dictionary.

3. **Modify the update schedule**: Edit `.github/workflows/update-language-stats.yml` and change the `cron` schedule.

## Display Format

The statistics appear in your README as:

```
### 📊 Top Languages (by lines of code)

**Python** - 45.2%
```████████████████████```

**JavaScript** - 30.5%
```██████████████░░░░░░```

...
```

## How Statistics are Calculated

- **Lines Added**: The system counts only lines added (not deleted) in all commits
- **Per Language**: Lines are attributed to languages based on file extensions
- **Across All Commits**: All commits in all branches are analyzed
- **Cumulative**: Statistics represent the total contribution over the repository's lifetime

## Notes

- The workflow automatically commits changes with `[skip ci]` to avoid infinite loops
- Binary files and files without recognized extensions are excluded
- The generated `language_stats.json` file is ignored by git (see `.gitignore`)
- Statistics update automatically but may take a few moments to reflect in merged PRs

## Troubleshooting

If the statistics don't update:
1. Check the Actions tab for workflow run status
2. Ensure the workflow has write permissions to the repository
3. Verify that the README contains the marker comments
4. Check the workflow logs for any error messages

## Example Output

After the workflow runs, your profile README will display your actual code contributions by language, giving visitors a clear picture of your coding activity across different technologies.
