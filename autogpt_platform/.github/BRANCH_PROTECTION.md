# Branch Protection Configuration Guide - SADOCKDOG

## 🔒 Branch Protection Setup for `master`

This document provides instructions to configure branch protection rules for the SADOCKDOG Platform repository.

> ⚠️ **Note**: Branch protection rules must be configured through GitHub's web interface or GitHub CLI. They cannot be set via files in the repository.

## 📋 Recommended Settings for `master` Branch

### Method 1: Via GitHub Web Interface

1. **Navigate to Settings**:
   - Go to your repository: https://github.com/SADOCKDOG/SADOCKDOG
   - Click on **Settings** tab
   - Click on **Branches** in the left sidebar

2. **Add Branch Protection Rule**:
   - Click **Add branch protection rule**
   - Branch name pattern: `master`

3. **Configure Protection Rules**:

#### ✅ Require Pull Request Reviews
```
☑️ Require a pull request before merging
   ☑️ Require approvals: 1
   ☑️ Dismiss stale pull request approvals when new commits are pushed
   ☐ Require review from Code Owners (optional)
   ☐ Restrict who can dismiss pull request reviews (for teams)
   ☐ Allow specified actors to bypass required pull requests (not recommended)
```

#### ✅ Require Status Checks
```
☑️ Require status checks to pass before merging
   ☑️ Require branches to be up to date before merging
   
   Status checks to require:
   - ✅ Backend CI / Lint & Format
   - ✅ Backend CI / Tests
   - ✅ Frontend CI / Lint & Build
   - ✅ Frontend CI / TypeScript Check
   - ✅ CodeQL / Analyze Python
   - ✅ CodeQL / Analyze JavaScript/TypeScript
```

#### ✅ Additional Protections
```
☑️ Require conversation resolution before merging
☑️ Require signed commits (recommended for security)
☑️ Require linear history (keeps git history clean)
☐ Require deployments to succeed before merging (if using deployments)
☑️ Lock branch (prevent direct pushes)
☐ Do not allow bypassing the above settings
```

#### ✅ Rules Applied to Administrators
```
☐ Include administrators
   
   ⚠️ Recommendation: Keep unchecked initially for flexibility
   Enable later when team grows
```

#### ✅ Restrict Pushes
```
☑️ Restrict who can push to matching branches
   Add: SADOCKDOG (yourself)
   Add: Trusted collaborators only
```

### Method 2: Via GitHub CLI

```bash
# Install GitHub CLI if not already installed
# https://cli.github.com/

# Authenticate
gh auth login

# Apply branch protection (run from repository root)
gh api repos/SADOCKDOG/SADOCKDOG/branches/master/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=Backend CI / Lint & Format \
  --field required_status_checks[contexts][]=Backend CI / Tests \
  --field required_status_checks[contexts][]=Frontend CI / Lint & Build \
  --field required_status_checks[contexts][]=Frontend CI / TypeScript Check \
  --field required_pull_request_reviews[required_approving_review_count]=1 \
  --field required_pull_request_reviews[dismiss_stale_reviews]=true \
  --field enforce_admins=false \
  --field required_conversation_resolution=true \
  --field required_linear_history=true \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

## 🎯 What These Settings Do

### ✅ Pull Request Reviews
- **Prevents direct pushes** to master
- **Requires code review** before merging
- **Dismisses old approvals** when code changes

### ✅ Status Checks
- **Runs CI/CD** automatically on every PR
- **Prevents broken code** from being merged
- **Ensures tests pass** before merging

### ✅ Conversation Resolution
- **All review comments** must be resolved
- **Improves communication** between contributors

### ✅ Linear History
- **Prevents merge commits**
- **Keeps git history clean** and easy to follow
- **Requires rebase or squash merge**

### ✅ Lock Branch
- **No direct commits** to master
- **All changes via PR** only

## 🚀 Workflow After Protection

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes and Commit**:
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**:
   - Go to GitHub
   - Click "Compare & pull request"
   - Fill out the PR template
   - Wait for CI checks to pass

4. **Get Review**:
   - Request review if working with team
   - Address feedback
   - Resolve conversations

5. **Merge**:
   - Once approved and CI passes
   - Click "Squash and merge" or "Rebase and merge"
   - Delete branch after merging

## 📊 Verify Protection is Active

```bash
# Check current branch protection
gh api repos/SADOCKDOG/SADOCKDOG/branches/master/protection

# Should return protection rules, not 404
```

## ⚙️ Adjusting Settings

As your project grows, you may want to:

- **Increase required reviewers** (e.g., 2 approvals)
- **Add CODEOWNERS** file for automatic reviewer assignment
- **Enable administrator enforcement** 
- **Add deployment protection rules**
- **Require signed commits** for all contributors

## 🔧 Troubleshooting

### Can't Merge PR
- ✅ Check all CI checks passed
- ✅ Ensure branch is up to date with master
- ✅ Resolve all conversations
- ✅ Get required approvals

### Need to Bypass Protection (Emergency)
1. Temporarily disable protection (Settings → Branches)
2. Make emergency fix
3. Re-enable protection immediately
4. Create follow-up PR to explain changes

---

## 📝 Next Steps

After setting up branch protection:

1. ☐ Enable branch protection on master
2. ☐ Test by creating a test PR
3. ☐ Verify CI runs automatically
4. ☐ Confirm merge is blocked without approvals
5. ☐ Document process for your team
6. ☐ Create CODEOWNERS file (optional)

## 📞 Questions?

If you need help configuring branch protection, please create an issue with the `documentation` label.

---

**Last updated:** November 8, 2025  
**Maintained by:** SADOCKDOG Team
