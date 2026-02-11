# Data Processing Skill

Skills for parsing, transforming, and storing arXiv paper data.

## Core Competencies

### 1. XML to YAML Conversion

#### Using Python
```python
import xml.etree.ElementTree as ET
import yaml
from datetime import datetime

def parse_arxiv_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    papers = []
    
    for entry in root.findall('atom:entry', ns):
        # Extract ID (remove version)
        id_url = entry.find('atom:id', ns).text
        paper_id = id_url.split('/')[-1].split('v')[0]
        
        # Extract title (clean whitespace)
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        
        # Extract authors
        authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
        authors_str = ', '.join(authors)
        
        # Extract abstract
        abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
        
        # Extract published date
        published = entry.find('atom:published', ns).text[:10]  # YYYY-MM-DD
        
        # Extract links
        pdf_url = f"http://arxiv.org/pdf/{paper_id}"
        arxiv_url = f"http://arxiv.org/abs/{paper_id}"
        
        papers.append({
            'id': paper_id,
            'title': title,
            'authors': authors_str,
            'abstract': abstract,
            'published': published,
            'pdf_url': pdf_url,
            'arxiv_url': arxiv_url,
            'key_findings': ''
        })
    
    return {'papers': papers}

# Usage
data = parse_arxiv_xml('response.xml')
with open('_data/arxiv_papers.yml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
```

### 2. YAML File Operations

#### Reading YAML
```python
import yaml

with open('_data/arxiv_papers.yml', 'r') as f:
    data = yaml.safe_load(f)
    
for paper in data['papers']:
    print(f"Title: {paper['title']}")
    print(f"Authors: {paper['authors']}")
```

#### Updating YAML (Preserving Structure)
```python
import yaml

# Read existing data
with open('_data/arxiv_papers.yml', 'r') as f:
    data = yaml.safe_load(f)

# Update key findings
for paper in data['papers']:
    if not paper.get('key_findings'):
        paper['key_findings'] = generate_summary(paper['abstract'])

# Write back with formatting
with open('_data/arxiv_papers.yml', 'w') as f:
    yaml.dump(data, f, 
              default_flow_style=False,
              allow_unicode=True,
              sort_keys=False,
              indent=2)
```

### 3. Text Processing

#### Clean Text (Remove Extra Whitespace)
```python
import re

def clean_text(text):
    # Remove newlines and extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Trim whitespace
    text = text.strip()
    return text

# Example
abstract = clean_text(paper['abstract'])
```

#### Truncate Text
```python
def truncate(text, max_length=200, suffix='...'):
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + suffix

# Example
short_abstract = truncate(abstract, 200)
```

### 4. Date Formatting
```python
from datetime import datetime

# Parse ISO 8601
date_str = "2024-01-15T12:00:00Z"
dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

# Format for display
formatted = dt.strftime("%B %d, %Y")  # "January 15, 2024"
```

### 5. Data Validation

#### Validate Paper Data
```python
def validate_paper(paper):
    required_fields = ['id', 'title', 'authors', 'abstract', 'published', 'pdf_url', 'arxiv_url']
    
    for field in required_fields:
        if field not in paper or not paper[field]:
            return False, f"Missing or empty field: {field}"
    
    # Validate date format
    try:
        datetime.strptime(paper['published'], '%Y-%m-%d')
    except ValueError:
        return False, "Invalid date format"
    
    # Validate URLs
    if not paper['pdf_url'].startswith('http'):
        return False, "Invalid PDF URL"
    
    return True, "Valid"

# Usage
for paper in papers:
    valid, msg = validate_paper(paper)
    if not valid:
        print(f"Paper {paper.get('id', 'UNKNOWN')}: {msg}")
```

### 6. Deduplication
```python
def deduplicate_papers(papers):
    seen_ids = set()
    unique_papers = []
    
    for paper in papers:
        if paper['id'] not in seen_ids:
            seen_ids.add(paper['id'])
            unique_papers.append(paper)
    
    return unique_papers
```

### 7. Sorting & Filtering
```python
# Sort by published date (newest first)
papers_sorted = sorted(papers, 
                       key=lambda p: p['published'], 
                       reverse=True)

# Filter by date range
from datetime import datetime, timedelta

cutoff_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
recent_papers = [p for p in papers if p['published'] >= cutoff_date]

# Take top N
top_10 = papers_sorted[:10]
```

## YAML Best Practices

### Good YAML Structure
```yaml
papers:
  - id: "2401.12345"
    title: "Multi-line titles should be on one line in YAML"
    authors: "Author One, Author Two"
    abstract: "Long abstracts should also be on one line, or use YAML multiline syntax"
    published: "2024-01-15"
    pdf_url: "http://arxiv.org/pdf/2401.12345"
    arxiv_url: "http://arxiv.org/abs/2401.12345"
    key_findings: "Summary goes here."
```

### Multiline Strings (if needed)
```yaml
papers:
  - id: "2401.12345"
    abstract: >
      This is a long abstract that spans multiple lines.
      The > symbol makes it a folded scalar, joining lines with spaces.
```

## Error Handling Patterns

```python
def safe_parse(xml_file):
    try:
        tree = ET.parse(xml_file)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {xml_file}")
        return None

def safe_write_yaml(data, filepath):
    try:
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        return True
    except Exception as e:
        print(f"Failed to write YAML: {e}")
        return False
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| YAML syntax error | Validate with `yaml.safe_load()` before writing |
| Unicode characters | Use `allow_unicode=True` in `yaml.dump()` |
| Newlines in text | Replace `\n` with spaces: `text.replace('\n', ' ')` |
| Missing fields | Provide defaults: `paper.get('field', 'N/A')` |
| Duplicate papers | Use deduplication based on paper ID |
