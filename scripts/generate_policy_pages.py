#!/usr/bin/env python3
import os
import json
import re
import yaml
from pathlib import Path

with open('_tmp_source/structure.json', 'r', encoding='utf-8') as f:
    structure = json.load(f)

output_base = Path('policy/original')

ZERO_WIDTH_CHARS = '\u200b\u200c\u200d\ufeff\u2060\u2061\u2062\u2063\u2064\u206a\u206b\u206c\u206d\u206e\u206f'

def clean_text(text):
    return ''.join(c for c in text if c not in ZERO_WIDTH_CHARS)

def parse_front_matter(text):
    if not text.startswith('---'):
        return {}, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}, text
    try:
        meta = yaml.safe_load(parts[1])
    except:
        meta = {}
    body = parts[2].strip()
    return meta if meta else {}, body

def extract_city(title):
    m = re.match(r'^(.*?市)', title)
    return m.group(1).replace('市', '') if m else ''

def extract_responsible_unit(line):
    m = re.search(r'（责任单位：[^）]+?）(?:\s*（.*?）)?$', line)
    if m:
        main = line[:m.start()].strip()
        resp = m.group(0)
        return main, f'<span class="responsible-unit">{resp}</span>'
    return line, ''

def _sig_html(lines):
    html = '<div class="inline-signature">\n'
    for s in lines:
        if '公开发布' in s or '印发' in s:
            html += f'  <p class="pub-note">{s}</p>\n'
        else:
            html += f'  <p class="sig-line">{s}</p>\n'
    html += '</div>\n'
    return html

def process_body(body_md):
    body_md = clean_text(body_md)
    lines = [line.strip() for line in body_md.split('\n') if line.strip()]
    parts = []
    in_sig = False
    sig_lines = []
    idx = 0
    
    for line in lines:
        if re.match(r'^[一二三四五六七八九十]+[、．\s]', line) and len(line) < 60:
            if in_sig and sig_lines:
                parts.append(_sig_html(sig_lines))
                in_sig = False
                sig_lines = []
            parts.append(f'<h2>{line}</h2>')
            idx += 1
            continue
        
        if re.match(r'^（[一二三四五六七八九十]+）', line) and len(line) < 60:
            if in_sig and sig_lines:
                parts.append(_sig_html(sig_lines))
                in_sig = False
                sig_lines = []
            parts.append(f'<h3>{line}</h3>')
            idx += 1
            continue
        
        if re.match(r'^(.*?人民政府|.*?办公厅|.*?办公室|.*?局|.*?委员会|.*?市场监督管理局)$', line) and not in_sig:
            in_sig = True
            sig_lines = [line]
            idx += 1
            continue
        
        if in_sig:
            if re.match(r'^\d{4}.*?(年|月|日)', line) or '公开发布' in line or '印发' in line:
                sig_lines.append(line)
                idx += 1
                continue
            else:
                parts.append(_sig_html(sig_lines))
                in_sig = False
                sig_lines = []
        
        if '本文件自' in line and '起施行' in line:
            parts.append(f'<div class="effective-date"><strong>施行说明:</strong>{line}</div>')
            idx += 1
            continue
        
        main, resp = extract_responsible_unit(line)
        p_class = 'meta-paragraph' if idx == 0 and ('各区' in line or '各县' in line or '各有关' in line) else ''
        
        if p_class:
            parts.append(f'<p class="{p_class}">{main}{resp}</p>')
        else:
            parts.append(f'<p>{main}{resp}</p>')
        idx += 1
    
    if in_sig and sig_lines:
        parts.append(_sig_html(sig_lines))
    
    return '\n'.join(parts)

def render_html(meta, body_md, title):
    doc_no = meta.get('doc_no', '')
    date = meta.get('date', '')
    publisher = meta.get('publisher', '')
    source = meta.get('source', '公众号OPC创业汇')
    category = meta.get('category', '政策解读')
    subcategory = meta.get('subcategory', '政策原文')
    city = extract_city(title)
    
    if not publisher or len(publisher) < 4 or '本文件' in publisher or '施行' in publisher:
        m = re.match(r'^(.*?)(?:关于|印发)', title)
        publisher = m.group(1).strip() if m else publisher
    
    body = process_body(body_md)
    
    cal = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
    bld = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>'
    src = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>'
    
    return f'''<article class="article-container">
  <header class="policy-header">
    <div class="policy-meta">
      <span class="meta-tag category">{category}</span>
      <span class="meta-tag">{subcategory}</span>
      {f'<span class="meta-tag">{city}</span>' if city else ''}
    </div>
    <h1 class="policy-title">{title}</h1>
    {f'<div class="policy-doc-no">{doc_no}</div>' if doc_no else ''}
    <div class="policy-source-bar">
      {f'<div class="source-item">{cal} {date}</div>' if date else ''}
      {f'<div class="source-item">{bld} {publisher}</div>' if publisher else ''}
      <div class="source-item">{src} 来源: {source}</div>
    </div>
  </header>
  <div class="policy-body">
    {body}
  </div>
</article>

<div class="back-to-list">
  <a href="./">返回政策列表</a>
</div>
'''

def page_tpl(title, content, back_link=None, back_text=None):
    back = f'<a class="back" href="{back_link}">返回 {back_text}</a>\n' if back_link else ''
    return f'''---
layout: default
title: {title}
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
  .policy-container {{
    max-width: 780px;
    margin: 0 auto;
    padding: 20px 24px 80px;
  }}
  .back {{
    color: #888;
    font-size: 14px;
    text-decoration: none;
    margin-bottom: 20px;
    display: inline-block;
    letter-spacing: 1px;
  }}
  .back:hover {{ color: #222; }}
  .article-container {{
    max-width: 780px;
    margin: 0 auto;
    padding: 40px 24px 0;
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
  .policy-doc-no {{
    font-size: 15px;
    color: var(--accent);
    font-family: "SF Mono", "Fira Code", "Courier New", monospace;
    margin-bottom: 20px;
    letter-spacing: 0.5px;
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
  .responsible-unit {{
    display: inline;
    color: var(--text-muted);
    font-size: 14px;
  }}
  .meta-paragraph {{
    color: var(--text-secondary);
    font-size: 15px;
  }}
  .inline-signature {{
    margin: 24px 0 36px;
  }}
  .inline-signature .sig-line {{
    text-align: right;
    font-size: 16px;
    color: var(--text-primary);
    line-height: 2.4;
    margin: 0;
  }}
  .inline-signature .pub-note {{
    text-align: left;
    font-size: 16px;
    color: var(--text-primary);
    line-height: 2.4;
    margin: 0;
  }}
  .effective-date {{
    margin-top: 24px;
    padding: 16px 20px;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.8;
  }}
  .effective-date strong {{
    color: var(--accent);
    font-weight: 600;
  }}
  .back-to-list {{
    text-align: center;
    margin-bottom: 32px;
    margin-top: 48px;
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

<div class="policy-container">
  {back}{content}</div>
'''

def make_slug(fname):
    m = re.match(r'^(\d+)', fname)
    return m.group(1) if m else '0'

CN = ['一','二','三','四','五','六','七','八','九','十','十一','十二']

for region in structure['regions']:
    region_dir = output_base / region['id']
    region_dir.mkdir(parents=True, exist_ok=True)
    
    ch_html = ""
    for i, ch in enumerate(region['chapters']):
        ch_html += f'<li style="border-left:2px solid #1a1a1a;padding-left:20px;margin-bottom:24px;"><div style="font-size:12px;color:#888;letter-spacing:2px;margin-bottom:6px;">第{CN[i]}章</div><a href="{ch["id"]}/" style="color:#1a1a1a;text-decoration:none;font-size:16px;">{ch["name"]}</a></li>\n'
    
    r_idx = structure['regions'].index(region)
    r_body = f'<div style="font-size:12px;color:#888;letter-spacing:2px;margin-bottom:10px;">第{CN[r_idx]}篇</div>\n<h1 style="font-size:28px;font-weight:400;padding-bottom:16px;margin-bottom:40px;letter-spacing:2px;">{region["name"]}</h1>\n<ul style="list-style:none;padding:0;margin:0;">\n{ch_html}</ul>\n'
    
    (region_dir / 'index.html').write_text(page_tpl(region['name'], r_body, '../', '返回政策汇编'), encoding='utf-8')
    
    for i, ch in enumerate(region['chapters']):
        ch_dir = region_dir / ch['id']
        ch_dir.mkdir(parents=True, exist_ok=True)
        
        p_html = ""
        for fname in ch.get('files', []):
            md = fname if fname.endswith('.md') else fname + '.md'
            mp = Path('_tmp_source/policy') / md
            if not mp.exists():
                print(f"跳过: {mp}")
                continue
            
            raw = mp.read_text(encoding='utf-8')
            meta, body = parse_front_matter(raw)
            
            title = meta.get('title', '')
            if not title:
                title = clean_text(body.strip().split('\n')[0])
                title = re.sub(r'^\d+[_\-\s]+', '', title)
            
            slug = make_slug(fname)
            policy = render_html(meta, body, title)
            (ch_dir / f'{slug}.html').write_text(page_tpl(title, policy, './', f'返回{ch["name"]}'), encoding='utf-8')
            
            p_html += f'<li style="border-left:2px solid #1a1a1a;padding-left:20px;margin-bottom:24px;"><a href="{slug}.html" style="color:#1a1a1a;text-decoration:none;font-size:16px;">{title}</a></li>\n'
        
        c_body = f'<div style="font-size:12px;color:#888;letter-spacing:2px;margin-bottom:10px;">第{CN[i]}章</div>\n<h1 style="font-size:28px;font-weight:400;padding-bottom:16px;margin-bottom:40px;letter-spacing:2px;">{ch["name"]}</h1>\n<ul style="list-style:none;padding:0;margin:0;">\n{p_html if p_html else "<li style=\'border-left-color:#ccc;\'><div style=\'color:#888;font-size:14px;\'>暂无政策文件</div></li>"}</ul>\n'
        (ch_dir / 'index.html').write_text(page_tpl(ch['name'], c_body, '../', f'返回{region["name"]}'), encoding='utf-8')

print("完成")
