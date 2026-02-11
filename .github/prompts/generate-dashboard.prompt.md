# Generate Dashboard Prompt

Instructions for the Dashboard Builder Agent to create the arXiv paper feed page.

## Objective
Create a Jekyll-based dashboard that displays the latest papers from `_data/arxiv_papers.yml` with a clean, responsive design.

## Step-by-Step Instructions

### Step 1: Create Dashboard Page

Create `_pages/arxiv-feed.md`:

```markdown
---
layout: archive
title: "Latest AI Research from arXiv"
permalink: /arxiv-feed/
author_profile: true
---

<div class="arxiv-feed">
  <p class="feed-intro">
    Displaying the 10 most recent papers from the <strong>cs.AI</strong> (Artificial Intelligence) category, 
    updated hourly via automated pipeline.
  </p>
  
  <p class="feed-updated">
    Last updated: <time datetime="{{ site.time | date_to_xmlschema }}">
      {{ site.time | date: "%B %d, %Y at %I:%M %p UTC" }}
    </time>
  </p>
  
  {% if site.data.arxiv_papers.papers.size > 0 %}
    <div class="papers-container">
      {% for paper in site.data.arxiv_papers.papers %}
        {% include paper-card.html paper=paper %}
      {% endfor %}
    </div>
  {% else %}
    <div class="no-papers">
      <p>📄 No papers available yet. Check back soon!</p>
    </div>
  {% endif %}
</div>
```

### Step 2: Create Paper Card Component

Create `_includes/paper-card.html`:

```html
<article class="paper-card">
  <header class="paper-header">
    <h3 class="paper-title">
      <a href="{{ include.paper.arxiv_url }}" target="_blank" rel="noopener noreferrer">
        {{ include.paper.title }}
      </a>
    </h3>
    
    <div class="paper-meta">
      <span class="paper-id">{{ include.paper.id }}</span>
      <span class="paper-date">{{ include.paper.published | date: "%b %d, %Y" }}</span>
    </div>
  </header>
  
  <div class="paper-authors">
    <strong>Authors:</strong> {{ include.paper.authors }}
  </div>
  
  <div class="paper-content">
    {% if include.paper.key_findings and include.paper.key_findings != "" %}
      <p class="paper-findings">{{ include.paper.key_findings }}</p>
    {% else %}
      <p class="paper-abstract">{{ include.paper.abstract | truncate: 200 }}</p>
    {% endif %}
  </div>
  
  <footer class="paper-actions">
    <a href="{{ include.paper.arxiv_url }}" class="btn btn-primary" target="_blank" rel="noopener noreferrer">
      View on arXiv
    </a>
    <a href="{{ include.paper.pdf_url }}" class="btn btn-secondary" target="_blank" rel="noopener noreferrer">
      Download PDF
    </a>
  </footer>
</article>
```

### Step 3: Add Navigation Link

Update `_data/navigation.yml` to add the arXiv feed to the main navigation:

```yaml
main:
  - title: "Publications"
    url: /publications/
  - title: "Talks"
    url: /talks/
  - title: "Teaching"
    url: /teaching/
  - title: "arXiv Feed"
    url: /arxiv-feed/
  - title: "CV"
    url: /cv/
```

**Important:** Only add if not already present.

### Step 4: Add Custom Styles (Optional)

If the theme doesn't provide sufficient styling, create `_sass/_arxiv-feed.scss`:

```scss
.arxiv-feed {
  max-width: 900px;
  margin: 0 auto;
  padding: 1em;
  
  .feed-intro {
    font-size: 1.1em;
    line-height: 1.6;
    margin-bottom: 1em;
  }
  
  .feed-updated {
    color: #666;
    font-size: 0.9em;
    font-style: italic;
    margin-bottom: 2em;
    text-align: right;
  }
}

.papers-container {
  display: grid;
  gap: 2em;
}

.paper-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5em;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
  
  &:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transform: translateY(-2px);
  }
}

.paper-header {
  margin-bottom: 1em;
  
  .paper-title {
    margin: 0 0 0.5em 0;
    font-size: 1.3em;
    line-height: 1.3;
    
    a {
      color: #2c3e50;
      text-decoration: none;
      
      &:hover {
        color: #0066cc;
        text-decoration: underline;
      }
    }
  }
  
  .paper-meta {
    display: flex;
    gap: 1em;
    font-size: 0.85em;
    color: #666;
    
    .paper-id {
      font-family: monospace;
      background: #f5f5f5;
      padding: 0.2em 0.5em;
      border-radius: 3px;
    }
  }
}

.paper-authors {
  margin-bottom: 1em;
  font-size: 0.9em;
  color: #555;
}

.paper-content {
  margin-bottom: 1.5em;
  line-height: 1.6;
  
  .paper-findings {
    font-style: italic;
    background: #f9f9f9;
    padding: 1em;
    border-left: 3px solid #0066cc;
    border-radius: 0 4px 4px 0;
  }
  
  .paper-abstract {
    color: #666;
  }
}

.paper-actions {
  display: flex;
  gap: 0.75em;
  
  .btn {
    padding: 0.6em 1.2em;
    text-decoration: none;
    border-radius: 4px;
    font-size: 0.9em;
    font-weight: 500;
    transition: all 0.2s;
    
    &-primary {
      background: #0066cc;
      color: white;
      
      &:hover {
        background: #0052a3;
      }
    }
    
    &-secondary {
      background: #f0f0f0;
      color: #333;
      border: 1px solid #ddd;
      
      &:hover {
        background: #e0e0e0;
      }
    }
  }
}

.no-papers {
  text-align: center;
  padding: 4em 2em;
  color: #999;
  font-size: 1.1em;
}

// Responsive design
@media (max-width: 768px) {
  .paper-card {
    padding: 1em;
  }
  
  .paper-header .paper-title {
    font-size: 1.1em;
  }
  
  .paper-actions {
    flex-direction: column;
    
    .btn {
      text-align: center;
      width: 100%;
    }
  }
}
```

Then import in `_sass/main.scss` or `assets/css/main.scss`:
```scss
@import "arxiv-feed";
```

## Design Requirements

### Visual Hierarchy
1. **Title** - Large, prominent, clickable
2. **Metadata** - Paper ID, date (small, subtle)
3. **Authors** - Clear but not dominant
4. **Key Findings** - Highlighted (background color, border)
5. **Actions** - Clear call-to-action buttons

### Color Scheme
- Use existing theme colors for consistency
- Primary action: Blue (#0066cc)
- Secondary action: Gray (#f0f0f0)
- Borders: Light gray (#e0e0e0)
- Background: White (#fff)

### Spacing
- Card padding: 1.5em
- Gap between cards: 2em
- Button gap: 0.75em
- Line height: 1.6 for readability

### Responsive Breakpoints
- Desktop (> 768px): Single column, wide cards
- Mobile (≤ 768px): Stacked buttons, reduced padding

## Testing Checklist

### Functionality
- [ ] Dashboard page loads without errors
- [ ] All 10 papers display
- [ ] Links to arXiv work (open in new tab)
- [ ] PDF links work (open in new tab)
- [ ] Navigation link appears in header

### Visual Design
- [ ] Cards have proper spacing
- [ ] Typography is readable
- [ ] Colors match site theme
- [ ] Key findings are visually distinct
- [ ] Buttons are clearly clickable

### Responsive Design
- [ ] Layout works on desktop (1920px)
- [ ] Layout works on tablet (768px)
- [ ] Layout works on mobile (375px)
- [ ] Buttons stack on mobile
- [ ] Text is readable on all sizes

### Accessibility
- [ ] Semantic HTML (article, header, footer)
- [ ] Links have meaningful text
- [ ] Sufficient color contrast (4.5:1 minimum)
- [ ] Keyboard navigation works
- [ ] Screen reader compatible

## Error Handling

### No Papers Available
Display friendly message:
```html
<div class="no-papers">
  <p>📄 No papers available yet. Check back soon!</p>
</div>
```

### Missing Key Findings
Fall back to abstract:
```liquid
{% if include.paper.key_findings and include.paper.key_findings != "" %}
  <p class="paper-findings">{{ include.paper.key_findings }}</p>
{% else %}
  <p class="paper-abstract">{{ include.paper.abstract | truncate: 200 }}</p>
{% endif %}
```

### Missing Authors
```liquid
{{ include.paper.authors | default: "Authors not listed" }}
```

## Success Criteria
- ✅ Page accessible at `/arxiv-feed/`
- ✅ All papers displayed correctly
- ✅ Links functional (arXiv and PDF)
- ✅ Responsive design working
- ✅ Navigation link added
- ✅ No console errors
- ✅ Matches site theme

## Expected Output
```
Creating dashboard components...
✓ Created _pages/arxiv-feed.md
✓ Created _includes/paper-card.html
✓ Updated _data/navigation.yml
✓ Dashboard ready at /arxiv-feed/
```
