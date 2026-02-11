# arXiv AI Feed System

An automated pipeline that fetches, summarizes, and displays the latest AI research papers from arXiv on your GitHub Pages site.

## 🎯 Overview

This system automatically:
- Fetches the 10 most recent papers from arXiv's cs.AI category every hour
- Generates key findings summaries from abstracts
- Updates a live dashboard on your GitHub Pages site
- Deploys changes automatically via GitHub Actions

## 📁 File Structure

```
.github/
├── agents/                          # Copilot CLI agents
│   ├── arxiv-fetcher.agent.md       # Fetches papers from arXiv API
│   ├── paper-summarizer.agent.md    # Generates key findings
│   ├── dashboard-builder.agent.md   # Updates Jekyll dashboard
│   └── pipeline-orchestrator.agent.md # Coordinates workflow
├── skills/                          # Reusable skills documentation
│   ├── api-interaction.skill.md
│   ├── data-processing.skill.md
│   ├── markdown-generation.skill.md
│   └── github-deployment.skill.md
├── prompts/                         # Task instructions
│   ├── fetch-papers.prompt.md
│   ├── summarize-abstract.prompt.md
│   ├── generate-dashboard.prompt.md
│   └── deploy-to-pages.prompt.md
├── coding-style.md                  # General coding conventions
├── html-guidelines.md               # HTML/CSS best practices
└── workflows/
    └── arxiv-pipeline.yml           # GitHub Actions workflow

_data/
└── arxiv_papers.yml                 # Paper data (auto-generated)

_pages/
└── arxiv-feed.md                    # Dashboard page

_includes/
└── paper-card.html                  # Paper card component
```

## 🚀 Setup Instructions

### 1. Enable GitHub Actions

The workflow is already configured in `.github/workflows/arxiv-pipeline.yml`. It will:
- Run every hour on the hour
- Can be manually triggered via "Actions" tab in GitHub

### 2. Configure GitHub Pages

1. Go to repository **Settings** → **Pages**
2. Under "Build and deployment":
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/ (root)`
3. Click **Save**

### 3. Verify Workflow Permissions

1. Go to **Settings** → **Actions** → **General**
2. Under "Workflow permissions":
   - Select **Read and write permissions**
3. Click **Save**

### 4. Trigger First Run

1. Go to **Actions** tab
2. Select "arXiv AI Feed Pipeline"
3. Click "Run workflow" → "Run workflow"
4. Wait ~2 minutes for completion

### 5. View Dashboard

After the workflow completes and GitHub Pages deploys (1-2 minutes):
- Visit: https://etlee110.github.io/test-pages/arxiv-feed/
- Check the navigation menu for "arXiv Feed" link

## 📊 How It Works

### Pipeline Stages

```
┌─────────────────────┐
│  1. Fetch Papers    │  Retrieves 10 latest papers from arXiv cs.AI
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  2. Summarize       │  Extracts key findings from abstracts
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  3. Build Dashboard │  Updates Jekyll page and components
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  4. Deploy          │  Commits changes and triggers GitHub Pages
└─────────────────────┘
```

### Data Flow

1. **arXiv API** → XML response with paper metadata
2. **Python script** → Parses XML, creates `_data/arxiv_papers.yml`
3. **Summarizer** → Adds key findings to YAML file
4. **Jekyll** → Renders dashboard using Liquid templates
5. **GitHub Pages** → Serves static HTML at `/arxiv-feed/`

## 🛠️ Customization

### Change Update Frequency

Edit `.github/workflows/arxiv-pipeline.yml`:

```yaml
on:
  schedule:
    - cron: '0 */2 * * *'  # Every 2 hours
    # or
    - cron: '0 9 * * *'    # Daily at 9 AM UTC
```

### Change arXiv Category

Edit the workflow script section (search for `cs.AI`):

```python
# Change category
params = {
    "search_query": "cat:cs.LG",  # Machine Learning
    # or "cat:cs.CV"               # Computer Vision
    # or "cat:cs.CL"               # Computation and Language
    "max_results": 10
}
```

### Change Number of Papers

Edit `max_results` in the workflow:

```python
"max_results": 20  # Display 20 papers instead of 10
```

### Customize Dashboard Styling

Edit `_pages/arxiv-feed.md` or `_includes/paper-card.html`:
- Modify the `<style>` sections
- Change colors, spacing, typography
- Adjust responsive breakpoints

## 🧪 Testing Locally

### Test Dashboard

```bash
# Install Jekyll
bundle install

# Serve locally
bundle exec jekyll serve

# Visit http://localhost:4000/arxiv-feed/
```

### Test Python Scripts

The workflow creates scripts inline. To test separately:

```bash
# Extract and run fetcher
python scripts/fetch_arxiv_papers.py

# Check output
cat _data/arxiv_papers.yml
```

## 📝 Copilot CLI Agents

The agents in `.github/agents/` are designed to be used with GitHub Copilot CLI:

```bash
# Example: Use the fetcher agent
@arxiv-fetcher "Fetch the latest 5 papers from cs.LG"

# Example: Use the orchestrator
@pipeline-orchestrator "Run the complete pipeline"
```

See each agent file for detailed instructions and capabilities.

## 🔧 Troubleshooting

### Workflow Fails

1. Check **Actions** tab for error logs
2. Verify GitHub Pages is enabled
3. Check workflow permissions (read/write required)
4. Ensure `_data/` directory exists

### Dashboard Not Updating

1. Wait 1-2 minutes for GitHub Pages rebuild
2. Hard refresh browser (Ctrl+Shift+R)
3. Check if workflow committed changes (git log)
4. Verify `_data/arxiv_papers.yml` contains data

### No Papers Displayed

1. Check `_data/arxiv_papers.yml` exists and has content
2. Verify YAML syntax is valid
3. Check Jekyll build logs in Actions tab
4. Ensure permalink `/arxiv-feed/` matches navigation

### arXiv API Rate Limit

The workflow includes a 3-second delay between requests. If you still hit limits:
- Reduce update frequency
- Add exponential backoff in error handling

## 📚 Documentation

- **Agents**: See `.github/agents/*.agent.md` for agent-specific docs
- **Skills**: See `.github/skills/*.skill.md` for technical references
- **Prompts**: See `.github/prompts/*.prompt.md` for task instructions
- **Coding Style**: See `.github/coding-style.md`
- **HTML Guidelines**: See `.github/html-guidelines.md`

## 🔗 Resources

- [arXiv API Documentation](https://arxiv.org/help/api)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Copilot CLI Custom Agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)

## 📄 License

This system uses the same license as the parent repository.

## 🙏 Acknowledgments

- Papers sourced from [arXiv.org](https://arxiv.org)
- Built on [Academic Pages Jekyll theme](https://github.com/academicpages/academicpages.github.io)
- Automated with GitHub Actions and Copilot CLI
