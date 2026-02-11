# API Interaction Skill

Skills for interacting with external APIs, specifically the arXiv API.

## Core Competencies

### 1. HTTP Requests with curl
```bash
# Basic GET request
curl -s "http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=10"

# With headers and error handling
curl -s -f -H "User-Agent: arXiv-Feed-Bot/1.0" \
  "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10" \
  || echo "API request failed"

# Save response to file
curl -s -o response.xml "http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=10"
```

### 2. XML Parsing
Use command-line tools to parse Atom XML:

```bash
# Extract titles using grep/sed
grep '<title>' response.xml | sed 's/<[^>]*>//g'

# Extract with xmllint (if available)
xmllint --xpath "//entry/title/text()" response.xml

# Python one-liner for complex parsing
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('response.xml')
for entry in tree.findall('.//{http://www.w3.org/2005/Atom}entry'):
    title = entry.find('{http://www.w3.org/2005/Atom}title').text
    print(title.strip())
"
```

### 3. Rate Limiting
```bash
# Wait between requests
curl "..." && sleep 3 && curl "..."

# Track request timing
start_time=$(date +%s)
curl "..."
end_time=$(date +%s)
elapsed=$((end_time - start_time))
if [ $elapsed -lt 3 ]; then
    sleep $((3 - elapsed))
fi
```

### 4. Error Handling & Retries
```bash
# Retry logic
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s -f "http://api.example.com/data" -o output.xml; then
        echo "Success!"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo "Attempt $RETRY_COUNT failed, retrying in 5s..."
        sleep 5
    fi
done
```

### 5. Response Validation
```bash
# Check if response is valid XML
if xmllint --noout response.xml 2>/dev/null; then
    echo "Valid XML"
else
    echo "Invalid XML response"
    exit 1
fi

# Check for error messages in response
if grep -q "<error>" response.xml; then
    echo "API returned error"
    exit 1
fi
```

## arXiv API Specifics

### URL Structure
```
Base: http://export.arxiv.org/api/query
Parameters:
  - search_query: Query string (e.g., cat:cs.AI)
  - sortBy: Field to sort by (submittedDate, lastUpdatedDate, relevance)
  - sortOrder: ascending or descending
  - start: Starting index (for pagination)
  - max_results: Number of results (max 30000, recommended <= 100)
```

### Response Format (Atom XML)
```xml
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2401.12345v1</id>
    <title>Paper Title</title>
    <summary>Abstract text...</summary>
    <author><name>Author Name</name></author>
    <published>2024-01-15T12:00:00Z</published>
    <link href="http://arxiv.org/abs/2401.12345" rel="alternate"/>
    <link href="http://arxiv.org/pdf/2401.12345" rel="related"/>
  </entry>
</feed>
```

### Extracting Paper ID from URL
```bash
# From: http://arxiv.org/abs/2401.12345v1
# Extract: 2401.12345

arxiv_id=$(echo "$url" | sed -E 's|.*/abs/([0-9.]+)v?[0-9]*|\1|')
```

## Best Practices
1. **Always respect rate limits**: Wait 3 seconds between arXiv API calls
2. **Use meaningful User-Agent**: Identify your application
3. **Handle network failures gracefully**: Implement retries with exponential backoff
4. **Validate responses**: Check for valid XML before parsing
5. **Log API calls**: Track requests for debugging

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| 403 Forbidden | Add proper User-Agent header |
| Empty response | Check query syntax, verify category exists |
| Malformed XML | arXiv API might be down, retry later |
| Timeout | Increase curl timeout: `--max-time 30` |
| Rate limit hit | Implement exponential backoff |
