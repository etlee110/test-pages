#!/usr/bin/env python3
"""Fetch latest papers from arXiv cs.AI category."""

import sys
import time
import xml.etree.ElementTree as ET
import requests
import yaml
from pathlib import Path

API_URL = "http://export.arxiv.org/api/query"
OUTPUT_FILE = "_data/arxiv_papers.yml"

def fetch_papers(category="cs.AI", max_results=10):
    """Fetch papers from arXiv API."""
    params = {
        "search_query": f"cat:{category}",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results
    }
    
    print(f"Fetching {max_results} papers from {category}...")
    
    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        time.sleep(3)  # Respect rate limit
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching papers: {e}", file=sys.stderr)
        return None

def parse_papers(xml_content):
    """Parse arXiv XML response."""
    if not xml_content:
        return []
    
    try:
        root = ET.fromstring(xml_content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            # Extract paper ID
            id_url = entry.find('atom:id', ns).text
            paper_id = id_url.split('/')[-1].split('v')[0]
            
            # Extract title
            title = entry.find('atom:title', ns).text
            title = ' '.join(title.split())  # Clean whitespace
            
            # Extract authors
            authors = [
                a.find('atom:name', ns).text 
                for a in entry.findall('atom:author', ns)
            ]
            authors_str = ', '.join(authors)
            
            # Extract abstract
            abstract = entry.find('atom:summary', ns).text
            abstract = ' '.join(abstract.split())  # Clean whitespace
            
            # Extract published date
            published = entry.find('atom:published', ns).text[:10]
            
            # Construct URLs
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
        
        return papers
    except Exception as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        return []

def save_papers(papers, filepath=OUTPUT_FILE):
    """Save papers to YAML file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    data = {'papers': papers}
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, 
                     default_flow_style=False,
                     allow_unicode=True,
                     sort_keys=False)
        print(f"✓ Saved {len(papers)} papers to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving YAML: {e}", file=sys.stderr)
        return False

def main():
    xml_content = fetch_papers()
    papers = parse_papers(xml_content)
    
    if papers:
        save_papers(papers)
        print(f"✓ Successfully fetched and saved {len(papers)} papers")
        return 0
    else:
        print("No papers fetched", file=sys.stderr)
        # Create empty file to avoid breaking pipeline
        save_papers([])
        return 1

if __name__ == "__main__":
    sys.exit(main())
