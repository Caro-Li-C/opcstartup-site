#!/usr/bin/env python3
import os
import json
import re
import markdown
from pathlib import Path

with open('_tmp_source/structure.json', 'r', encoding='utf-8') as f:
    structure = json.load(f)

output_base = Path('policy/original')

# 零宽字符集合（水印字符，需清洗）
ZERO_WIDTH_CHARS = '\u200b\u200c\u200d\ufeff\u2060\u2061\u2062\u2063\u2064\u206a\u206b\u206c\u206d\u206e\u206f'

def clean_text(text):
    return ''.join(c for c in text if c not in ZERO_WIDTH_CHARS)

def page_template(title, body_content, back_link=None, back_text=None):
    back_html = '<a class="back" href="' + back_link + '">← ' + back_text + '</a>\n' if back_link else ''
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>''' + title + ''' | 全国OPC政策汇编</title>
<link rel="stylesheet" href="/assets/css/main.css">
<style>
  .policy-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 20px 80px;
  }
  .back {
    color: #888;
    font-size: 14px;
    text-decoration: none;
    margin-bottom: 30px;
    display: inline-block;
    letter-spacing: 1px;
  }
  .back:hover { color: #222; }
  .section-label {
    font-size: 12px;
    color: #888;
    letter-spacing: 2px;
    margin-bottom: 10px;
    text-transform: uppercase;
  }
  h1.page-title {
    font-size: 28px;
    font-weight: 400;
    border-bottom: 1px solid #222;
    padding-bottom: 20px;
    margin-bottom: 40px;
    letter-spacing: 2px;
  }
  .chapter-list, .policy-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .chapter-list li, .policy-list li {
    border-left: 2px solid #222;
    padding-left: 20px;
    margin-bottom: 24px;
    transition: border-color 0.2s;
  }
  .chapter-list li:hover { border-left-color: #666; }
  .chapter-list a, .policy-list a {
    color: #222;
    text-decoration: none;
    font-size: 16px;
    letter-spacing: 0.5px;
    line-height: 1.6;
  }
  .chapter-list a:hover, .policy-list a:hover {
    text-decoration: underline;
  }
  .policy-content {
    font-size: 15px;
    line-height: 1.9;
    color: #333;
  }
  .policy-content h1, .policy-content h2, .policy-content h3, .policy-content h4 {
    font-weight: 600;
    color: #222;
    margin-top: 32px;
    margin-bottom: 16px;
    line-height: 1.4;
  }
  .policy-content h1 { font-size: 22px; border-bottom: 1px solid #ddd; padding-bottom: 12px; }
  .policy-content h2 { font-size: 20px; }
  .policy-content h3 { font-size: 18px; }
  .policy-content h4 { font-size: 16px; }
  .policy-content p {
    margin: 16px 0;
    text-align: justify;
  }
  .policy-content ul, .policy-content ol {
    margin: 16px 0;
    padding-left: 28px;
  }
  .policy-content li {
    margin: 8px 0;
  }
  .policy-content table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 14px;
  }
  .policy-content th, .policy-content td {
    border: 1px solid #ddd;
    padding: 10px 12px;
    text-align: left;
  }
  .policy-content th {
    background: #f5f5f0;
    font-weight: 600;
  }
  .policy-content blockquote {
    border-left: 3px solid #222;
    margin: 20px 0;
    padding: 10px 20px;
    background: #fafafa;
    color: #555;
  }
  .policy-content strong {
    font-weight: 600;
    color: #222;
  }
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
</style>
</head>
<body>
<nav class="site-nav">
  <div class="nav-container">
    <a href="/" class="nav-logo">OPC创业汇</a>
    <div class="nav-links">
      <a href="/">首页</a>
      <a href="/policy/">政策</a>
      <a href="/practice/">实务</a>
      <a href="/posts/">文章</a>
      <a href="/insights/">观点</a>
    </div>
  </div>
</nav>
<main class="site-main">
  <div class="policy-container">
    ''' + back_html + body_content + '''
  </div>
  <div class="watermark">OPC创业汇</div>
</main>
<footer class="site-footer">
  <p>OPC创业汇 · 超级个体的战略合伙人</p>
</footer>
</body>
</html>'''

def md_to_html(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = parts[2]
    text = clean_text(text)
    return markdown.markdown(text, extensions=['tables', 'fenced_code', 'toc'])

def extract_title(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        first_line = clean_text(first_line)
        if first_line.startswith('#'):
            return first_line.lstrip('#').strip()
    name = md_path.stem
    name = re.sub(r'^\d+[_-]', '', name)
    return name

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
        chapters_html += '''
        <li>
          <div class="section-label">''' + ch_label + '''</div>
          <a href="''' + ch_link + '''">''' + ch['name'] + '''</a>
        </li>
'''

    region_idx = structure['regions'].index(region)
    region_label = "第" + CN_NUMS[region_idx] + "篇"

    region_body = '''
<div class="section-label">''' + region_label + '''</div>
<h1 class="page-title">''' + region['name'] + '''</h1>
<ul class="chapter-list">
''' + chapters_html + '''
</ul>
'''

    region_html = page_template(
        region['name'],
        region_body,
        back_link="../",
        back_text="返回政策汇编"
    )

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

            title = extract_title(md_path)
            slug = make_slug(fname)

            detail_body = '''
<h1 class="page-title">''' + title + '''</h1>
<div class="policy-content">
''' + md_to_html(md_path) + '''
</div>
'''

            detail_html = page_template(
                title,
                detail_body,
                back_link="./",
                back_text="返回" + ch['name']
            )

            (ch_dir / (slug + '.html')).write_text(detail_html, encoding='utf-8')

            policies_html += '''
            <li>
              <a href="''' + slug + '''.html">''' + title + '''</a>
            </li>
'''

        ch_label = "第" + CN_NUMS[ch_idx] + "章"
        ch_body = '''
<div class="section-label">''' + ch_label + '''</div>
<h1 class="page-title">''' + ch['name'] + '''</h1>
<ul class="policy-list">
''' + (policies_html if policies_html else '<li style="border-left-color:#ccc;"><div style="color:#888;font-size:14px;">暂无政策文件</div></li>') + '''
</ul>
'''

        ch_html = page_template(
            ch['name'],
            ch_body,
            back_link="../",
            back_text="返回" + region['name']
        )

        (ch_dir / 'index.html').write_text(ch_html, encoding='utf-8')

print("✅ 政策子页面生成完成！")
print("   生成路径: " + str(output_base))
