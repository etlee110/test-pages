# Academic Pages - Copilot Instructions

This is a Jekyll-based academic portfolio website template built on the Minimal Mistakes theme.

## Development Commands

### Local Development
```bash
# Install dependencies (first time setup)
bundle install

# Run Jekyll server with live reload
jekyll serve -l -H localhost
# OR with bundler to ensure correct dependencies
bundle exec jekyll serve -l -H localhost

# If you encounter permission errors during bundle install:
bundle config set --local path 'vendor/bundle'
bundle install
```

### Docker Development
```bash
# Make files writable and start container
chmod -R 777 .
docker compose up

# Access site at http://localhost:4000
```

### JavaScript Build
```bash
# Minify and concatenate JavaScript
npm run build:js

# Watch for changes and auto-build
npm run watch:js
```

## Architecture

### Jekyll Collections
The site uses Jekyll collections to organize different content types:
- `_pages/` - Static pages (about, cv, etc.)
- `_posts/` - Blog posts
- `_portfolio/` - Portfolio items
- `_publications/` - Academic publications
- `_talks/` - Conference talks and presentations
- `_teaching/` - Teaching materials

### Key Directories
- `_includes/` - Reusable HTML partials (author profile, navigation, comments, analytics)
- `_layouts/` - Page templates that wrap content
- `_sass/` - SCSS stylesheets organized by component
- `_data/` - YAML data files for navigation and configuration
- `assets/` - Compiled CSS, JavaScript, images
- `files/` - Static files (PDFs, etc.) served directly at `/files/`

### Configuration Files
- `_config.yml` - Main Jekyll site configuration (use this for local development)
- `_config_docker.yml` - Docker-specific overrides
- Site settings include themes (default, air, sunrise, mint, dirt, contrast)

### Markdown Generators
The `markdown_generator/` directory contains tools to bulk-generate content from structured data:
- `publications.py` - Generate publication pages from CSV/TSV
- `talks.py` - Generate talk pages from TSV
- `pubsFromBib.py` - Import publications from BibTeX
- Jupyter notebooks (`.ipynb`) provide the same functionality with more documentation

**Usage**: `python3 publications.py publications.csv`

### Layouts and Templates
Common layouts in `_layouts/`:
- `default.html` - Base template with header/footer
- `single.html` - Single page/post layout
- `archive.html` - Collection/archive listings
- `cv.html` - CV page with timeline

Important includes:
- `author-profile.html` - Sidebar bio/social links
- `archive-single.html` - Individual item in archive list
- `cv-template.html` - Structured CV sections

## Conventions

### Front Matter
All content files require YAML front matter with at minimum:
```yaml
---
layout: archive  # or single, default, etc.
title: "Page Title"
permalink: /path/
---
```

Collections often use additional fields:
- Publications: `venue`, `date`, `paperurl`, `citation`
- Talks: `venue`, `date`, `location`, `type` (Talk/Tutorial/Workshop)
- Portfolio: `excerpt`, `collection`, `date`

### Content Updates
1. Profile/bio: Edit `_config.yml` under `author:` section
2. Navigation: Modify `_data/navigation.yml`
3. Add static pages: Create `.md` files in `_pages/` with appropriate front matter
4. Bulk import: Use scripts in `markdown_generator/` for publications/talks

### Theme Customization
- Change site theme: Edit `site_theme` in `_config.yml` (default, air, sunrise, mint, dirt, contrast)
- Custom styles: Add to `_sass/` directory
- Override includes: Create file with same name in `_includes/`

### GitHub Pages Deployment
This template is designed for GitHub Pages deployment at `[username].github.io`. The site builds automatically on push. Check deployment status in repository Settings > Pages.

**Important**: Changes to `_config.yml` require restarting the Jekyll server - they are NOT reloaded automatically.

## Scripts

- `scripts/cv_markdown_to_json.py` - Convert CV markdown to JSON format
- `scripts/update_cv_json.sh` - Update CV JSON file

## DevContainer
VS Code users can use the included DevContainer configuration (F1 → "Dev Containers: Reopen in Container") for a pre-configured development environment with Jekyll and dependencies.
