# Summarize Abstract Prompt

Instructions for the Paper Summarizer Agent to generate key findings from paper abstracts.

## Objective
Read papers from `_data/arxiv_papers.yml` and generate concise, insightful key findings (2-3 sentences) for each paper.

## Step-by-Step Instructions

### Step 1: Load Papers
```python
import yaml

with open('_data/arxiv_papers.yml', 'r') as f:
    data = yaml.safe_load(f)
    papers = data['papers']
```

### Step 2: Identify Papers Needing Summaries
Only process papers where `key_findings: ""` (empty string).

```python
papers_to_summarize = [p for p in papers if not p.get('key_findings')]
```

### Step 3: Generate Key Findings
For each abstract, extract:

1. **Main Contribution**: What's the novel idea or approach?
2. **Methodology**: What technique or method is used? (if significant)
3. **Key Results**: What are the main findings or implications?

### Step 4: Write Summary
Compose a 2-3 sentence summary that:
- Starts with the main contribution
- Mentions methodology if it's important
- Ends with results or impact

## Summary Guidelines

### Structure
```
[Main contribution]. [Methodology/approach]. [Key results/implications].
```

### Good Examples

**Example 1:**
```
Introduces a novel sparse attention mechanism that reduces transformer computational complexity from O(n²) to O(n log n). The method uses locality-sensitive hashing to identify relevant token pairs. Achieves 40% faster training on BERT-scale models while maintaining 99% of baseline accuracy.
```

**Example 2:**
```
Proposes a multi-task learning framework for simultaneous object detection and semantic segmentation. Uses shared encoder with task-specific decoder heads and a novel cross-task attention module. Outperforms single-task baselines by 5% mIoU on COCO dataset with 30% fewer parameters.
```

**Example 3:**
```
Presents a reinforcement learning approach to automated theorem proving in first-order logic. Combines Monte Carlo tree search with a learned value function trained on 100K formal proofs. Successfully proves 78% of test theorems, including 12 previously unsolved problems.
```

### Bad Examples

❌ **Too vague:**
```
This paper discusses transformers. They made improvements. Good results.
```

❌ **Too technical:**
```
Implements a MHDPA mechanism with QKV projection matrices utilizing Gaussian-initialized orthogonal weight matrices following He et al. normalization schemes.
```

❌ **Too long:**
```
This paper introduces a new method for natural language processing that uses transformers, which are a type of neural network architecture. The authors trained their model on a large dataset and found that it performed well on several benchmarks. They also conducted ablation studies to understand which components were most important.
```

## Writing Style

### Tone
- Professional and objective
- Clear and accessible (for AI researchers)
- Factual, based on abstract content

### Voice
- Active voice preferred: "Introduces..." not "A novel method is introduced..."
- Present tense: "Achieves..." not "Achieved..."

### Vocabulary
- Use technical terms when appropriate (attention mechanism, gradient descent)
- Avoid excessive jargon
- Spell out acronyms first time: "Natural Language Processing (NLP)"

## Quality Checklist

For each summary, verify:
- [ ] 2-3 sentences (40-60 words)
- [ ] Starts with main contribution
- [ ] Mentions methodology (if important)
- [ ] States results/impact
- [ ] Clear and understandable
- [ ] Based on abstract content only
- [ ] No speculation or added information

## Example Python Script

```python
#!/usr/bin/env python3
import yaml

def generate_key_findings(abstract):
    """
    Generate key findings from abstract.
    In production, this would use an LLM API.
    """
    # Example: Extract first 2-3 sentences as key findings
    # (In real implementation, use Claude/GPT API)
    sentences = abstract.split('. ')[:3]
    return '. '.join(sentences) + '.'

# Load papers
with open('_data/arxiv_papers.yml', 'r') as f:
    data = yaml.safe_load(f)

# Process papers
updated = 0
for paper in data['papers']:
    if not paper.get('key_findings'):
        paper['key_findings'] = generate_key_findings(paper['abstract'])
        updated += 1

# Save updated data
with open('_data/arxiv_papers.yml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

print(f"✓ Updated key findings for {updated} papers")
```

## Error Handling

### If Abstract is Missing
```python
if not paper.get('abstract'):
    paper['key_findings'] = "Abstract not available."
```

### If Abstract is Too Short (< 50 chars)
```python
if len(paper['abstract']) < 50:
    paper['key_findings'] = "Brief abstract. See paper for details."
```

### If Summarization Fails
```python
try:
    paper['key_findings'] = generate_key_findings(paper['abstract'])
except Exception as e:
    paper['key_findings'] = "Novel approach. Results pending detailed analysis."
    print(f"Warning: Failed to summarize {paper['id']}: {e}")
```

## Success Criteria
- ✅ All papers have non-empty `key_findings`
- ✅ Summaries are 2-3 sentences
- ✅ Summaries follow guidelines
- ✅ YAML file updated successfully
- ✅ No data loss (all other fields preserved)

## Expected Output
```
Loading papers from _data/arxiv_papers.yml...
Found 10 papers, 10 need summaries
Generating key findings...
  ✓ 2401.12345: "Introduces a novel..."
  ✓ 2401.12346: "Proposes a multi-task..."
  ...
✓ Updated 10 papers with key findings
✓ Saved to _data/arxiv_papers.yml
```
