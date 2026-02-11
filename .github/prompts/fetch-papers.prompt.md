# Fetch arXiv Papers Prompt

Instructions for the arXiv Fetcher Agent to retrieve the latest AI papers.

## Objective
Fetch the 10 most recent papers from arXiv in the cs.AI (Artificial Intelligence) category and store them in `_data/arxiv_papers.yml`.

## Step-by-Step Instructions

### Step 1: Make API Request
```bash
curl -s "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10" \
  -o /tmp/arxiv_response.xml
```

**What to check:**
- Response saved to `/tmp/arxiv_response.xml`
- File is not empty
- File contains valid XML

### Step 2: Parse XML Response
Extract the following fields from each `<entry>`:
- **ID**: From `<id>` tag, extract paper ID (e.g., `2401.12345`)
  - Example: `http://arxiv.org/abs/2401.12345v1` → Extract `2401.12345`
- **Title**: From `<title>` tag, clean whitespace and newlines
- **Authors**: From all `<author><name>` tags, join with commas
- **Abstract**: From `<summary>` tag, clean whitespace
- **Published Date**: From `<published>` tag, format as `YYYY-MM-DD`
- **PDF URL**: Construct as `http://arxiv.org/pdf/{paper_id}`
- **arXiv URL**: Construct as `http://arxiv.org/abs/{paper_id}`

### Step 3: Create YAML File
Generate `_data/arxiv_papers.yml` with this structure:

```yaml
papers:
  - id: "2401.12345"
    title: "Advances in Large Language Models"
    authors: "John Doe, Jane Smith"
    abstract: "We present a novel approach to..."
    published: "2024-01-15"
    pdf_url: "http://arxiv.org/pdf/2401.12345"
    arxiv_url: "http://arxiv.org/abs/2401.12345"
    key_findings: ""
  - id: "2401.12346"
    title: "Another Paper Title"
    ...
```

**Important:**
- Leave `key_findings: ""` empty (will be filled by summarizer)
- Ensure valid YAML syntax (proper indentation, quotes around strings)
- Sort papers by published date (newest first)

### Step 4: Validate Output
Check that:
- `_data/arxiv_papers.yml` exists
- Contains exactly 10 papers (or fewer if less available)
- All required fields present for each paper
- Valid YAML syntax (no errors when parsed)

## Error Handling

### If API Request Fails
1. Wait 5 seconds
2. Retry once
3. If still fails, create empty file:
   ```yaml
   papers: []
   ```

### If XML Parse Fails
- Log error message
- Skip malformed entries
- Continue with successfully parsed papers

### If No Papers Found
- Create file with empty list:
  ```yaml
  papers: []
  ```

## Example Python Script

```python
#!/usr/bin/env python3
import requests
import xml.etree.ElementTree as ET
import yaml

# Fetch papers
response = requests.get(
    "http://export.arxiv.org/api/query",
    params={
        "search_query": "cat:cs.AI",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": 10
    }
)

# Parse XML
root = ET.fromstring(response.content)
ns = {'atom': 'http://www.w3.org/2005/Atom'}

papers = []
for entry in root.findall('atom:entry', ns):
    paper_id = entry.find('atom:id', ns).text.split('/')[-1].split('v')[0]
    
    papers.append({
        'id': paper_id,
        'title': entry.find('atom:title', ns).text.strip().replace('\n', ' '),
        'authors': ', '.join([a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]),
        'abstract': entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
        'published': entry.find('atom:published', ns).text[:10],
        'pdf_url': f"http://arxiv.org/pdf/{paper_id}",
        'arxiv_url': f"http://arxiv.org/abs/{paper_id}",
        'key_findings': ''
    })

# Write YAML
with open('_data/arxiv_papers.yml', 'w') as f:
    yaml.dump({'papers': papers}, f, default_flow_style=False, allow_unicode=True)

print(f"✓ Fetched {len(papers)} papers")
```

## Success Criteria
- ✅ File `_data/arxiv_papers.yml` created
- ✅ Contains 10 papers from cs.AI
- ✅ All required fields populated
- ✅ Valid YAML format
- ✅ Papers sorted by date (newest first)

## Expected Output
```
Fetching papers from arXiv API...
✓ Retrieved 10 papers from cs.AI category
✓ Parsed XML successfully
✓ Created _data/arxiv_papers.yml
✓ Validation passed
```
