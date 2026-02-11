# Coding Style Guidelines

General coding conventions for the arXiv Feed Pipeline project.

## Python

### Style Guide
Follow [PEP 8](https://peps.python.org/pep-0008/) - Python Enhancement Proposal 8.

### Formatting
- **Indentation**: 4 spaces (no tabs)
- **Line length**: 79 characters for code, 72 for docstrings/comments
- **Encoding**: UTF-8
- **Imports**: One per line, grouped (standard library, third-party, local)

```python
# Good
import os
import sys
from typing import List, Dict

import requests
import yaml

from local_module import helper

# Bad
import os, sys
from typing import *
```

### Naming Conventions
- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

```python
# Variables and functions
paper_count = 10
max_results = 100

def fetch_papers(category: str) -> List[Dict]:
    pass

# Classes
class ArxivFetcher:
    pass

# Constants
MAX_RETRIES = 3
API_BASE_URL = "http://export.arxiv.org/api/query"

# Private
_internal_cache = {}
```

### Docstrings
Use Google-style docstrings:

```python
def parse_arxiv_response(xml_content: str) -> List[Dict]:
    """Parse arXiv API XML response into structured paper data.
    
    Args:
        xml_content: Raw XML string from arXiv API.
    
    Returns:
        List of paper dictionaries with keys: id, title, authors, abstract,
        published, pdf_url, arxiv_url, key_findings.
    
    Raises:
        XMLParseError: If XML is malformed.
        ValueError: If required fields are missing.
    
    Example:
        >>> xml = fetch_arxiv_api()
        >>> papers = parse_arxiv_response(xml)
        >>> print(papers[0]['title'])
        'Advances in Transformers'
    """
    pass
```

### Type Hints
Use type hints for all function signatures:

```python
from typing import List, Dict, Optional

def fetch_papers(
    category: str,
    max_results: int = 10,
    sort_by: str = "submittedDate"
) -> List[Dict[str, str]]:
    """Fetch papers from arXiv."""
    pass

def get_paper_by_id(paper_id: str) -> Optional[Dict]:
    """Get paper by ID, returns None if not found."""
    pass
```

### Error Handling
- Use specific exceptions
- Handle errors at appropriate level
- Always provide context

```python
# Good
try:
    papers = fetch_papers("cs.AI")
except requests.HTTPError as e:
    logger.error(f"Failed to fetch papers: {e}")
    return []
except ValueError as e:
    logger.error(f"Invalid response format: {e}")
    return []

# Bad
try:
    papers = fetch_papers("cs.AI")
except:
    return []
```

### Logging
Use Python's logging module:

```python
import logging

logger = logging.getLogger(__name__)

def fetch_papers(category: str) -> List[Dict]:
    logger.info(f"Fetching papers from category: {category}")
    
    try:
        response = make_api_call(category)
        logger.debug(f"Received {len(response)} papers")
        return response
    except Exception as e:
        logger.error(f"Failed to fetch papers: {e}", exc_info=True)
        raise
```

### Code Organization
```python
# 1. Module docstring
"""Module for fetching and parsing arXiv papers."""

# 2. Imports (grouped)
import os
import sys

import requests
import yaml

# 3. Constants
API_BASE_URL = "http://export.arxiv.org/api/query"
MAX_RETRIES = 3

# 4. Helper functions
def _clean_text(text: str) -> str:
    """Private helper function."""
    pass

# 5. Main functions/classes
def fetch_papers(category: str) -> List[Dict]:
    """Public API function."""
    pass

class ArxivFetcher:
    """Main fetcher class."""
    pass

# 6. Main execution
if __name__ == "__main__":
    main()
```

## Bash

### Style Guide
Follow [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html).

### Formatting
- **Indentation**: 2 spaces
- **Line length**: 80 characters
- **Shebang**: `#!/bin/bash`

```bash
#!/bin/bash
# Good script structure

set -euo pipefail  # Exit on error, undefined vars, pipe failures

readonly API_URL="http://export.arxiv.org/api/query"
readonly OUTPUT_FILE="_data/arxiv_papers.yml"

function fetch_papers() {
  local category="$1"
  local max_results="${2:-10}"
  
  curl -s "${API_URL}?search_query=cat:${category}&max_results=${max_results}"
}

function main() {
  if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <category>" >&2
    exit 1
  fi
  
  fetch_papers "$1"
}

main "$@"
```

### Error Handling
```bash
# Check command success
if ! command -v curl &> /dev/null; then
    echo "Error: curl not found" >&2
    exit 1
fi

# Check file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: Config file not found: $CONFIG_FILE" >&2
    exit 1
fi
```

## YAML

### Formatting
- **Indentation**: 2 spaces
- **Quotes**: Use quotes for strings with special chars
- **Lists**: Use `-` for list items
- **No tabs**: Always use spaces

```yaml
# Good
papers:
  - id: "2401.12345"
    title: "Paper Title"
    authors: "Author One, Author Two"
    published: "2024-01-15"
    key_findings: ""

# Bad
papers:
- id: 2401.12345  # Missing quotes for string
  title: Paper Title  # Inconsistent quotes
     authors: Author One  # Extra indentation
```

### Data Types
```yaml
# Strings
title: "Simple string"
abstract: >
  Multi-line string
  folded into one line
notes: |
  Multi-line string
  preserving newlines

# Numbers
max_results: 10
version: 1.0

# Booleans
enabled: true
debug: false

# Null
key_findings: null
# Or
key_findings: ""  # Preferred for empty strings

# Lists
authors:
  - "Author One"
  - "Author Two"

# Or inline
tags: [ai, ml, nlp]

# Dictionaries
paper:
  id: "2401.12345"
  title: "Title"
```

## Git

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat: add arXiv paper fetcher

Implements automated fetching of papers from arXiv API
using cs.AI category filter.

Closes #123

---

fix: handle empty abstract in summarizer

Previously crashed when abstract was missing. Now returns
placeholder text.

---

docs: update README with deployment instructions

---

chore: update arXiv feed: 2024-01-15 14:30 UTC
```

### Branch Naming
```
feature/arxiv-fetcher
fix/summarizer-crash
docs/api-documentation
```

## Jekyll/Liquid

### Front Matter
- Always include required fields
- Use consistent formatting
- Quote string values with special chars

```yaml
---
layout: archive
title: "Latest AI Research"
permalink: /arxiv-feed/
author_profile: true
---
```

### Liquid Templates
- Use whitespace for readability
- Comment complex logic
- Prefer `if` over `unless` when possible

```liquid
{% comment %}
  Display paper cards for all papers in data file
{% endcomment %}

{% if site.data.arxiv_papers.papers.size > 0 %}
  {% for paper in site.data.arxiv_papers.papers %}
    {% include paper-card.html paper=paper %}
  {% endfor %}
{% else %}
  <p>No papers available.</p>
{% endif %}
```

## General Best Practices

### Comments
- Explain **why**, not **what**
- Keep comments up-to-date
- Use comments sparingly (code should be self-documenting)

```python
# Good
# Retry with exponential backoff to handle rate limiting
time.sleep(2 ** retry_count)

# Bad
# Sleep for 2 to the power of retry_count seconds
time.sleep(2 ** retry_count)
```

### DRY (Don't Repeat Yourself)
```python
# Bad
papers_ai = fetch_papers("cs.AI", 10)
papers_ml = fetch_papers("cs.LG", 10)
papers_cv = fetch_papers("cs.CV", 10)

# Good
def fetch_multiple_categories(categories: List[str], max_results: int = 10):
    return [fetch_papers(cat, max_results) for cat in categories]

papers = fetch_multiple_categories(["cs.AI", "cs.LG", "cs.CV"])
```

### KISS (Keep It Simple, Stupid)
```python
# Bad (overly complex)
result = list(map(lambda x: x['id'], filter(lambda x: x['published'] > cutoff, papers)))

# Good (readable)
result = [p['id'] for p in papers if p['published'] > cutoff]
```

### Security
- Never commit secrets or API keys
- Use environment variables for sensitive data
- Validate all user input
- Sanitize output (especially in HTML)

```python
# Bad
API_KEY = "sk-1234567890abcdef"

# Good
import os
API_KEY = os.environ.get("ARXIV_API_KEY")
if not API_KEY:
    raise ValueError("ARXIV_API_KEY environment variable not set")
```

### Performance
- Minimize API calls
- Cache expensive operations
- Use appropriate data structures
- Profile before optimizing

```python
# Use caching for repeated operations
from functools import lru_cache

@lru_cache(maxsize=128)
def get_paper_metadata(paper_id: str) -> Dict:
    return fetch_from_api(paper_id)
```

## Code Review Checklist

- [ ] Code follows style guide
- [ ] Functions have docstrings
- [ ] Variables have meaningful names
- [ ] No hardcoded values (use constants)
- [ ] Error handling is appropriate
- [ ] Code is DRY (no duplication)
- [ ] Comments explain why, not what
- [ ] Security best practices followed
- [ ] Tests included (if applicable)
- [ ] Documentation updated
