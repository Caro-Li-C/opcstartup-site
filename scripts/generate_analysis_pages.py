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
    author = fm.get('author', '潇韬')
    description = fm.get('description', fm.get('summary', ''))

    # 正文简单处理：把 markdown 标题转成 HTML
    processed_body = body
    processed_body = re.sub(r'^#{1,2}\s+(.+)$', r'<h2>\1</h2>', processed_body, flags=re.MULTILINE)
    processed_body = re.sub(r'^#{3}\s+(.+)$', r'<h3>\1</h3>', processed_body, flags=re.MULTILINE)
    processed_body = re.sub(r'^\*\*(.+?)\*\*$', r'<p><strong>\1</strong></p>', processed_body, flags=re.MULTILINE)
    # 普通段落用 <p> 包裹（已经是段落的不处理）
    lines = processed_body.split('\n')
    html_lines = []
    in_para = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_para:
                html_lines.append('</p>')
                in_para = False
            continue
        if stripped.startswith('<h') or stripped.startswith('<p><strong>'):
            if in_para:
                html_lines.append('</p>')
                in_para = False
            html_lines.append(stripped)
            continue
        if not in_para:
            html_lines.append('<p>')
            in_para = True
        html_lines.append(line)
    if in_para:
        html_lines.append('</p>')
    processed_body = '\n'.join(html_lines)

    # 生成带内联样式的完整 HTML（参照政策原文排版）
    tags_html = ''.join([f'<span class="meta-tag">{t}</span>' for t in tags])
    
    html = f'''---
layout: default
title: "{title}"
---

<style>
  :root {{
    --bg: #f5f5f5;
    --bg-elevated: #ebebeb;
    --border: #d8d8d8;
    --text-primary: #1a1a1a;
    --text-secondary: #4a4a4a;
    --text-muted: #7a7a7a;
    --accent: #c4a35a;
    --accent-dim: rgba(196, 163, 90, 0.1);
    --accent-border: rgba(196, 163, 90, 0.25);
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    color: var(--text-primary);
    line-height: 1.9;
    font-size: 16px;
  }}
  .article-container {{
    max-width: 780px;
    margin: 0 auto;
    padding: 40px 24px 80px;
  }}
  .policy-header {{
    border-bottom: 1px solid var(--border);
    padding-bottom: 32px;
    margin-bottom: 40px;
  }}
  .policy-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
  }}
  .meta-tag {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 4px;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    color: var(--text-secondary);
  }}
  .meta-tag.category {{
    background: var(--accent-dim);
    border-color: var(--accent-border);
    color: var(--accent);
    font-weight: 500;
  }}
  .policy-title {{
    font-size: 26px;
    font-weight: 700;
    line-height: 1.45;
    color: var(--text-primary);
    margin-bottom: 14px;
    letter-spacing: -0.3px;
  }}
  .policy-source-bar {{
    display: flex;
    align-items: center;
    gap: 20px;
    font-size: 13px;
    color: var(--text-muted);
    flex-wrap: wrap;
  }}
  .source-item {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .source-item svg {{
    width: 14px;
    height: 14px;
    opacity: 0.5;
  }}
  .policy-body {{
    font-size: 16px;
    line-height: 2;
    color: var(--text-primary);
  }}
  .policy-body p {{
    margin-bottom: 16px;
    text-align: justify;
  }}
  .policy-body h2 {{
    font-size: 19px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 44px 0 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    letter-spacing: 0.3px;
  }}
  .policy-body h3 {{
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 28px 0 14px;
    padding-left: 12px;
    border-left: 3px solid var(--accent);
  }}
  .policy-body strong {{
    font-weight: 600;
    color: var(--text-primary);
  }}
  .back-to-list {{
    text-align: center;
    margin: 48px auto 32px;
    max-width: 780px;
    padding: 0 24px;
  }}
  .back-to-list a {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: var(--text-muted);
    text-decoration: none;
    font-size: 14px;
    transition: color 0.2s;
  }}
  .back-to-list a:hover {{ color: var(--accent); }}
  @media (max-width: 640px) {{
    .policy-title {{ font-size: 21px; }}
    .policy-body {{ font-size: 15px; }}
    .policy-body h2 {{ font-size: 17px; }}
  }}
</style>
<base target="_blank">

<article class="article-container">
  <header class="policy-header">
    <div class="policy-meta">
      <span class="meta-tag category">政策解析</span>
      {tags_html}
    </div>
    <h1 class="policy-title">{title}</h1>
    <div class="policy-source-bar">
      <div class="source-item">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        {date_str}
      </div>
      <div class="source-item">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        {author}
      </div>
      <div class="source-item">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
        来源：OPC创业汇
      </div>
    </div>
  </header>
  <div class="policy-body">
    {processed_body}
  </div>
</article>

<div class="back-to-list">
  <a href="./">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
    返回政策解析列表
  </a>
</div>
'''

    with open(OUTPUT_DIR / f'{slug}.html', 'w', encoding='utf-8') as f:
        f.write(html)

    dt = datetime.strptime(str(date_str), '%Y-%m-%d')
    articles.append({
        'title': title,
        'url': f'/policy/analysis/{slug}.html',
        'date': date_str,
        'day': dt.strftime('%d'),
        'month_year': dt.strftime('%m/%Y'),
        'desc': description
    })

    print(f"✓ {filename}")

# 生成列表页 index.html
items = ""
for art in sorted(articles, key=lambda x: x['date'], reverse=True):
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

# 生成 _data/analysis.yml（供首页调用）
data_dir = Path('_data')
data_dir.mkdir(exist_ok=True)

analysis_data = []
for art in sorted(articles, key=lambda x: x['date'], reverse=True):
    analysis_data.append({
        'title': art['title'],
        'url': art['url'],
        'date': art['date'],
        'description': art['desc']
    })

with open(data_dir / 'analysis.yml', 'w', encoding='utf-8') as f:
    yaml.dump(analysis_data, f, allow_unicode=True, sort_keys=False)

print(f"\n✅ 完成！共 {len(articles)} 篇文章 + 列表页 + _data/analysis.yml")
