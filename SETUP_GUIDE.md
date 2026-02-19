# Setting Up Language Statistics for All Repositories

Follow these steps to enable language statistics tracking across all your repositories (public and private):

## Step 1: Create a Personal Access Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Fill in the details:
   - **Note**: `Language Statistics` (or any descriptive name)
   - **Expiration**: Choose your preferred expiration (90 days recommended for security)
   - **Select scopes**:
     - ✅ `repo` - Full control of private repositories (**Required**)
     - ✅ `read:user` - Read user profile data (Optional)
4. Click **"Generate token"**
5. **IMPORTANT**: Copy the token immediately - you won't be able to see it again!

## Step 2: Add Token as a Repository Secret

1. Go to your profile repository: `https://github.com/narain1/narain1`
2. Click **Settings** (repository settings, not your account settings)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **"New repository secret"**
5. Fill in:
   - **Name**: `GH_PAT` (exactly as shown - this name is used by the workflow)
   - **Secret**: Paste your personal access token from Step 1
6. Click **"Add secret"**

## Step 3: Test the Workflow

You can manually trigger the workflow to test it:

1. Go to the **Actions** tab in your repository
2. Click on **"Update Language Statistics"** in the left sidebar
3. Click **"Run workflow"** button
4. Select the branch (usually `main`)
5. Click **"Run workflow"**

The workflow will:
- Fetch all your repositories (public and private)
- Clone each repository temporarily
- Analyze all commits for language statistics
- Update your README with the results
- Commit and push the changes

This may take several minutes depending on how many repositories you have.

## Step 4: Verify the Results

After the workflow completes:
1. Check your README.md - it should now show statistics from all your repositories
2. Review the workflow logs to see which repositories were analyzed
3. The statistics will show your total lines of code across all languages

## What Gets Analyzed?

- ✅ All repositories where you are the owner
- ✅ Both public and private repositories
- ✅ All commits in all branches
- ✅ All programming languages (40+ supported)
- ❌ Forked repositories (skipped to avoid double-counting)

## Automatic Updates

Once set up, the workflow automatically runs:
- When you push to the main branch
- When pull requests are merged
- Every Sunday (weekly update)
- Anytime you manually trigger it

## Troubleshooting

### Token Expired
If your statistics stop updating after a while, your token may have expired. Generate a new token and update the `GH_PAT` secret.

### Missing Private Repos
Ensure your token has the `repo` scope enabled. Without it, only public repositories will be analyzed.

### Workflow Failures
Check the Actions tab for error messages. Common issues:
- Token not set correctly (check secret name is exactly `GH_PAT`)
- Token doesn't have required permissions
- Rate limiting (workflow will retry automatically)

## Security Notes

- Never share or commit your personal access token
- Store it only in GitHub Secrets
- Use token expiration for better security
- Revoke and regenerate tokens if compromised
- The token is only used within GitHub Actions and never exposed

## Need Help?

Check the detailed documentation in [LANGUAGE_STATS.md](LANGUAGE_STATS.md) for more information about how the system works and customization options.
