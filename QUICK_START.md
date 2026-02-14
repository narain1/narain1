# 🚀 Quick Start Guide

## What You Have Now

A fully automated language statistics system that will track your coding contributions across **ALL your repositories** (public and private) and display them beautifully on your GitHub profile!

## Current Display

Your README now shows language statistics like this:

```
📊 Top Languages (by lines of code)

Python - 56.3%
███████████░░░░░░░░░

Markdown - 31.6%
██████░░░░░░░░░░░░░░

YAML - 12.1%
██░░░░░░░░░░░░░░░░░░

Based on 462 lines of code added across all commits
```

> **Note**: Currently showing stats from just this repository. Follow setup below to analyze ALL your repos!

## ⚡ Quick Setup (5 minutes)

### Step 1: Create GitHub Token (2 minutes)

1. Click here: [Create Token](https://github.com/settings/tokens/new)
2. Fill in:
   - **Note**: `Language Statistics`
   - **Expiration**: 90 days (recommended)
   - **Scopes**: Check ✅ `repo` (this is the only one required!)
3. Click "Generate token"
4. **COPY THE TOKEN** - you won't see it again! (looks like: `ghp_xxxxxxxxxxxx`)

### Step 2: Add Token to Repository (1 minute)

1. Go to: https://github.com/narain1/narain1/settings/secrets/actions
2. Click "New repository secret"
3. Enter:
   - **Name**: `GH_PAT` (MUST be exactly this)
   - **Secret**: Paste your token from Step 1
4. Click "Add secret"

### Step 3: Run the Workflow (30 seconds)

1. Go to: https://github.com/narain1/narain1/actions/workflows/update-language-stats.yml
2. Click "Run workflow" button (blue button on the right)
3. Keep "Branch: main" selected
4. Click "Run workflow"

### Step 4: Wait & Watch (2-10 minutes)

- Click on the workflow run to watch progress
- It will analyze all your repositories
- When done, check your profile README!

## 🎉 That's It!

After setup, the system runs automatically:
- ✅ Every time you push to main
- ✅ When PRs are merged  
- ✅ Every Sunday (weekly update)
- ✅ Anytime you manually trigger it

## 📊 What Gets Analyzed?

- All repositories you own
- Both public AND private repos
- All commits in all branches
- 40+ programming languages
- Forked repos are skipped

## 🔍 Example Output

After running across all your repos, you might see:

```
📊 Top Languages (by lines of code)

Python - 45.2%
█████████░░░░░░░░░░░

JavaScript - 28.4%
██████░░░░░░░░░░░░░░

TypeScript - 15.3%
███░░░░░░░░░░░░░░░░░

C++ - 8.1%
██░░░░░░░░░░░░░░░░░░

Go - 3.0%
█░░░░░░░░░░░░░░░░░░░

Based on 145,892 lines of code added across all commits
```

## 🛠️ Troubleshooting

### Workflow Failed?
- **Check**: Is your token named exactly `GH_PAT`?
- **Check**: Does your token have `repo` scope?
- **Check**: Has your token expired?

### No Private Repos?
- Make sure token has `repo` scope (not just `public_repo`)

### Still Stuck?
- Check the workflow logs in the Actions tab
- See detailed docs in [LANGUAGE_STATS.md](LANGUAGE_STATS.md)

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup with screenshots
- **[LANGUAGE_STATS.md](LANGUAGE_STATS.md)** - Technical documentation
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - What was built

## 🔒 Security

- ✅ Token stored securely in GitHub Secrets
- ✅ Never exposed in logs or commits
- ✅ CodeQL scanned - no vulnerabilities
- ✅ Only used within GitHub Actions
- ✅ You can revoke it anytime

## 💡 Pro Tips

1. **Token Renewal**: Set a calendar reminder before your token expires
2. **Manual Updates**: Trigger workflow after major coding sessions
3. **Customization**: Edit `.github/scripts/update_readme.py` to show more/fewer languages
4. **Monitoring**: Star your repo to get workflow notifications

## 🎯 Next Steps

1. ✅ Setup complete? Merge this PR!
2. ✅ Follow the 3-step setup above
3. ✅ Run the workflow
4. ✅ Share your awesome profile!

---

**Need help?** Open an issue or check the detailed guides above!
