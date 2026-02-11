# GitHub Deployment Skill

Skills for committing changes and deploying to GitHub Pages.

## Core Competencies

### 1. Git Configuration

#### Set User Identity
```bash
git config user.name "arXiv Feed Bot"
git config user.email "bot@arxiv-feed.local"

# For GitHub Actions (already configured in workflow)
git config user.name "${{ github.actor }}"
git config user.email "${{ github.actor }}@users.noreply.github.com"
```

### 2. Git Operations

#### Check Status
```bash
# View changed files
git status --short

# View diff
git diff --stat

# Check what would be committed
git diff --cached
```

#### Stage Changes
```bash
# Stage specific files
git add _data/arxiv_papers.yml
git add _pages/arxiv-feed.md
git add _includes/paper-card.html

# Stage multiple files at once
git add _data/arxiv_papers.yml _pages/arxiv-feed.md _includes/paper-card.html _data/navigation.yml

# Stage all changes (use cautiously)
git add .
```

#### Commit Changes
```bash
# Commit with message
git commit -m "Update arXiv feed: $(date -u +"%Y-%m-%d %H:%M UTC")"

# Commit with multi-line message
git commit -m "Update arXiv feed" -m "- Fetched 10 new papers from cs.AI" -m "- Updated dashboard with key findings"

# Amend last commit (if needed)
git commit --amend -m "Updated message"
```

#### Push Changes
```bash
# Push to main branch
git push origin main

# Push with verbose output
git push -v origin main

# Force push (use only when absolutely necessary)
git push --force-with-lease origin main
```

### 3. Branch Management

#### Working with Branches
```bash
# List branches
git branch -a

# Create and switch to new branch
git checkout -b feature/arxiv-feed

# Switch branches
git checkout main

# Merge branch
git merge feature/arxiv-feed

# Delete branch
git branch -d feature/arxiv-feed
```

### 4. GitHub Pages Deployment

#### Deployment Methods

**Method 1: Deploy from Branch (Recommended)**
- Repository Settings → Pages
- Source: Deploy from a branch
- Branch: `main` or `gh-pages`, folder: `/ (root)` or `/docs`
- GitHub automatically builds and deploys Jekyll sites

**Method 2: GitHub Actions Workflow**
- Repository Settings → Pages
- Source: GitHub Actions
- Use custom workflow (see GitHub Actions section)

#### Verify Deployment
```bash
# Check if GitHub Pages is enabled
gh api repos/etlee110/test-pages/pages

# View deployment status
gh api repos/etlee110/test-pages/deployments | jq '.[0]'

# Visit site (after ~1 minute)
open https://etlee110.github.io/test-pages/arxiv-feed/
```

### 5. GitHub Actions Integration

#### Workflow for Automated Updates
```yaml
# .github/workflows/arxiv-pipeline.yml
name: arXiv Feed Pipeline

on:
  schedule:
    - cron: '0 * * * *'  # Hourly
  workflow_dispatch:  # Manual trigger

permissions:
  contents: write

jobs:
  update-feed:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install pyyaml requests

      - name: Fetch papers from arXiv
        run: |
          # Run fetcher script (to be created)
          python scripts/fetch_arxiv_papers.py
      
      - name: Summarize papers
        run: |
          # Run summarizer script (to be created)
          python scripts/summarize_papers.py
      
      - name: Commit and push changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add _data/arxiv_papers.yml _pages/arxiv-feed.md _includes/paper-card.html
          git diff --quiet && git diff --staged --quiet || (
            git commit -m "Update arXiv feed: $(date -u +"%Y-%m-%d %H:%M UTC")"
            git push
          )
```

#### Manual Trigger
```bash
# Trigger workflow manually via GitHub CLI
gh workflow run arxiv-pipeline.yml

# View workflow runs
gh run list --workflow=arxiv-pipeline.yml

# View logs
gh run view <run-id> --log
```

### 6. Conflict Resolution

#### Handle Merge Conflicts
```bash
# Pull latest changes before pushing
git pull origin main

# If conflicts occur
git status  # View conflicted files

# Edit files to resolve conflicts (remove <<<<, ====, >>>> markers)
# Then:
git add <resolved-file>
git commit -m "Resolve merge conflict"
git push origin main
```

#### Abort Merge
```bash
git merge --abort
```

### 7. Rollback Strategies

#### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

#### Undo Last Commit (Discard Changes)
```bash
git reset --hard HEAD~1
```

#### Revert Specific Commit
```bash
# Find commit hash
git log --oneline

# Revert it (creates new commit)
git revert <commit-hash>
git push origin main
```

### 8. Debugging Deployment Issues

#### Check Jekyll Build Locally
```bash
# Install Jekyll
bundle install

# Build site
bundle exec jekyll build

# Serve locally
bundle exec jekyll serve
```

#### View GitHub Pages Build Logs
```bash
# Via GitHub CLI
gh api repos/etlee110/test-pages/pages/builds/latest

# Via web interface
# Repository → Settings → Pages → View builds
```

#### Common Deployment Issues
| Issue | Solution |
|-------|----------|
| 404 on GitHub Pages | Check permalink format, wait 1-2 minutes for deployment |
| Site not updating | Clear browser cache, check git push succeeded |
| Jekyll build failed | Check `_config.yml` syntax, validate front matter |
| Assets not loading | Verify paths are relative or use `{{ site.baseurl }}` |
| YAML parse error | Validate YAML syntax in data files |

### 9. Security Best Practices

```bash
# Never commit secrets
# Use GitHub Secrets for sensitive data
# Access in workflow: ${{ secrets.SECRET_NAME }}

# Check for secrets before committing
git diff --cached | grep -i "password\|token\|key\|secret"

# Use .gitignore
echo "*.env" >> .gitignore
echo "secrets.yml" >> .gitignore
```

### 10. Automation Scripts

#### Pre-commit Check
```bash
#!/bin/bash
# scripts/pre-commit-check.sh

# Validate YAML files
for file in _data/*.yml; do
    python -c "import yaml; yaml.safe_load(open('$file'))" || exit 1
done

# Check for secrets
if git diff --cached | grep -qiE "password|token|key|secret"; then
    echo "Warning: Possible secret detected!"
    exit 1
fi

echo "Pre-commit checks passed"
```

#### Post-update Verification
```bash
#!/bin/bash
# scripts/verify-deployment.sh

URL="https://etlee110.github.io/test-pages/arxiv-feed/"

# Wait for deployment (max 2 minutes)
for i in {1..24}; do
    if curl -s -f "$URL" > /dev/null; then
        echo "Deployment successful!"
        exit 0
    fi
    echo "Waiting for deployment... ($i/24)"
    sleep 5
done

echo "Deployment verification failed"
exit 1
```

## GitHub CLI Tips

```bash
# View repository info
gh repo view etlee110/test-pages

# View workflow status
gh workflow view arxiv-pipeline.yml

# View recent runs
gh run list --limit 5

# View pull requests
gh pr list

# Create issue
gh issue create --title "Pipeline failed" --body "Details..."
```

## Deployment Checklist

- [ ] Changes committed with descriptive message
- [ ] No sensitive data in commit
- [ ] Git push successful
- [ ] GitHub Actions workflow completed (if applicable)
- [ ] Site accessible at expected URL
- [ ] Page displays correctly (check in browser)
- [ ] Mobile responsive (check on small screen)
- [ ] No console errors (check browser DevTools)
