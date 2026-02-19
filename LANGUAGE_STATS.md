# Language Statistics Feature

This repository includes an automated language statistics tracking system that analyzes **all your repositories** (both public and private) to calculate the lines of code added for each programming language across your entire GitHub profile.

## How It Works

### Components

1. **GitHub Actions Workflow** (`.github/workflows/update-language-stats.yml`)
   - Automatically runs on:
     - Push to `main` branch
     - Merged pull requests
     - Weekly schedule (every Sunday)
     - Manual trigger via workflow dispatch
   
2. **Language Analysis Script** (`.github/scripts/analyze_languages.py`)
   - Connects to GitHub API to fetch all your repositories
   - Clones each repository temporarily
   - Analyzes all commits in each repository
   - Counts lines of code added by language based on file extensions
   - Supports 40+ programming languages
   - Aggregates statistics across all repositories
   - Generates statistics in JSON format

3. **README Update Script** (`.github/scripts/update_readme.py`)
   - Reads the generated language statistics
   - Creates visual progress bars for top 5 languages
   - Updates the README.md with current statistics
   - Maintains markers: `<!-- LANGUAGE-STATS:START -->` and `<!-- LANGUAGE-STATS:END -->`

### Authentication

To analyze private repositories, you need to set up a Personal Access Token (PAT):

1. **Create a Personal Access Token**:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a descriptive name like "Language Statistics"
   - Select scopes:
     - `repo` (Full control of private repositories) - **Required for private repos**
     - `read:user` (Read user profile data) - Optional but recommended
   - Click "Generate token" and copy the token

2. **Add the token as a repository secret**:
   - Go to your repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `GH_PAT`
   - Value: Paste your personal access token
   - Click "Add secret"

**Note**: The workflow will use `GH_PAT` if available, otherwise it falls back to the default `GITHUB_TOKEN` (which only has access to public repositories).

### Supported Languages

The system automatically detects and tracks the following **coding** languages (markup and configuration files are excluded):
- Python, TypeScript, Java, C++, C, CUDA, C#
- Go, Rust, Ruby, PHP, Swift, Kotlin, Scala
- R, Objective-C, Shell, SQL
- Vue, Dart, Lua, Perl

**Excluded:** HTML, CSS, SCSS, SASS, JavaScript, Markdown, JSON, XML, YAML, TOML, Jupyter Notebooks

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

1. **Analyze only current repository**: Set the environment variable `ANALYZE_ALL_REPOS=false` in the workflow.

2. **Change the number of languages displayed**: Edit `.github/scripts/update_readme.py` and modify the `top_n` parameter in the `generate_language_bars()` function.

3. **Add more language extensions**: Edit `.github/scripts/analyze_languages.py` and add entries to the `LANGUAGE_EXTENSIONS` dictionary. Note that the system only tracks coding languages and excludes markup/configuration files like HTML, CSS, JSON, YAML, etc.

4. **Modify the update schedule**: Edit `.github/workflows/update-language-stats.yml` and change the `cron` schedule.

5. **Exclude specific repositories**: Modify the `analyze_all_repositories()` function to filter out repositories by name.

## Display Format

The statistics appear in your README with colored progress bars for each language:

```
### 📊 Top Languages (by lines of code)

**Python** - 45.2%
🟦🟦🟦🟦🟦🟦🟦🟦🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜

**TypeScript** - 30.5%
🟦🟦🟦🟦🟦🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜

...
```

Each language uses a distinct color for its progress bar, making it easy to visually distinguish between different technologies.

## How Statistics are Calculated

- **Multi-Repository Analysis**: The system analyzes ALL your repositories (where you are the owner)
- **Lines Added**: The system counts only lines added (not deleted) in all commits
- **Per Language**: Lines are attributed to languages based on file extensions
- **Across All Commits**: All commits in all branches of all repositories are analyzed
- **Cumulative**: Statistics represent the total contribution across all your repositories
- **Fork Handling**: Forked repositories are skipped to avoid double-counting

## Performance Considerations

- The workflow may take several minutes to complete depending on the number and size of repositories
- Repositories are cloned temporarily and deleted after analysis
- Rate limiting is respected with automatic pausing between repositories
- Large repositories (>5 minute clone time) will timeout gracefully

## Notes

- The workflow automatically commits changes with `[skip ci]` to avoid infinite loops
- Binary files and files without recognized extensions are excluded
- The generated `language_stats.json` file is ignored by git (see `.gitignore`)
- Statistics update automatically but may take a few moments to reflect in merged PRs

## Troubleshooting

If the statistics don't update:
1. Check the Actions tab for workflow run status
2. Ensure you have created a `GH_PAT` secret with the `repo` scope for private repository access
3. Verify that the workflow has write permissions to the repository
4. Verify that the README contains the marker comments
5. Check the workflow logs for any error messages
6. Ensure your token hasn't expired (PATs need to be renewed)

### Common Issues

- **"No commits found"**: The token may not have access to repositories
- **Clone timeouts**: Very large repositories may timeout - this is normal
- **Rate limiting**: The workflow respects GitHub rate limits and will pause automatically

## Example Output

After the workflow runs, your profile README will display your actual code contributions by language, giving visitors a clear picture of your coding activity across different technologies.
