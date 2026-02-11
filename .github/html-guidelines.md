# HTML & CSS Guidelines

Best practices for HTML and CSS in the arXiv Feed Dashboard.

## HTML

### Document Structure

#### Semantic HTML
Use appropriate semantic elements:

```html
<!-- Good: Semantic structure -->
<article class="paper-card">
  <header class="paper-header">
    <h3 class="paper-title">Title</h3>
  </header>
  
  <section class="paper-content">
    <p>Content...</p>
  </section>
  
  <footer class="paper-actions">
    <a href="...">Link</a>
  </footer>
</article>

<!-- Bad: Divitis -->
<div class="paper-card">
  <div class="paper-header">
    <div class="paper-title">Title</div>
  </div>
  <div class="paper-content">
    <div>Content...</div>
  </div>
</div>
```

#### HTML5 Elements
- `<header>` - Page/section header
- `<nav>` - Navigation
- `<main>` - Main content
- `<article>` - Self-contained content
- `<section>` - Thematic grouping
- `<aside>` - Sidebar content
- `<footer>` - Page/section footer
- `<time>` - Dates/times

### Attributes

#### Required Attributes
```html
<!-- Images -->
<img src="image.jpg" alt="Descriptive text">

<!-- Links (external) -->
<a href="https://arxiv.org/..." target="_blank" rel="noopener noreferrer">
  Link text
</a>

<!-- Forms -->
<label for="search">Search:</label>
<input type="text" id="search" name="search">
```

#### Data Attributes
```html
<!-- Use data-* for custom attributes -->
<article class="paper-card" data-paper-id="2401.12345" data-category="cs.AI">
  ...
</article>
```

### Accessibility

#### ARIA Labels
```html
<!-- Button without visible text -->
<button aria-label="Close dialog">
  <span class="icon-close"></span>
</button>

<!-- Navigation landmark -->
<nav aria-label="Main navigation">
  <ul>...</ul>
</nav>

<!-- Hidden content -->
<div aria-hidden="true">Decorative element</div>
```

#### Heading Hierarchy
```html
<!-- Good: Proper hierarchy -->
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
    <h3>Subsection</h3>
  <h2>Section</h2>

<!-- Bad: Skipping levels -->
<h1>Page Title</h1>
  <h3>Section</h3>
  <h5>Subsection</h5>
```

#### Focus States
```css
/* Always style focus states */
a:focus,
button:focus {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* Never remove without replacement */
/* Bad */
*:focus {
  outline: none;
}

/* Good alternative */
button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.5);
}
```

### Performance

#### Minimize DOM Depth
```html
<!-- Good: Shallow structure -->
<article class="paper-card">
  <h3 class="paper-title">Title</h3>
  <p class="paper-meta">Authors</p>
  <p class="paper-findings">Findings</p>
</article>

<!-- Bad: Deep nesting -->
<article class="paper-card">
  <div class="paper-wrapper">
    <div class="paper-inner">
      <div class="title-wrapper">
        <h3 class="paper-title">Title</h3>
      </div>
    </div>
  </div>
</article>
```

#### Lazy Loading
```html
<!-- Images below the fold -->
<img src="image.jpg" loading="lazy" alt="Description">
```

## CSS

### Formatting

#### Syntax
```css
/* Good: Consistent formatting */
.paper-card {
  margin: 1em 0;
  padding: 1.5em;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.paper-title {
  margin: 0 0 0.5em;
  font-size: 1.3em;
  line-height: 1.3;
}

/* Bad: Inconsistent formatting */
.paper-card{margin:1em 0;padding:1.5em;border:1px solid #e0e0e0;}
.paper-title{margin:0 0 0.5em;font-size:1.3em;}
```

#### Declaration Order
```css
.element {
  /* Positioning */
  position: relative;
  top: 0;
  left: 0;
  z-index: 10;
  
  /* Display & Box Model */
  display: flex;
  width: 100%;
  padding: 1em;
  margin: 1em 0;
  border: 1px solid #ccc;
  
  /* Typography */
  font-size: 1em;
  line-height: 1.5;
  text-align: center;
  
  /* Visual */
  background: white;
  color: #333;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  
  /* Animation */
  transition: all 0.2s ease;
}
```

### Naming Conventions (BEM)

BEM: Block, Element, Modifier

```css
/* Block */
.paper-card { }

/* Element (child of block) */
.paper-card__title { }
.paper-card__authors { }
.paper-card__actions { }

/* Modifier (variation) */
.paper-card--featured { }
.paper-card--draft { }
.paper-card__title--large { }
```

**Example:**
```html
<article class="paper-card paper-card--featured">
  <h3 class="paper-card__title">Title</h3>
  <p class="paper-card__authors">Authors</p>
  <div class="paper-card__actions">
    <a href="#" class="btn btn--primary">Link</a>
  </div>
</article>
```

```css
.paper-card {
  border: 1px solid #e0e0e0;
  padding: 1.5em;
}

.paper-card--featured {
  border-color: #0066cc;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.paper-card__title {
  font-size: 1.3em;
  margin: 0 0 0.5em;
}

.paper-card__authors {
  color: #666;
}

.paper-card__actions {
  margin-top: 1em;
}
```

### Responsive Design

#### Mobile-First Approach
```css
/* Base: Mobile styles */
.paper-card {
  padding: 1em;
  font-size: 0.9em;
}

/* Tablet and up */
@media (min-width: 768px) {
  .paper-card {
    padding: 1.5em;
    font-size: 1em;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .paper-card {
    padding: 2em;
  }
}
```

#### Responsive Units
```css
/* Use relative units */
.paper-card {
  padding: 1.5em;          /* Relative to font size */
  margin: 2rem 0;          /* Relative to root font size */
  width: 90%;              /* Relative to parent */
  max-width: 900px;        /* Fixed maximum */
  font-size: clamp(0.9em, 2vw, 1.2em);  /* Fluid sizing */
}
```

#### Breakpoints
```css
/* Standard breakpoints */
/* Mobile: < 768px (default) */
/* Tablet: 768px - 1023px */
@media (min-width: 768px) { }

/* Desktop: 1024px+ */
@media (min-width: 1024px) { }

/* Large desktop: 1440px+ */
@media (min-width: 1440px) { }
```

### Colors & Typography

#### Color System
```css
:root {
  /* Primary colors */
  --color-primary: #0066cc;
  --color-primary-dark: #0052a3;
  --color-primary-light: #3385d6;
  
  /* Grayscale */
  --color-text: #2c3e50;
  --color-text-muted: #666;
  --color-border: #e0e0e0;
  --color-bg: #fff;
  --color-bg-alt: #f9f9f9;
  
  /* Semantic */
  --color-success: #28a745;
  --color-warning: #ffc107;
  --color-error: #dc3545;
}

.paper-card {
  color: var(--color-text);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
}

.btn-primary {
  background: var(--color-primary);
}
```

#### Typography Scale
```css
:root {
  --font-size-xs: 0.75rem;   /* 12px */
  --font-size-sm: 0.875rem;  /* 14px */
  --font-size-base: 1rem;    /* 16px */
  --font-size-lg: 1.125rem;  /* 18px */
  --font-size-xl: 1.25rem;   /* 20px */
  --font-size-2xl: 1.5rem;   /* 24px */
  --font-size-3xl: 1.875rem; /* 30px */
}

.paper-title {
  font-size: var(--font-size-xl);
}

.paper-meta {
  font-size: var(--font-size-sm);
}
```

### Spacing

#### Consistent Scale
```css
:root {
  --space-xs: 0.25rem;  /* 4px */
  --space-sm: 0.5rem;   /* 8px */
  --space-md: 1rem;     /* 16px */
  --space-lg: 1.5rem;   /* 24px */
  --space-xl: 2rem;     /* 32px */
  --space-2xl: 3rem;    /* 48px */
}

.paper-card {
  padding: var(--space-lg);
  margin-bottom: var(--space-xl);
  gap: var(--space-md);
}
```

### Performance

#### Efficient Selectors
```css
/* Good: Simple selectors */
.paper-card { }
.paper-title { }

/* Bad: Overly specific */
article.paper-card div.paper-wrapper h3.paper-title { }

/* Bad: Universal selector */
* {
  margin: 0;
  padding: 0;
}

/* Good: Reset specific elements */
h1, h2, h3, p {
  margin: 0;
}
```

#### Animation Performance
```css
/* Good: GPU-accelerated properties */
.paper-card {
  transition: transform 0.2s, opacity 0.2s;
}

.paper-card:hover {
  transform: translateY(-2px);
  opacity: 0.9;
}

/* Bad: Layout-triggering properties */
.paper-card {
  transition: width 0.2s, height 0.2s, margin 0.2s;
}
```

#### Will-Change
```css
/* Use sparingly for animations */
.paper-card:hover {
  will-change: transform;
  transform: translateY(-2px);
}

/* Remove after animation */
.paper-card {
  will-change: auto;
}
```

### Accessibility

#### Color Contrast
Ensure WCAG AA compliance (4.5:1 for normal text, 3:1 for large text):

```css
/* Good: Sufficient contrast */
.paper-title {
  color: #2c3e50;  /* Dark gray on white: 12.6:1 */
  background: #fff;
}

/* Bad: Insufficient contrast */
.paper-meta {
  color: #ccc;  /* Light gray on white: 1.6:1 ❌ */
  background: #fff;
}

/* Good alternative */
.paper-meta {
  color: #666;  /* Medium gray on white: 5.7:1 ✓ */
  background: #fff;
}
```

#### Focus Indicators
```css
/* Visible focus states */
a:focus,
button:focus,
input:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Custom focus ring */
.btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.3);
}
```

### Browser Compatibility

#### Vendor Prefixes (use autoprefixer)
```css
/* Autoprefixer handles this */
.paper-card {
  display: flex;
  transform: translateY(-2px);
}

/* Output with prefixes */
.paper-card {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-transform: translateY(-2px);
  transform: translateY(-2px);
}
```

#### Feature Detection
```css
/* Flexbox with fallback */
.papers-container {
  display: block;  /* Fallback */
}

@supports (display: flex) {
  .papers-container {
    display: flex;
    gap: 2em;
  }
}

/* CSS Grid with fallback */
.papers-grid {
  display: block;  /* Fallback */
}

@supports (display: grid) {
  .papers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2em;
  }
}
```

## Jekyll/Liquid Integration

### Conditional Classes
```liquid
<article class="paper-card {% if paper.featured %}paper-card--featured{% endif %}">
  ...
</article>
```

### Dynamic Styles
```liquid
<div class="paper-meta" style="color: {{ site.theme_color }}">
  ...
</div>
```

### Asset Pipeline
```html
<!-- In Jekyll template -->
<link rel="stylesheet" href="{{ '/assets/css/main.css' | relative_url }}">
<script src="{{ '/assets/js/main.js' | relative_url }}"></script>
```

## Checklist

### HTML
- [ ] Semantic elements used appropriately
- [ ] All images have alt text
- [ ] External links have rel="noopener noreferrer"
- [ ] Form inputs have labels
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] ARIA labels where needed
- [ ] Valid HTML (passes W3C validator)

### CSS
- [ ] Mobile-first responsive design
- [ ] Sufficient color contrast (WCAG AA)
- [ ] Focus states visible
- [ ] Uses relative units (em, rem, %)
- [ ] Follows naming convention (BEM)
- [ ] No !important (unless absolutely necessary)
- [ ] Organized and commented
- [ ] No unused styles

### Performance
- [ ] Minimal DOM depth
- [ ] Efficient selectors
- [ ] GPU-accelerated animations
- [ ] Images lazy loaded
- [ ] CSS minified for production
- [ ] No render-blocking resources

### Accessibility
- [ ] Keyboard navigable
- [ ] Screen reader compatible
- [ ] Color not sole indicator
- [ ] Text is resizable (200%)
- [ ] Skip to content link
- [ ] ARIA landmarks used

### Browser Support
- [ ] Works in Chrome, Firefox, Safari, Edge
- [ ] Graceful degradation for older browsers
- [ ] Tested on mobile devices
- [ ] No console errors
