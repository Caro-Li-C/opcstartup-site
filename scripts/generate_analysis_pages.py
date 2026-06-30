#!/usr/bin/env python3
import os
import re
import yaml
from pathlib import Path
from datetime import datetime

SOURCE_DIR = Path('_tmp_source/analysis')
OUTPUT_DIR = Path('policy/analysis')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def slugify(title):
    return re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-').replace('_', '-')[:50]

articles = []

for filename in sorted(os.listdir(SOURCE_DIR)):
    if not filename.endswith('.md'):
        continue

    filepath = SOURCE_DIR / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 解析 front matter
    fm = {}
    body = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
            except:
                pass
            body = parts[2].strip()

    # 从文件名提取日期
    name = filename.replace('.md', '')
    m = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)', name)
    if m:
        date_str = m.group(1)
        title = fm.get('title', m.group(2).replace('-', ''))
    else:
        date_str = fm.get('date', '2026-06-25')
        title = fm.get('title', name)

    slug = slugify(title)
    tags = fm.get('tags', ['政策解析', 'OPC'])
    tags_str = ', '.join([f'"{t}"' for t in tags])

    # 生成单篇文章 HTML
    html = f'''---
layout: post
title: "{title}"
date: {date_str}
description: "{fm.get('description', fm.get('summary', ''))}"
source: OPC创业汇
tags: [{tags_str}]
---

<div class="article-content">
{body}
</div>
'''

    with open(OUTPUT_DIR / f'{slug}.html', 'w', encoding='utf-8') as f:
        f.write(html)

    dt = datetime.strptime(str(date_str), '%Y-%m-%d')
    articles.append({
        'title': title,
        'url': f'/policy/analysis/{slug}.html',
        'day': dt.strftime('%d'),
        'month_year': dt.strftime('%m/%Y'),
        'desc': fm.get('description', fm.get('summary', title))
    })

    print(f"✓ {filename}")

# 生成列表页 index.html
items = ""
for art in sorted(articles, key=lambda x: x['url'], reverse=True):
    items += f'''
    <article class="post-item">
      <div class="post-left">
        <div class="post-date-day">{art['day']}</div>
        <div class="post-date-month">{art['month_year']}</div>
      </div>
      <div class="post-main">
        <h2 class="post-title"><a href="{art['url']}">{art['title']}</a></h2>
        <p class="post-description">{art['desc']}</p>
        <div class="post-footer">
          <div class="post-tags-inline">
            <span class="post-tag-inline">政策解析</span>
          </div>
        </div>
      </div>
    </article>'''

index_html = f'''---
layout: default
title: "政策解析"
---

<div class="articles-page">
  <div class="page-header">
    <h1 class="page-title">政策解析</h1>
    <p class="page-subtitle">OPC创业汇对重点政策的深度解读</p>
  </div>
  <div class="post-list">
{items}
  </div>
</div>
'''

with open(OUTPUT_DIR / 'index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print(f"\n✅ 完成！共 {len(articles)} 篇文章 + 列表页")
