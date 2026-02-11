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

<style>
.arxiv-feed {
  max-width: 900px;
  margin: 0 auto;
}

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

.papers-container {
  display: grid;
  gap: 2em;
}

.no-papers {
  text-align: center;
  padding: 4em 2em;
  color: #999;
  font-size: 1.1em;
}
</style>
