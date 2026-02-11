#!/usr/bin/env python3
"""Generate key findings from paper abstracts."""

import sys
import yaml

INPUT_FILE = "_data/arxiv_papers.yml"

def extract_key_sentences(abstract, max_sentences=3):
    """Extract first N sentences from abstract as key findings."""
    sentences = abstract.replace('?', '.').replace('!', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    key_findings = '. '.join(sentences[:max_sentences])
    if key_findings and not key_findings.endswith('.'):
        key_findings += '.'
    
    return key_findings

def generate_findings():
    """Generate key findings for papers."""
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"File not found: {INPUT_FILE}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error reading YAML: {e}", file=sys.stderr)
        return 1
    
    if not data or 'papers' not in data:
        print("No papers in data file", file=sys.stderr)
        return 1
    
    updated_count = 0
    for paper in data['papers']:
        if not paper.get('key_findings'):
            abstract = paper.get('abstract', '')
            if abstract:
                paper['key_findings'] = extract_key_sentences(abstract)
                updated_count += 1
            else:
                paper['key_findings'] = 'Abstract not available.'
    
    # Save updated data
    try:
        with open(INPUT_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(data, f,
                     default_flow_style=False,
                     allow_unicode=True,
                     sort_keys=False)
        print(f"✓ Generated key findings for {updated_count} papers")
        return 0
    except Exception as e:
        print(f"Error writing YAML: {e}", file=sys.stderr)
        return 1

def main():
    return generate_findings()

if __name__ == "__main__":
    sys.exit(main())
