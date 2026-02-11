# Markdown Generation Skill

Skills for generating Jekyll-compatible Markdown content and HTML components.

## Core Competencies

### 1. Jekyll Page Front Matter

#### Basic Page Structure
```markdown
---
layout: archive
title: "arXiv AI Feed"
permalink: /arxiv-feed/
author_profile: true
---

Content goes here...
```

#### Front Matter Fields
- `layout`: Template to use (archive, single, default)
- `title`: Page title (shows in header)
- `permalink`: URL path (must start and end with /)
- `author_profile`: Show sidebar (true/false)
- `toc`: Show table of contents (true/false)
- `date`: Page date (YYYY-MM-DD)

### 2. Liquid Templating

#### Accessing Data Files
```liquid
{% for paper in site.data.arxiv_papers.papers %}
  <h3>{{ paper.title }}</h3>
  <p>{{ paper.authors }}</p>
{% endfor %}
```

#### Conditional Logic
```liquid
{% if paper.key_findings != "" %}
  <p>{{ paper.key_findings }}</p>
{% else %}
  <p>{{ paper.abstract | truncate: 200 }}</p>
{% endif %}
```

#### Filters
```liquid
{{ paper.title | capitalize }}
{{ paper.abstract | truncate: 200 }}
{{ paper.published | date: "%B %d, %Y" }}
{{ paper.authors | split: ", " | size }}
```

#### Includes
```liquid
{% include paper-card.html paper=paper %}
```

### 3. HTML Component Design

#### Paper Card Component (`_includes/paper-card.html`)
```html
<div class="paper-card">
  <h3 class="paper-title">
    <a href="{{ include.paper.arxiv_url }}" target="_blank" rel="noopener">
      {{ include.paper.title }}
    </a>
  </h3>
  
  <p class="paper-meta">
    <span class="paper-authors">{{ include.paper.authors }}</span>
    <span class="paper-date">{{ include.paper.published | date: "%b %d, %Y" }}</span>
  </p>
  
  {% if include.paper.key_findings != "" %}
    <p class="paper-findings">{{ include.paper.key_findings }}</p>
  {% else %}
    <p class="paper-abstract">{{ include.paper.abstract | truncate: 200 }}</p>
  {% endif %}
  
  <div class="paper-links">
    <a href="{{ include.paper.arxiv_url }}" class="btn btn--primary" target="_blank">View on arXiv</a>
    <a href="{{ include.paper.pdf_url }}" class="btn btn--secondary" target="_blank">Download PDF</a>
  </div>
</div>
```

### 4. Dashboard Page Template

#### Full Page Example (`_pages/arxiv-feed.md`)
```markdown
---
layout: archive
title: "Latest AI Research from arXiv"
permalink: /arxiv-feed/
author_profile: true
---

<div class="arxiv-feed">
  <p class="feed-intro">
    Displaying the 10 most recent papers from the <strong>cs.AI</strong> category, 
    updated hourly via automated pipeline.
  </p>
  
  <p class="feed-updated">
    Last updated: <time datetime="{{ site.time | date_to_xmlschema }}">
      {{ site.time | date: "%B %d, %Y at %I:%M %p UTC" }}
    </time>
  </p>
  
  {% if site.data.arxiv_papers.papers.size > 0 %}
    <div class="papers-grid">
      {% for paper in site.data.arxiv_papers.papers %}
        {% include paper-card.html paper=paper %}
      {% endfor %}
    </div>
  {% else %}
    <div class="no-papers">
      <p>No papers available yet. Check back soon!</p>
    </div>
  {% endif %}
</div>
```

### 5. CSS Styling (Optional Custom Styles)

If custom styling is needed beyond theme defaults:

```scss
// _sass/_arxiv-feed.scss
.arxiv-feed {
  max-width: 900px;
  margin: 0 auto;
  
  .feed-intro {
    font-size: 1.1em;
    margin-bottom: 1em;
  }
  
  .feed-updated {
    color: #666;
    font-size: 0.9em;
    margin-bottom: 2em;
  }
}

.papers-grid {
  display: grid;
  gap: 2em;
}

.paper-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5em;
  background: #fff;
  transition: box-shadow 0.2s;
  
  &:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }
  
  .paper-title {
    margin-top: 0;
    font-size: 1.3em;
    
    a {
      color: #2c3e50;
      text-decoration: none;
      
      &:hover {
        color: #0066cc;
      }
    }
  }
  
  .paper-meta {
    color: #666;
    font-size: 0.9em;
    margin-bottom: 1em;
    
    .paper-date {
      margin-left: 1em;
      &:before {
        content: "•";
        margin-right: 0.5em;
      }
    }
  }
  
  .paper-findings,
  .paper-abstract {
    line-height: 1.6;
    margin-bottom: 1em;
  }
  
  .paper-links {
    display: flex;
    gap: 0.5em;
    
    .btn {
      padding: 0.5em 1em;
      text-decoration: none;
      border-radius: 4px;
      font-size: 0.9em;
      
      &--primary {
        background: #0066cc;
        color: white;
      }
      
      &--secondary {
        background: #f0f0f0;
        color: #333;
      }
    }
  }
}

.no-papers {
  text-align: center;
  padding: 3em;
  color: #999;
}
```

### 6. Navigation Configuration

#### Add to `_data/navigation.yml`
```yaml
main:
  - title: "Publications"
    url: /publications/
  - title: "Talks"
    url: /talks/
  - title: "arXiv Feed"  # New entry
    url: /arxiv-feed/
  - title: "CV"
    url: /cv/
```

### 7. Responsive Design Considerations

```html
<!-- Mobile-friendly meta tags -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Responsive image -->
<img src="image.jpg" 
     srcset="image-320w.jpg 320w, image-640w.jpg 640w"
     alt="Description">

<!-- Responsive grid -->
<style>
.papers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2em;
}

@media (max-width: 768px) {
  .papers-grid {
    grid-template-columns: 1fr;
  }
  
  .paper-links {
    flex-direction: column;
  }
}
</style>
```

## Jekyll Best Practices

1. **Use existing layouts**: Leverage `archive`, `single`, `default` layouts from theme
2. **Consistent permalinks**: Always use format `/path/` (leading and trailing slashes)
3. **Data files**: Store structured data in `_data/` directory (YAML, JSON, CSV)
4. **Includes**: Create reusable components in `_includes/`
5. **Front matter**: Always include at minimum `layout`, `title`, `permalink`

## Liquid Best Practices

1. **Safe navigation**: Use `| default: "fallback"` for missing values
2. **Escape output**: Use `{{ var | escape }}` for user-generated content
3. **Performance**: Minimize loops, cache expensive operations
4. **Readability**: Add whitespace, use meaningful variable names

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Page not showing | Check permalink format, ensure front matter present |
| Data not loading | Verify file path in `site.data.file_name` |
| Include not found | Check file exists in `_includes/` directory |
| Liquid syntax error | Validate with `{% raw %}...{% endraw %}` for literal display |
| CSS not applying | Check `_sass/` directory, ensure imported in main SCSS |

## Testing Checklist

- [ ] Page renders without errors
- [ ] All Liquid tags resolve correctly
- [ ] Links work (internal and external)
- [ ] Responsive on mobile (< 768px width)
- [ ] Accessible (semantic HTML, ARIA labels)
- [ ] Fast load time (< 3 seconds)
