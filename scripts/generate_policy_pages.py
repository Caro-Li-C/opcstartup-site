#!/usr/bin/env python3
import os
import json
import re
import yaml
from pathlib import Path

with open('_tmp_source/structure.json', 'r', encoding='utf-8') as f:
    structure = json.load(f)

# 兼容 structure 列表格式
if isinstance(structure, list):
    new_structure = {'regions': []}
    for i, region in enumerate(structure):
        region_id = f"{i+1}-{region['name'][:6]}"
        chapters = []
        for j, prov in enumerate(region.get('provinces', [])):
            ch_id = f"{j+1}-{prov['name'][:6]}"
            files = []
            for f in prov.get('files', []):
                if isinstance(f, dict):
                    slug = f.get('slug', '')
                    if slug:
                        files.append(f"{slug}.md")
                elif isinstance(f, str):
                    if not f.endswith(".md"):
                        f = f + ".md"
                    files.append(f)
            chapters.append({
                'id': ch_id,
                'name': prov['name'],
                'files': files
            })
        new_structure['regions'].append({
            'id': region_id,
            'name': region['name'],
            'chapters': chapters
        })
    structure = new_structure

output_base = Path('policy/original')
data_dir = Path('_data')
data_dir.mkdir(exist_ok=True)

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
        
        if '起施行' in line and ('自' in line or '从' in line):
            parts.append(f'<div class="effective-date"><strong>施行说明：</strong>{line}</div>')
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
    
    city_tag = f'<span class="meta-tag">{city}</span>' if city else ''
    doc_no_div = f'<div class="policy-doc-no">{doc_no}</div>' if doc_no else ''
    date_div = f'<div class="source-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> {date}</div>' if date else ''
    publisher_div = f'<div class="source-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg> {publisher}</div>' if publisher else ''
    
    return f"""---
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
  .publish-note {{
    margin-top: 48px;
    padding-top: 32px;
    border-top: 1px solid var(--border);
    font-size: 14px;
    color: var(--text-muted);
    line-height: 2;
  }}
  .publish-note p {{
    margin: 0;
    text-align: left;
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
  .article-nav {{
    max-width: 780px;
    margin: 0 auto;
    padding: 0 24px 60px;
    display: flex;
    justify-content: space-between;
  }}
  .nav-btn {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 14px;
    transition: all 0.2s;
    background: var(--bg);
  }}
  .nav-btn:hover {{
    border-color: var(--accent);
    color: var(--accent);
  }}
  .back-to-list {{
    text-align: center;
    margin-bottom: 32px;
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
    .nav-links {{ display: none; }}
  }}
</style>
<base target="_blank">

<article class="article-container">
  <header class="policy-header">
    <div class="policy-meta">
      <span class="meta-tag category">{category}</span>
      <span class="meta-tag">{subcategory}</span>
      {city_tag}
    </div>
    <h1 class="policy-title">{title}</h1>
    {doc_no_div}
    <div class="policy-source-bar">
      {date_div}
      {publisher_div}
      <div class="source-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> 来源：{source}</div>
    </div>
  </header>
  <div class="policy-body">
    {body}
  </div>
</article>

<div class="back-to-list">
  <a href="./">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
    返回政策原文列表
  </a>
</div>

<nav class="article-nav">
  <a href="#" class="nav-btn" style="visibility: hidden;">← 上一篇</a>
  <a href="#" class="nav-btn">下一篇 →</a>
</nav>
"""

def make_slug(fname):
    return fname.replace('.md', '')


CN = ['一','二','三','四','五','六','七','八','九','十','十一','十二']

# 跳过的非政策章节
SKIP_REGIONS = ['卷首语', '编制说明', 'OPC创业汇', '附录']

policies_data = []

# 生成总列表页
print("生成总列表页...")

region_count = len(structure['regions'])

total_index_html = (
    "---\n"
    "layout: default\n"
    "title: 全国OPC政策汇编\n"
    "---\n"
    "\n"
    "<style>\n"
    "    * { margin: 0; padding: 0; box-sizing: border-box; }\n"
    "    .original-page { max-width: 720px; margin: 0 auto; padding: 80px 24px 120px; }\n"
    "    .top-bar { background: #1a1a1a; padding: 16px 0; }\n"
    "    .top-bar a { display: block; max-width: 720px; margin: 0 auto; padding: 0 24px; color: #888; text-decoration: none; font-size: 12px; letter-spacing: 1px; transition: color 0.3s; }\n"
    "    .top-bar a:hover { color: #fff; }\n"
    "    .header { margin-bottom: 60px; }\n"
    "    .page-title { font-size: 42px; font-weight: 100; letter-spacing: 10px; margin-bottom: 16px; }\n"
    "    .divider { width: 60px; height: 1px; background: #1a1a1a; margin-bottom: 16px; }\n"
    "    .page-desc { font-size: 14px; color: #999; letter-spacing: 2px; }\n"
    "    .catalog { display: flex; flex-direction: column; gap: 48px; }\n"
    "    .part-block { background: #fff; padding: 36px 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); position: relative; }\n"
    "    .part-block::before { content: \"\"; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: #1a1a1a; }\n"
    "    .part-header { margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #eee; }\n"
    "    .part-number { font-size: 11px; color: #bbb; letter-spacing: 3px; margin-bottom: 4px; }\n"
    "    .part-name { font-size: 20px; font-weight: 500; letter-spacing: 2px; }\n"
    "    .chapter-list { display: flex; flex-direction: column; gap: 16px; }\n"
    "    .chapter-item { display: flex; align-items: baseline; gap: 16px; padding: 8px 0; text-decoration: none; color: #1a1a1a; transition: all 0.3s; }\n"
    "    .chapter-item:hover { padding-left: 8px; }\n"
    "    .chapter-item:hover .chapter-name { color: #1a1a1a; }\n"
    "    .chapter-number { font-size: 12px; color: #ccc; min-width: 48px; letter-spacing: 1px; }\n"
    "    .chapter-name { font-size: 15px; color: #666; transition: color 0.3s; }\n"
    "    .back { margin-top: 60px; font-size: 12px; }\n"
    "    .back a { color: #bbb; text-decoration: none; letter-spacing: 1px; transition: color 0.3s; }\n"
    "    .back a:hover { color: #1a1a1a; }\n"
    "    @media (max-width: 768px) { .page-title { font-size: 30px; letter-spacing: 5px; } .original-page { padding: 50px 20px 80px; } .part-block { padding: 28px 24px; } .chapter-item { gap: 12px; } }\n"
    "</style>\n"
    "\n"
    "<div class=\"top-bar\">\n"
    "    <a href=\"../\">← 返回 政策解读</a>\n"
    "</div>\n"
    "<div class=\"original-page\">\n"
    "    <div class=\"header\">\n"
    "        <h1 class=\"page-title\">全国OPC政策汇编</h1>\n"
    "        <div class=\"divider\"></div>\n"
    "        <p class=\"page-desc\">" + str(region_count) + "篇 · 全部政策</p>\n"
    "    </div>\n"
    "    <div class=\"catalog\">\n"
)

for r_idx, region in enumerate(structure['regions']):
    # 跳过非政策章节
    if any(skip in region['name'] for skip in SKIP_REGIONS):
        continue
    
    ch_links = ""
    for c_idx, ch in enumerate(region['chapters']):
        ch_links += (
            '        <a href="' + region["id"] + '/' + ch["id"] + '" class="chapter-item">\n'
            '            <span class="chapter-number">第' + CN[c_idx] + '章</span>\n'
            '            <span class="chapter-name">' + ch["name"] + '</span>\n'
            '        </a>\n'
        )
    
    total_index_html += (
        "        <div class=\"part-block\">\n"
        "            <div class=\"part-header\">\n"
        "                <div class=\"part-number\">第" + CN[r_idx] + "篇</div>\n"
        "                <div class=\"part-name\">" + region["name"] + "</div>\n"
        "            </div>\n"
        "            <div class=\"chapter-list\">\n"
        + ch_links +
        "            </div>\n"
        "        </div>\n"
    )

total_index_html += (
    "    </div>\n"
    "    <div class=\"back\">\n"
    "        <a href=\"../\">← 返回 政策解读</a>\n"
    "    </div>\n"
    "</div>\n"
)

(output_base / 'index.html').write_text(total_index_html, encoding='utf-8')
print("✓ 生成总列表页")


for region in structure['regions']:
    # 跳过非政策章节
    if any(skip in region['name'] for skip in SKIP_REGIONS):
        continue

    region_dir = output_base / region['id']
    region_dir.mkdir(parents=True, exist_ok=True)
    
    for i, ch in enumerate(region['chapters']):
        ch_dir = region_dir / ch['id']
        ch_dir.mkdir(parents=True, exist_ok=True)
        
        p_html = ""
        for fname in ch.get('files', []):
            md = fname if fname.endswith(".md") else fname + ".md"
            # 递归搜索文件（支持 region 子目录）
            mp = None
            for p in Path('_tmp_source/policy').rglob(md):
                mp = p
                break
            if not mp or not mp.exists():
                print(f"跳过: {md}")
                continue
            
            raw = mp.read_text(encoding='utf-8')
            meta, body = parse_front_matter(raw)
            
            title = meta.get('title', '')
            if not title:
                title = clean_text(body.strip().split('\n')[0])
                title = re.sub(r'^\d+[_\-\s]+', '', title)
            
            slug = make_slug(fname)
            (ch_dir / f'{slug}.html').write_text(render_html(meta, body, title), encoding='utf-8')
            
            # 收集数据供首页调用（关键：读取 md 里的真实 date）
            policies_data.append({
                'id': slug,
                'region': region['name'],
                'province': meta.get('province', ''),
                'city': meta.get('city', extract_city(title)),
                'title': title,
                'date': str(meta.get('date', '2026-01-01')),
                'category': meta.get('category', '政策原文'),
                'url': f'/policy/original/{region["id"]}/{ch["id"]}/{slug}.html',
                'original_url': meta.get('original_url', f'https://github.com/Caro-Li-C/opc-content-source/blob/main/policy/{md}')
            })
            
            p_html += (
                '      <div class="timeline-item">\n'
                + '        <div class="timeline-date">' + str(meta.get("date", "")) + '</div>\n'
                + '        <a href="' + slug + '.html" class="timeline-content">\n'
                + '          <div class="timeline-title">' + title + '</div>\n'
                + '          <div class="timeline-city">' + str(meta.get("city", "")) + '</div>\n'
                + '        </a>\n'
                + '      </div>\n'
            )
        
        # 提取省份名（去掉"第X章"前缀）
        ch_name = ch['name']
        if " " in ch_name:
            ch_name = ch_name.split(" ", 1)[1]
        
        ch_tpl = (
            "---\n"
            "layout: default\n"
            "title: " + ch_name + "\n"
            "---\n"
            "\n"
            "<style>\n"
            "  .article-container { max-width: 780px; margin: 0 auto; padding: 40px 24px 80px; }\n"
            "  .timeline { position: relative; padding-left: 32px; }\n"
            "  .timeline::before { content: \"\"; position: absolute; left: 6px; top: 0; bottom: 0; width: 2px; background: #eee; }\n"
            "  .timeline-item { position: relative; padding-bottom: 32px; }\n"
            "  .timeline-item::before { content: \"\"; position: absolute; left: -32px; top: 4px; width: 12px; height: 12px; border-radius: 50%; background: #1a1a1a; border: 3px solid #fff; box-shadow: 0 0 0 2px #1a1a1a; }\n"
            "  .timeline-date { font-size: 12px; color: #bbb; letter-spacing: 1px; margin-bottom: 4px; font-family: \"SF Mono\", monospace; }\n"
            "  .timeline-content { background: #fff; border: 1px solid #eee; padding: 20px 24px; border-radius: 8px; text-decoration: none; color: #1a1a1a; display: block; transition: all 0.3s; }\n"
            "  .timeline-content:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-color: #1a1a1a; }\n"
            "  .timeline-title { font-size: 15px; line-height: 1.6; margin-bottom: 8px; font-weight: 500; }\n"
            "  .timeline-city { font-size: 12px; color: #999; }\n"
            "  .top-bar { background: #1a1a1a; padding: 16px 0; }\n"
            "  .top-bar a { display: block; max-width: 780px; margin: 0 auto; padding: 0 24px; color: #888; text-decoration: none; font-size: 12px; letter-spacing: 1px; transition: color 0.3s; }\n"
            "  .top-bar a:hover { color: #fff; }\n"
            "  .back { margin-top: 60px; font-size: 12px; }\n"
            "  .back a { color: #bbb; text-decoration: none; letter-spacing: 1px; transition: color 0.3s; }\n"
            "  .back a:hover { color: #1a1a1a; }\n"
            "  .chapter-label { font-size: 12px; color: #888; letter-spacing: 2px; margin-bottom: 10px; }\n"
            "</style>\n"
            "\n"
            "<div class=\"top-bar\">\n"
            "    <a href=\"../\">← 返回 全国OPC政策汇编</a>\n"
            "</div>\n"
            "\n"
            "<div class=\"article-container\">\n"
            "    <div class=\"chapter-label\">第" + CN[i] + "章</div>\n"
            "    <h1 style=\"font-size:28px;font-weight:400;padding-bottom:16px;margin-bottom:40px;letter-spacing:2px;\">" + ch_name + "</h1>\n"
            "    <div class=\"timeline\">\n"
            + (p_html if p_html else "<div style='color:#888;font-size:14px;'>暂无政策文件</div>") +
            "    </div>\n"
            "    <div class=\"back\">\n"
            "        <a href=\"../../\">← 返回 全国OPC政策汇编</a>\n"
            "    </div>\n"
            "</div>\n"
        )
        (ch_dir / 'index.html').write_text(ch_tpl, encoding='utf-8')

# 生成 _data/policies.yml（按真实 date 倒序）
policies_data.sort(key=lambda x: x['date'], reverse=True)

with open(data_dir / 'policies.yml', 'w', encoding='utf-8') as f:
    yaml.dump(policies_data, f, allow_unicode=True, sort_keys=False)

print(f"✓ 生成 _data/policies.yml，共 {len(policies_data)} 条")
print("完成")
