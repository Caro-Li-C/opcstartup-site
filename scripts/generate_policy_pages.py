#!/usr/bin/env python3
import os
import json
import re
import markdown
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

def process_body_text(body_md):
    """
    处理正文文本：
    1. 清洗零宽字符
    2. 按行分割，每行转为独立段落
    3. 识别标题层级（一、二、三... → h2； （一）（二）... → h3）
    4. 识别落款
    5. 返回精美 HTML
    """
    body_md = clean_text(body_md)
    
    # 按行分割，过滤空行
    lines = [line.strip() for line in body_md.split('\n') if line.strip()]
    
    html_parts = []
    in_signature = False
    signature_lines = []
    
    for line in lines:
        # 识别一级标题：一、二、三... 
        if re.match(r'^[一二三四五六七八九十]+[、\\.\\s]', line):
            html_parts.append(f'<h2>{line}</h2>')
            continue
        
        # 识别二级标题：（一）（二）（三）...
        if re.match(r'^（[一二三四五六七八九十]+）', line):
            html_parts.append(f'<h3>{line}</h3>')
            continue
        
        # 识别落款开始
        if re.match(r'^(.*?人民政府|.*?办公厅|.*?办公室|.*?局|.*?委员会)$', line) and not in_signature:
            in_signature = True
            signature_lines = [line]
            continue
        
        if in_signature:
            if re.match(r'^\\d{4}.*?(年|月|日)', line) or '公开发布' in line or '印发' in line:
                signature_lines.append(line)
                continue
            else:
                # 落款结束，输出
                if signature_lines:
                    sig_html = '<div class="inline-signature">\n'
                    for sig_line in signature_lines:
                        if '公开发布' in sig_line or '印发' in sig_line:
                            sig_html += f'  <p class="pub-note">{sig_line}</p>\n'
                        else:
                            sig_html += f'  <p class="sig-line">{sig_line}</p>\n'
                    sig_html += '</div>\n'
                    html_parts.append(sig_html)
                in_signature = False
        
        # 识别施行说明
        if '本文件自' in line and '起施行' in line:
            html_parts.append(f'<div class="effective-date"><strong>施行说明：</strong>{line}</div>')
            continue
        
        # 普通段落
        if in_signature:
            signature_lines.append(line)
        else:
            html_parts.append(f'<p>{line}</p>')
    
    # 处理未闭合的落款
    if in_signature and signature_lines:
        sig_html = '<div class="inline-signature">\n'
        for sig_line in signature_lines:
            if '公开发布' in sig_line or '印发' in sig_line:
                sig_html += f'  <p class="pub-note">{sig_line}</p>\n'
            else:
                sig_html += f'  <p class="sig-line">{sig_line}</p>\n'
        sig_html += '</div>\n'
        html_parts.append(sig_html)
    
    return '\n'.join(html_parts)

def render_policy_html(meta, body_md, title):
    doc_no = meta.get('doc_no', '')
    date = meta.get('date', '')
    publisher = meta.get('publisher', '')
    source = meta.get('source', '公众号OPC创业汇')
    category = meta.get('category', '政策解读')
    subcategory = meta.get('subcategory', '政策原文')
    
    # 处理正文
    body_html = process_body_text(body_md)
    
    html = f'''
<article class="article-container">
  <header class="policy-header">
    <div class="policy-meta">
      <span class="meta-tag category">{category}</span>
      <span class="meta-tag">{subcategory}</span>
      {f'<span class="meta-tag">{publisher}</span>' if publisher else ''}
    </div>
    <h1 class="policy-title">{title}</h1>
    {f'<div class="policy-doc-no">{doc_no}</div>' if doc_no else ''}
    <div class="policy-source-bar">
      {f'<div class="source-item">📅 {date}</div>' if date else ''}
      {f'<div class="source-item">🏛️ {publisher}</div>' if publisher else ''}
      <div class="source-item">📢 来源：{source}</div>
    </div>
  </header>
  <div class="policy-body">
    {body_html}
  </div>
</article>

<div class="back-to-list">
  <a href="./">← 返回政策列表</a>
</div>
'''
    return html

def page_template(title, body_content, back_link=None, back_text=None):
    back_html = '<a class="back" href="' + back_link + '">← ' + back_text + '</a>\n' if back_link else ''
    return """---
layout: default
title: """ + title + """
---

<style>
  :root {
    --bg: #f5f5f5;
    --bg-elevated: #ebebeb;
    --border: #d8d8d8;
    --text-primary: #1a1a1a;
    --text-secondary: #4a4a4a;
    --text-muted: #7a7a7a;
    --accent: #c4a35a;
    --accent-dim: rgba(196, 163, 90, 0.1);
    --accent-border: rgba(196, 163, 90, 0.25);
  }
  .policy-container {
    max-width: 780px;
    margin: 0 auto;
    padding: 20px 24px 80px;
  }
  .back {
    color: #888;
    font-size: 14px;
    text-decoration: none;
    margin-bottom: 20px;
    display: inline-block;
    letter-spacing: 1px;
  }
  .back:hover { color: #222; }
  .policy-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 32px;
    margin-bottom: 40px;
  }
  .policy-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
  }
  .meta-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 4px;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    color: var(--text-secondary);
  }
  .meta-tag.category {
    background: var(--accent-dim);
    border-color: var(--accent-border);
    color: var(--accent);
    font-weight: 500;
  }
  .policy-title {
    font-size: 26px;
    font-weight: 700;
    line-height: 1.45;
    color: var(--text-primary);
    margin-bottom: 14px;
    letter-spacing: -0.3px;
  }
  .policy-doc-no {
    font-size: 15px;
    color: var(--accent);
    font-family: "SF Mono", "Fira Code", "Courier New", monospace;
    margin-bottom: 20px;
    letter-spacing: 0.5px;
  }
  .policy-source-bar {
    display: flex;
    align-items: center;
    gap: 20px;
    font-size: 13px;
    color: var(--text-muted);
    flex-wrap: wrap;
  }
  .source-item {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .policy-body {
    font-size: 16px;
    line-height: 2;
    color: var(--text-primary);
  }
  .policy-body p {
    margin-bottom: 16px;
    text-align: justify;
  }
  .policy-body h2 {
    font-size: 19px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 44px 0 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    letter-spacing: 0.3px;
  }
  .policy-body h3 {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 28px 0 14px;
    padding-left: 12px;
    border-left: 3px solid var(--accent);
  }
  .policy-body h4 {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 24px 0 12px;
  }
  .policy-body ul, .policy-body ol {
    margin: 16px 0;
    padding-left: 32px;
  }
  .policy-body li {
    margin: 12px 0;
    line-height: 1.9;
  }
  .policy-body table {
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
    font-size: 14px;
  }
  .policy-body th, .policy-body td {
    border: 1px solid var(--border);
    padding: 10px 12px;
    text-align: left;
  }
  .policy-body th {
    background: var(--bg-elevated);
    font-weight: 600;
  }
  .policy-body blockquote {
    border-left: 3px solid var(--accent);
    margin: 20px 0;
    padding: 12px 24px;
    background: var(--bg-elevated);
    color: var(--text-secondary);
    line-height: 1.8;
  }
  .policy-body strong {
    font-weight: 600;
    color: var(--text-primary);
  }
  .inline-signature {
    margin: 24px 0 36px;
  }
  .inline-signature .sig-line {
    text-align: right;
    font-size: 16px;
    color: var(--text-primary);
    line-height: 2.4;
    margin: 0;
  }
  .inline-signature .pub-note {
    text-align: left;
    font-size: 16px;
    color: var(--text-primary);
    line-height: 2.4;
    margin: 0;
  }
  .effective-date {
    margin-top: 24px;
    padding: 16px 20px;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.8;
  }
  .effective-date strong {
    color: var(--accent);
    font-weight: 600;
  }
  .back-to-list {
    text-align: center;
    margin-bottom: 32px;
  }
  .back-to-list a {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: var(--text-muted);
    text-decoration: none;
    font-size: 14px;
    transition: color 0.2s;
  }
  .back-to-list a:hover { color: var(--accent); }
  .watermark {
    position: fixed;
    top: 50%; 
    left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 120px;
    color: rgba(0,0,0,0.012);
    pointer-events: none;
    z-index: 9999;
    user-select: none;
    font-family: sans-serif;
    letter-spacing: 10px;
  }
  @media (max-width: 640px) {
    .policy-title { font-size: 21px; }
    .policy-body { font-size: 15px; }
    .policy-body h2 { font-size: 17px; }
  }
</style>

<div class="policy-container">
  """ + back_html + body_content + """  <div class="watermark">OPC创业汇</div>
</div>
"""

def make_slug(fname):
    m = re.match(r'^(\d+)', fname)
    return m.group(1) if m else '0'

CN_NUMS = ['一','二','三','四','五','六','七','八','九','十','十一','十二']

for region in structure['regions']:
    region_dir = output_base / region['id']
    region_dir.mkdir(parents=True, exist_ok=True)
    
    chapters_html = ""
    for idx, ch in enumerate(region['chapters']):
        ch_link = ch['id'] + "/"
        ch_label = "第" + CN_NUMS[idx] + "章"
        chapters_html += '<li style="border-left:2px solid #1a1a1a;padding-left:20px;margin-bottom:24px;"><div style="font-size:12px;color:#888;letter-spacing:2px;margin-bottom:6px;">' + ch_label + '</div><a href="' + ch_link + '" style="color:#1a1a1a;text-decoration:none;font-size:16px;">' + ch['name'] + '</a></li>\n'
    
    region_idx = structure['regions'].index(region)
    region_label = "第" + CN_NUMS[region_idx] + "篇"
    
    region_body = '<div style="font-size:12px;color:#888;letter-spacing:2px;margin-bottom:10px;">' + region_label + '</div>\n<h1 style="font-size:28px;font-weight:400;padding-bottom:16px;margin-bottom:40px;letter-spacing:2px;">' + region['name'] + '</h1>\n<ul style="list-style:none;padding:0;margin:0;">\n' + chapters_html + '</ul>\n'
    
    region_html = page_template(region['name'], region_body, back_link="../", back_text="返回政策汇编")
    (region_dir / 'index.html').write_text(region_html, encoding='utf-8')
    
    for ch_idx, ch in enumerate(region['chapters']):
        ch_dir = region_dir / ch['id']
        ch_dir.mkdir(parents=True, exist_ok=True)
        
        policies_html = ""
        
        for fname in ch.get('files', []):
            md_name = fname if fname.endswith('.md') else fname + '.md'
            md_path = Path('_tmp_source/policy') / md_name
            
            if not md_path.exists():
                print("⚠️  文件不存在，跳过: " + str(md_path))
                continue
            
            raw_text = md_path.read_text(encoding='utf-8')
            meta, body_md = parse_front_matter(raw_text)
            
            title = meta.get('title', '')
            if not title:
                first_line = body_md.strip().split('\n')[0]
                title = clean_text(first_line).strip()
                title = re.sub(r'^\d+[_\-\s]+', '', title)
            
            slug = make_slug(fname)
            
            policy_html = render_policy_html(meta, body_md, title)
            
            detail_html = page_template(title, policy_html, back_link="./", back_text="返回" + ch['name'])
            (ch_dir / (slug + '.html')).write_text(detail_html, encoding='utf-8')
            
            policies_html += '<li style="border-left:2px solid #1a1a1a;padding-left:20px;margin-bottom:24px;"><a href="' + slug + '.html" style="color:#1a1a1a;text-decoration:none;font-size:16px;">' + title + '</a></li>\n'
        
        ch_label = "第" + CN_NUMS[ch_idx] + "章"
        ch_body = '<div style="font-size:12px;color:#888;letter-spacing:2px;margin-bottom:10px;">' + ch_label + '</div>\n<h1 style="font-size:28px;font-weight:400;padding-bottom:16px;margin-bottom:40px;letter-spacing:2px;">' + ch['name'] + '</h1>\n<ul style="list-style:none;padding:0;margin:0;">\n' + (policies_html if policies_html else '<li style="border-left-color:#ccc;"><div style="color:#888;font-size:14px;">暂无政策文件</div></li>') + '</ul>\n'
        
        ch_html = page_template(ch['name'], ch_body, back_link="../", back_text="返回" + region['name'])
        (ch_dir / 'index.html').write_text(ch_html, encoding='utf-8')

print("✅ 政策子页面生成完成！")
print("   生成路径: " + str(output_base))
