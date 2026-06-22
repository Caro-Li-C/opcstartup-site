#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path

with open('_tmp_source/structure.json', 'r', encoding='utf-8') as f:
    structure = json.load(f)

output_base = Path('policy/original')

ZERO_WIDTH_CHARS = '\u200b\u200c\u200d\ufeff\u2060\u2061\u2062\u2063\u2064\u206a\u206b\u206c\u206d\u206e\u206f'

def clean_text(text):
    return ''.join(c for c in text if c not in ZERO_WIDTH_CHARS)

def extract_from_html(html_text):
    """
    从完整的 HTML 文件中提取：
    1. <style>...</style> 内容
    2. <body>...</body> 内容
    返回 (css_content, body_content)
    """
    # 提取 <style> 标签内容
    style_match = re.search(r'<style[^>]*>(.*?)</style>', html_text, re.DOTALL)
    css_content = style_match.group(1).strip() if style_match else ""
    
    # 提取 <body> 内容
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html_text, re.DOTALL)
    body_content = body_match.group(1).strip() if body_match else html_text
    
    # 清洗零宽字符
    css_content = clean_text(css_content)
    body_content = clean_text(body_content)
    
    return css_content, body_content

def page_template(title, body_content, back_link=None, back_text=None):
    back_html = '<a class="back" href="' + back_link + '">← ' + back_text + '</a>\n' if back_link else ''
    return """---
layout: default
title: """ + title + """
---

<style>
  .policy-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px 20px 80px;
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
</style>

""" + back_html + body_content

def read_policy_file(md_path):
    """读取 md/html 文件，去掉 YAML front matter，提取 style 和 body"""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 去掉 Jekyll front matter
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = parts[2]
    
    text = text.strip()
    
    # 如果是完整 HTML（包含 <html> 标签），提取 body 和 style
    if '<html' in text.lower() or '<!DOCTYPE' in text.upper():
        css, body = extract_from_html(text)
        
        # 如果提取到了 CSS，把它内嵌到 body 里（用 <style> 包裹）
        if css:
            body = '<style>\n' + css + '\n</style>\n\n' + body
        
        return body
    
    # 如果不是完整 HTML，直接返回（兜底）
    return clean_text(text)

def extract_title_from_html(html_text):
    """从 HTML 中提取 <title> 或 <h1> 作为标题"""
    # 先去掉 front matter
    if html_text.startswith('---'):
        parts = html_text.split('---', 2)
        if len(parts) >= 3:
            html_text = parts[2]
    
    # 尝试 <title>
    title_match = re.search(r'<title>(.*?)</title>', html_text, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
        # 去掉 " | OPC创业汇" 后缀
        title = re.sub(r'\s*\|\s*OPC创业汇.*$', '', title)
        return clean_text(title)
    
    # 尝试 <h1 class="policy-title">
    h1_match = re.search(r'<h1[^>]*class="policy-title"[^>]*>(.*?)</h1>', html_text, re.IGNORECASE | re.DOTALL)
    if h1_match:
        # 去掉 HTML 标签
        h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1))
        return clean_text(h1_text.strip())
    
    # 尝试第一个 <h1>
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_text, re.IGNORECASE | re.DOTALL)
    if h1_match:
        h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1))
        return clean_text(h1_text.strip())
    
    # 兜底：文件名
    return "政策文件"

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
    
    region_body = '<div style="font-size:12px;color:#888;letter-spacing:2px;margin-bottom:10px;">' + region_label + '</div>\n<h1 style="font-size:28px;font-weight:400;padding-bottom:16px;margin-bottom:40px;letter-spacing:2px;position:relative;">' + region['name'] + '</h1>\n<ul style="list-style:none;padding:0;margin:0;">\n' + chapters_html + '</ul>\n'
    
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
            
            # 读取文件内容（提取 HTML body 和 style）
            body_content = read_policy_file(md_path)
            title = extract_title_from_html(md_path.read_text(encoding='utf-8'))
            slug = make_slug(fname)
            
            # 生成政策详情页：layout: default + 提取的 HTML 内容
            detail_html = page_template(
                title,
                body_content,
                back_link="./",
                back_text="返回" + ch['name']
            )
            
            (ch_dir / (slug + '.html')).write_text(detail_html, encoding='utf-8')
            
            policies_html += '<li style="border-left:2px solid #1a1a1a;padding-left:20px;margin-bottom:24px;"><a href="' + slug + '.html" style="color:#1a1a1a;text-decoration:none;font-size:16px;">' + title + '</a></li>\n'
        
        ch_label = "第" + CN_NUMS[ch_idx] + "章"
        ch_body = '<div style="font-size:12px;color:#888;letter-spacing:2px;margin-bottom:10px;">' + ch_label + '</div>\n<h1 style="font-size:28px;font-weight:400;padding-bottom:16px;margin-bottom:40px;letter-spacing:2px;">' + ch['name'] + '</h1>\n<ul style="list-style:none;padding:0;margin:0;">\n' + (policies_html if policies_html else '<li style="border-left-color:#ccc;"><div style="color:#888;font-size:14px;">暂无政策文件</div></li>') + '</ul>\n'
        
        ch_html = page_template(
            ch['name'],
            ch_body,
            back_link="../",
            back_text="返回" + region['name']
        )
        
        (ch_dir / 'index.html').write_text(ch_html, encoding='utf-8')

print("✅ 政策子页面生成完成！")
print("   生成路径: " + str(output_base))
