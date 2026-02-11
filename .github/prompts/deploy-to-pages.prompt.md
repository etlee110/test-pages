# Deploy to GitHub Pages Prompt

Instructions for deploying the arXiv feed updates to GitHub Pages.

## Objective
Commit changes to the repository and push to GitHub, triggering automatic deployment to GitHub Pages.

## Step-by-Step Instructions

### Step 1: Configure Git Identity
```bash
git config user.name "arXiv Feed Bot"
git config user.email "bot@arxiv-feed.local"
```

**In GitHub Actions:**
```bash
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"
```

### Step 2: Check Status
```bash
# View what changed
git status --short

# View detailed diff
git diff
```

**Expected changes:**
- `_data/arxiv_papers.yml` (modified)
- `_pages/arxiv-feed.md` (new or modified)
- `_includes/paper-card.html` (new or modified)
- `_data/navigation.yml` (modified, if navigation updated)

### Step 3: Stage Changes
```bash
# Stage specific files
git add _data/arxiv_papers.yml
git add _pages/arxiv-feed.md
git add _includes/paper-card.html

# If navigation was updated
git add _data/navigation.yml

# If custom styles were added
git add _sass/_arxiv-feed.scss
git add assets/css/main.scss
```

**Verify staged changes:**
```bash
git diff --cached --name-only
```

### Step 4: Commit Changes
```bash
# Generate commit message with timestamp
git commit -m "Update arXiv feed: $(date -u +"%Y-%m-%d %H:%M UTC")"
```

**Example commit message:**
```
Update arXiv feed: 2024-01-15 14:30 UTC
```

**Or with detailed message:**
```bash
git commit -m "Update arXiv feed: $(date -u +"%Y-%m-%d %H:%M UTC")" \
           -m "- Fetched 10 new papers from cs.AI category" \
           -m "- Generated key findings for all papers" \
           -m "- Updated dashboard with latest content"
```

### Step 5: Push to GitHub
```bash
# Push to main branch
git push origin main
```

**Expected output:**
```
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 8 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 1.23 KiB | 1.23 MiB/s, done.
Total 4 (delta 3), reused 0 (delta 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To https://github.com/etlee110/test-pages.git
   abc1234..def5678  main -> main
```

### Step 6: Verify Deployment

#### Wait for GitHub Pages Build
GitHub Pages automatically rebuilds when main branch updates. This takes ~1-2 minutes.

#### Check Deployment Status (GitHub CLI)
```bash
# View latest deployment
gh api repos/etlee110/test-pages/pages/builds/latest

# Wait for completion (polling)
while true; do
    status=$(gh api repos/etlee110/test-pages/pages/builds/latest --jq '.status')
    if [ "$status" = "built" ]; then
        echo "✓ Deployment completed!"
        break
    fi
    echo "Status: $status (waiting...)"
    sleep 10
done
```

#### Verify Site is Live
```bash
# Test if page is accessible
curl -s -o /dev/null -w "%{http_code}" https://etlee110.github.io/test-pages/arxiv-feed/

# Should return: 200
```

**Manual verification:**
Visit: https://etlee110.github.io/test-pages/arxiv-feed/

## Error Handling

### If Nothing to Commit
```bash
if git diff-index --quiet HEAD --; then
    echo "No changes to commit"
    exit 0
fi

git add ...
git commit ...
git push ...
```

### If Push Fails (Non-Fast-Forward)
```bash
# Pull latest changes first
git pull --rebase origin main

# Resolve conflicts if any
# Then push again
git push origin main
```

### If GitHub Pages Build Fails
1. Check repository Settings → Pages
2. View build logs
3. Common issues:
   - YAML syntax error in data files
   - Invalid front matter in pages
   - Missing `_config.yml` settings
   - Jekyll plugin not supported by GitHub Pages

**Debug locally:**
```bash
bundle exec jekyll build

# If errors, fix them before pushing
```

### If Deployment Times Out
```bash
# Wait up to 5 minutes
timeout=300
elapsed=0

while [ $elapsed -lt $timeout ]; do
    if curl -s -f https://etlee110.github.io/test-pages/arxiv-feed/ > /dev/null; then
        echo "✓ Site is live!"
        exit 0
    fi
    echo "Waiting for deployment... ($elapsed/$timeout seconds)"
    sleep 10
    elapsed=$((elapsed + 10))
done

echo "⚠ Deployment verification timed out"
exit 1
```

## GitHub Actions Integration

### Full Workflow Example
```yaml
name: Update arXiv Feed

on:
  schedule:
    - cron: '0 * * * *'  # Hourly
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update-feed:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install pyyaml requests
      
      - name: Fetch and process papers
        run: |
          echo "Fetching papers from arXiv..."
          # Run fetcher script
          # Run summarizer script
          # Run dashboard builder script
      
      - name: Commit and push if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          
          git add _data/arxiv_papers.yml _pages/arxiv-feed.md _includes/paper-card.html _data/navigation.yml
          
          if git diff --staged --quiet; then
            echo "No changes to commit"
          else
            git commit -m "Update arXiv feed: $(date -u +"%Y-%m-%d %H:%M UTC")"
            git push origin main
            echo "✓ Changes pushed successfully"
          fi
      
      - name: Verify deployment
        run: |
          echo "Waiting for GitHub Pages deployment..."
          sleep 60  # Wait for build to start
          
          # Test site accessibility
          for i in {1..10}; do
            if curl -s -f https://etlee110.github.io/test-pages/arxiv-feed/ > /dev/null; then
              echo "✓ Site is live!"
              exit 0
            fi
            echo "Attempt $i/10: Site not ready yet..."
            sleep 10
          done
          
          echo "⚠ Could not verify deployment (may still succeed)"
```

## Repository Configuration

### Required Settings

**GitHub Pages:**
- Navigate to: Repository → Settings → Pages
- Source: Deploy from a branch
- Branch: `main`
- Folder: `/ (root)`

**Branch Protection (Optional):**
- Require status checks before merging
- Require branches to be up to date

**Workflow Permissions:**
- Settings → Actions → General → Workflow permissions
- Select: "Read and write permissions"

## Best Practices

### Commit Messages
- Include timestamp for traceability
- Be descriptive about what changed
- Use conventional commit format if desired:
  ```
  feat: update arXiv feed with 10 new papers
  ```

### Atomic Commits
- One logical change per commit
- Don't mix unrelated changes
- Makes rollback easier if needed

### Push Frequency
- Push after complete pipeline execution
- Don't push intermediate states
- Reduces unnecessary deployments

### Error Recovery
- Always check exit codes
- Log errors with context
- Provide actionable error messages
- Have rollback strategy ready

## Success Criteria
- ✅ Changes committed with clear message
- ✅ Push to GitHub successful
- ✅ No merge conflicts
- ✅ GitHub Pages build triggered
- ✅ Build completed successfully
- ✅ Site accessible at URL
- ✅ Dashboard displays new papers
- ✅ No broken links or errors

## Expected Output
```
[DEPLOY] Configuring git...
[DEPLOY] Staging changes...
[DEPLOY] Files staged: _data/arxiv_papers.yml, _pages/arxiv-feed.md, _includes/paper-card.html
[DEPLOY] Committing changes...
[DEPLOY] Commit: "Update arXiv feed: 2024-01-15 14:30 UTC"
[DEPLOY] Pushing to GitHub...
[DEPLOY] Push successful!
[DEPLOY] Waiting for deployment...
[DEPLOY] ✓ Site deployed successfully!
[DEPLOY] URL: https://etlee110.github.io/test-pages/arxiv-feed/
```
