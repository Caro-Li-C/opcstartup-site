#!/usr/bin/env python3
import os
import json
import re
import markdown
from pathlib import Path

with open('_tmp_source/structure.json', 'r', encoding='utf-8') as f:
    structure = json.load(f)

output_base = Path('policy/original')

STYLE = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: "Noto Serif SC", "Songti SC", "SimSun", serif;
    background: #f5f5f0;
    color: #222;
    line-height: 1.8;
    max-width: 800px;
    margin: 0 auto;
    padding: 60px 40px;
  }
  h1 { font-size: 32px; font-weight: 400; border-bottom: 1px solid #222; padding-bottom: 20px; margin-bottom: 40px; letter-spacing: 2px; }
  h2 { font-size: 22px; font-weight: 400; margin-top: 40px; margin-bottom: 20px; letter-spacing: 1px; }
  .back { color: #888; font-size: 14px; text-decoration: none; margin-bottom: 40px; display: block; letter-spacing: 1px; }
  .back:hover { color: #222; }
  .chapter-list, .policy-list { list-style: none; padding: 0; }
  .chapter-list li, .policy-list li { border-left: 2px solid #222; padding-left: 20px; margin-bottom: 30px; transition: border-color 0.2s; }
  .chapter-list li:hover { border-left-color: #666; }
  .chapter-list a, .policy-list a { color: #222; text-decoration: none; font-size: 16px; letter-spacing: 0.5px; }
  .chapter-list a:hover, .policy-list a:hover { text-decoration: underline; }
  .content { margin-top: 40px; font-size: 15px; }
  .content h3 { font-size: 18px; font-weight: 600; margin-top: 30px; margin-bottom: 15px; }
  .content h4 { font-size: 16px; font-weight: 600; margin-top: 25px; margin-bottom: 10px; }
  .content p { margin: 15px 0; }
  .content ul, .content ol { margin: 15px 0; padding-left: 25px; }
  .content li { margin: 8px 0; }
  .content table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }
  .content th, .content td { border: 1px solid #ddd; padding: 10px; text-align: left; }
  .content th { background: #f0f0f0; font-weight: 600; }
  .watermark {
    position: fixed; top: 50%; left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 120px; color: rgba(0,0,0,0.012);
    pointer-events: none; z-index: 9999; user-select: none;
    font-family: sans-serif; letter-spacing: 10px;
  }
  .section-label { font-size: 12px; color: #888; letter-spacing: 2px; margin-bottom: 10px; text-transform: uppercase; }
</style>
"""

def md_to_html(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = parts[2]
    return markdown.markdown(text, extensions=['tables', 'fenced_code', 'toc'])

def extract_title(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        if first_line.startswith('#'):
            return first_line.lstrip('#').strip()
    name = md_path.stem
    name = re.sub(r'^\d+[_-]', '', name)
    return name

def make_slug(fname):
    m = re.match(r'^(\d+)', fname)
    return m.group(1) if m else '0'

for region in structure['regions']:
    region_dir = output_base / region['id']
    region_dir.mkdir(parents=True, exist_ok=True)
    
    chapters_html = ""
    for ch in region['chapters']:
        ch_link = f"{ch['id']}/"
        ch_label = f"第{['一','二','三','四','五','六','七','八','九','十','十一','十二'][region['chapters'].index(ch)]}章"
        chapters_html += f'''
        <li>
          <div class="section-label">{ch_label}</div>
          <a href="{ch_link}">{ch['name']}</a>
        </li>\n'''
    
    region_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{region['name']} | 全国OPC政策汇编</title>
{STYLE}
</head>
<body>
<a class="back" href="../">← 返回政策汇编</a>
<div class="section-label">第{['一','二','三','四','五','六','七'][structure['regions'].index(region)]}篇</div>
<h1>{region['name']}</h1>
<ul class="chapter-list">
{chapters_html}
</ul>
<div class="watermark">OPC创业汇</div>
</body>
</html>'''
    
    (region_dir / 'index.html').write_text(region_html, encoding='utf-8')
    
    for ch in region['chapters']:
        ch_dir = region_dir / ch['id']
        ch_dir.mkdir(parents=True, exist_ok=True)
        
        policies_html = ""
        
        for fname in ch.get('files', []):
            md_name = fname if fname.endswith('.md') else fname + '.md'
            md_path = Path('_tmp_source/policy') / md_name
            
            if not md_path.exists():
                print(f"⚠️  文件不存在，跳过: {md_path}")
                continue
            
            title = extract_title(md_path)
            slug = make_slug(fname)
            
            detail_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | 全国OPC政策汇编</title>
{STYLE}
</head>
<body>
<a class="back" href="./">← 返回{ch['name']}</a>
<h1>{title}</h1>
<div class="content">
{md_to_html(md_path)}
</div>
<div class="watermark">OPC创业汇</div>
</body>
</html>'''
            
            (ch_dir / f'{slug}.html').write_text(detail_html, encoding='utf-8')
            
            # 去掉小字（meta 文件名），只保留标题链接
            policies_html += f'''
            <li>
              <a href="{slug}.html">{title}</a>
            </li>\n'''
        
        ch_label = f"第{['一','二','三','四','五','六','七','八','九','十','十一','十二'][region['chapters'].index(ch)]}章"
        ch_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{ch['name']} | 全国OPC政策汇编</title>
{STYLE}
</head>
<body>
<a class="back" href="../">← 返回{region['name']}</a>
<div class="section-label">{ch_label}</div>
<h1>{ch['name']}</h1>
<ul class="policy-list">
{policies_html if policies_html else '<li style="border-left-color:#ccc;"><div style="color:#888;font-size:14px;">暂无政策文件</div></li>'}
</ul>
<div class="watermark">OPC创业汇</div>
</body>
</html>'''
        
        (ch_dir / 'index.html').write_text(ch_html, encoding='utf-8')

print("✅ 政策子页面生成完成！")
