# arXiv AI Paper Feed System - Implementation Plan

## Problem Statement
Build an automated system that fetches the latest arXiv papers in AI (cs.AI category), generates summaries, and displays them on a live dashboard hosted on GitHub Pages—orchestrated entirely by GitHub Copilot CLI agents without manual code writing.

## Proposed Approach
Create a system of specialized Copilot CLI agents that work together in a data pipeline:
1. **Fetcher Agent** - Retrieves papers from arXiv API (cs.AI category)
2. **Summarizer Agent** - Processes paper abstracts and generates key findings
3. **Dashboard Agent** - Updates the Jekyll-based dashboard with latest papers
4. **Orchestrator Agent** - Coordinates the pipeline and handles scheduling

The system will use GitHub Actions for hourly execution and deploy via GitHub Pages from the gh-pages branch.

## Requirements
- **GitHub Account**: etlee110
- **Repository**: test-pages
- **Frequency**: Hourly updates
- **Category**: cs.AI (Artificial Intelligence)
- **Display**: Top 10 most recent papers
- **Paper Info**: Title, authors, key findings

## Workplan

### Phase 1: Agent Architecture
- [ ] Create `.github/agents/` directory structure
- [ ] Design `arxiv-fetcher.agent.md` - Fetches papers from arXiv API
- [ ] Design `paper-summarizer.agent.md` - Generates key findings from abstracts
- [ ] Design `dashboard-builder.agent.md` - Updates Jekyll pages with paper data
- [ ] Design `pipeline-orchestrator.agent.md` - Coordinates the entire workflow

### Phase 2: Skills Definition
- [ ] Create `.github/skills/` directory structure
- [ ] Design `api-interaction.skill.md` - Skills for working with arXiv API
- [ ] Design `data-processing.skill.md` - Skills for parsing and transforming paper data
- [ ] Design `markdown-generation.skill.md` - Skills for generating Jekyll-compatible content
- [ ] Design `github-deployment.skill.md` - Skills for committing and deploying to GitHub Pages

### Phase 3: Prompts Library
- [ ] Create `.github/prompts/` directory structure (already exists)
- [ ] Design `fetch-papers.prompt.md` - Instructions for fetching arXiv papers
- [ ] Design `summarize-abstract.prompt.md` - Instructions for generating key findings
- [ ] Design `generate-dashboard.prompt.md` - Instructions for creating dashboard HTML/MD
- [ ] Design `deploy-to-pages.prompt.md` - Instructions for GitHub Pages deployment

### Phase 4: Coding Standards
- [ ] Create `coding-style.md` - General coding conventions
- [ ] Create `html-guidelines.md` - HTML/CSS best practices for dashboard
- [ ] Document Jekyll integration requirements
- [ ] Define data schema for paper storage (JSON/YAML)

### Phase 5: GitHub Actions Integration
- [ ] Design workflow file `arxiv-pipeline.yml` for hourly execution
- [ ] Configure GitHub Pages deployment from gh-pages branch
- [ ] Set up environment variables and secrets (if needed)
- [ ] Define failure notification strategy

### Phase 6: Dashboard Design
- [ ] Design dashboard layout in Jekyll
- [ ] Create `_pages/arxiv-feed.md` for displaying papers
- [ ] Design paper card component in `_includes/paper-card.html`
- [ ] Add navigation link to main site
- [ ] Style dashboard to match site theme

## File Structure
```
.github/
├── agents/
│   ├── arxiv-fetcher.agent.md
│   ├── paper-summarizer.agent.md
│   ├── dashboard-builder.agent.md
│   └── pipeline-orchestrator.agent.md
├── skills/
│   ├── api-interaction.skill.md
│   ├── data-processing.skill.md
│   ├── markdown-generation.skill.md
│   └── github-deployment.skill.md
├── prompts/
│   ├── fetch-papers.prompt.md
│   ├── summarize-abstract.prompt.md
│   ├── generate-dashboard.prompt.md
│   └── deploy-to-pages.prompt.md
├── coding-style.md
├── html-guidelines.md
└── workflows/
    └── arxiv-pipeline.yml
```

## Notes & Considerations

### arXiv API Details
- Base URL: `http://export.arxiv.org/api/query`
- Query format: `search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10`
- Rate limiting: 3 seconds between requests
- Response format: Atom XML

### Agent Format Requirements
All agents must follow Copilot CLI format:
- File naming: `*.agent.md`
- YAML front matter with:
  - `type`: Agent type (task, explore, code-review, general-purpose)
  - `model`: Model to use (claude-sonnet-4.5, claude-haiku-4.5, etc.)
  - `tools`: List of available tools
- Reference: https://code.visualstudio.com/docs/copilot/customization/custom-agents

### Jekyll Integration
- Papers stored as data files in `_data/arxiv_papers.yml`
- Dashboard page at `_pages/arxiv-feed.md`
- Use existing site theme and layout system
- Ensure compatibility with GitHub Pages supported plugins

### Deployment Strategy
- Use GitHub Actions workflow for automated execution
- Commit updates to `gh-pages` branch
- Configure repository settings: Settings → Pages → Deploy from branch → gh-pages
- No manual intervention required after initial setup

### Key Findings Generation
- Extract main contributions from abstract
- Identify methodology if mentioned
- Highlight novel aspects
- Keep summaries concise (2-3 sentences)

### Error Handling
- API failures: Retry with exponential backoff
- Parse errors: Log and skip problematic papers
- Deployment failures: Notify via GitHub Actions status
- Maintain last-known-good state if update fails
