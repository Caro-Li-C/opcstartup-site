#!/usr/bin/env python3
"""
generate_analysis_pages.py - 政策解析页面生成脚本
统一排版：杂志画报版（无表头）
"""
import os
import re
import yaml
from pathlib import Path
from datetime import datetime

SOURCE_DIR = Path("_tmp_source/analysis")
OUTPUT_DIR = Path("policy/analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def slugify(title):
    return re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "-").replace("_", "-")[:50]


def parse_markdown_body(body):
    lines = body.strip().split("\n")
    html_parts = []
    chapter_idx = 0
    in_chapter = False
    chapter_buffer = []
    first_para = True
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            if in_chapter and chapter_buffer:
                html_parts.append(render_chapter(chapter_idx, chapter_buffer))
                chapter_buffer = []
                in_chapter = False
            i += 1
            continue
        if re.match(r"^#{1,2}\s*结语", line) or re.match(r"^#{1,2}\s*Conclusion", line, re.I):
            if in_chapter and chapter_buffer:
                html_parts.append(render_chapter(chapter_idx, chapter_buffer))
                chapter_buffer = []
                in_chapter = False
            conclusion_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("#"):
                if lines[i].strip():
                    conclusion_lines.append(lines[i].strip())
                i += 1
            html_parts.append(render_conclusion(conclusion_lines))
            continue
        h2_match = re.match(r"^#{2}\s+(.+)$", line)
        if h2_match:
            if in_chapter and chapter_buffer:
                html_parts.append(render_chapter(chapter_idx, chapter_buffer))
                chapter_buffer = []
            chapter_idx += 1
            in_chapter = True
            chapter_buffer.append(("h2", h2_match.group(1)))
            i += 1
            continue
        h3_match = re.match(r"^#{3}\s+(.+)$", line)
        if h3_match:
            if in_chapter:
                chapter_buffer.append(("h3", h3_match.group(1)))
            i += 1
            continue
        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            if in_chapter:
                chapter_buffer.append(("quote", " ".join(quote_lines)))
            else:
                html_parts.append(render_highlight(" ".join(quote_lines)))
            continue
        if line.startswith("**") and line.endswith("**"):
            text = line[2:-2]
            if in_chapter:
                chapter_buffer.append(("strong_p", text))
            else:
                html_parts.append(f"<p><strong>{text}</strong></p>")
            i += 1
            continue
        if first_para and not in_chapter:
            html_parts.append(f"<div class=\"drop-cap-section\"><p>{line}</p></div>")
            first_para = False
        elif in_chapter:
            chapter_buffer.append(("p", line))
        else:
            html_parts.append(f"<p>{line}</p>")
        i += 1
    if in_chapter and chapter_buffer:
        html_parts.append(render_chapter(chapter_idx, chapter_buffer))
    return "\n".join(html_parts)


def render_chapter(idx, items):
    h2_title = ""
    h3_sub = ""
    body_parts = []
    for typ, content in items:
        if typ == "h2":
            h2_title = content
        elif typ == "h3":
            h3_sub = content
        elif typ == "quote":
            body_parts.append(render_highlight(content))
        elif typ == "strong_p":
            body_parts.append(f"<p><strong>{content}</strong></p>")
        elif typ == "p":
            body_parts.append(f"<p>{content}</p>")
    sub_html = f"<div class=\"chapter-sub\">{h3_sub}</div>" if h3_sub else ""
    body_html = "\n".join(body_parts)
    return f"""  <div class="chapter">
    <div class="chapter-number">{idx}</div>
    <div class="chapter-content">
      <h2>{h2_title}</h2>
{sub_html}
{body_html}
    </div>
  </div>"""


def render_highlight(text):
    text = re.sub(r"^\*\*(.+?)：\*\*", r"<strong>\1：</strong>", text)
    text = re.sub(r"^\*\*(.+?):\*\*", r"<strong>\1：</strong>", text)
    return f"""      <div class="highlight-box">
        {text}
      </div>"""


def render_conclusion(lines):
    paragraphs = []
    closing_line = ""
    for line in lines:
        if len(line) < 50 and ("是" in line or "信用" in line or "承诺" in line):
            closing_line = line
        else:
            paragraphs.append(f"<p>{line}</p>")
    closing_html = f"\n    <div class=\"closing-line\">{closing_line}</div>" if closing_line else ""
    return f"""  <div class="conclusion">
    <h2>结语</h2>
{chr(10).join(["    " + p for p in paragraphs])}{closing_html}
  </div>"""


articles = []

for filename in sorted(os.listdir(SOURCE_DIR)):
    if not filename.endswith(".md"):
        continue
    filepath = SOURCE_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    fm = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
            except:
                pass
            body = parts[2].strip()
    name = filename.replace(".md", "")
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", name)
    date_str = str(fm.get("date", ""))
    if not date_str and m:
        date_str = m.group(1)
    if not date_str:
        date_str = "2026-06-25"
    title = fm.get("title", m.group(2).replace("-", "") if m else name)
    slug = slugify(title)
    author = fm.get("author", "潇韬")
    description = fm.get("description", fm.get("summary", ""))
    tags = fm.get("tags", ["政策解析", "OPC"])
    city = fm.get("city", "")
    body_html = parse_markdown_body(body)
    lead_text = description if description else ""
    tags_html = "".join([f"<span class=\"meta-text\">{t}</span>" for t in tags[:3]])

    html = f"""---
layout: default
title: "{title}"
---

<style>
@import url("https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap");
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --ink: #1a1a1a; --charcoal: #2d2d2d; --warm-gray: #8a8279; --mist: #e8e4df; --parchment: #f5f3f0; --brass: #b8956a; --brass-light: #d4b896; --brass-dim: rgba(184,149,106,0.12); --white: #ffffff; --bg-warm: #faf8f5; }
body { font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; background: var(--bg-warm); color: var(--ink); line-height: 1.85; -webkit-font-smoothing: antialiased; }
.article-container { max-width: 720px; margin: 0 auto; padding: 48px 24px 80px; }
.article-meta-bar { display: flex; align-items: center; justify-content: space-between; padding: 24px 0; border-bottom: 1px solid var(--mist); margin-bottom: 48px; }
.meta-left { display: flex; align-items: center; gap: 16px; }
.meta-tag { font-size: 12px; padding: 6px 16px; background: var(--brass-dim); color: var(--brass); font-weight: 600; letter-spacing: 1px; }
.meta-divider { width: 1px; height: 16px; background: var(--mist); }
.meta-text { font-size: 13px; color: var(--warm-gray); }
.meta-right { font-size: 13px; color: var(--warm-gray); }
.headline-area { margin-bottom: 48px; }
.headline-area h1 { font-family: "Noto Serif SC", serif; font-size: 42px; font-weight: 900; line-height: 1.2; color: var(--ink); margin-bottom: 8px; letter-spacing: 1px; }
.headline-area .headline-sub { font-family: "Noto Serif SC", serif; font-size: 42px; font-weight: 900; line-height: 1.2; color: var(--brass); margin-bottom: 24px; letter-spacing: 1px; }
.headline-area .headline-lead { font-size: 18px; color: var(--warm-gray); line-height: 1.8; max-width: 560px; font-weight: 400; }
.drop-cap-section { margin-bottom: 48px; }
.drop-cap-section p { font-size: 16px; line-height: 2; color: var(--charcoal); text-align: justify; }
.drop-cap-section p::first-letter { font-family: "Noto Serif SC", serif; font-size: 72px; font-weight: 900; float: left; line-height: 0.8; margin-right: 12px; margin-top: 8px; color: var(--brass); }
.section-divider { height: 2px; background: linear-gradient(to right, var(--brass), transparent); margin: 48px 0; max-width: 200px; }
.chapter { margin-bottom: 48px; display: flex; gap: 24px; align-items: flex-start; }
.chapter-number { flex-shrink: 0; width: 48px; height: 48px; background: var(--ink); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--brass-light); font-family: "Noto Serif SC", serif; font-size: 18px; font-weight: 700; margin-top: 4px; }
.chapter-content { flex: 1; }
.chapter-content h2 { font-family: "Noto Serif SC", serif; font-size: 22px; font-weight: 700; color: var(--ink); margin-bottom: 4px; line-height: 1.4; }
.chapter-content .chapter-sub { font-size: 14px; color: var(--warm-gray); margin-bottom: 16px; font-style: italic; }
.chapter-content p { font-size: 16px; line-height: 2; color: var(--charcoal); margin-bottom: 16px; text-align: justify; }
.chapter-content p:last-child { margin-bottom: 0; }
.highlight-box { background: var(--parchment); border-left: 4px solid var(--brass); padding: 24px 28px; margin: 24px 0; font-size: 15px; line-height: 1.8; color: var(--charcoal); }
.highlight-box strong { color: var(--ink); font-weight: 600; }
.conclusion { margin-top: 64px; padding-top: 32px; border-top: 2px solid var(--ink); }
.conclusion h2 { font-family: "Noto Serif SC", serif; font-size: 24px; font-weight: 700; color: var(--ink); margin-bottom: 20px; }
.conclusion p { font-size: 16px; line-height: 2; color: var(--charcoal); margin-bottom: 16px; text-align: justify; }
.conclusion .closing-line { font-family: "Noto Serif SC", serif; font-size: 18px; font-weight: 700; color: var(--brass); margin-top: 24px; text-align: center; letter-spacing: 2px; }
.article-footer { margin-top: 64px; padding-top: 24px; border-top: 1px solid var(--mist); display: flex; justify-content: space-between; align-items: center; }
.footer-author { font-size: 14px; color: var(--warm-gray); }
.footer-author strong { color: var(--ink); font-weight: 600; }
.footer-source { font-size: 13px; color: var(--warm-gray); letter-spacing: 1px; }
.back-link { text-align: center; margin-top: 48px; }
.back-link a { display: inline-flex; align-items: center; gap: 8px; color: var(--warm-gray); text-decoration: none; font-size: 14px; transition: color 0.2s; padding: 10px 24px; border: 1px solid var(--mist); }
.back-link a:hover { color: var(--brass); border-color: var(--brass-light); }
@media (max-width: 640px) { .headline-area h1, .headline-area .headline-sub { font-size: 28px; } .chapter { gap: 16px; } .chapter-number { width: 36px; height: 36px; font-size: 14px; } .chapter-content h2 { font-size: 18px; } .drop-cap-section p::first-letter { font-size: 56px; } }
</style>

<article class="article-container">

  <div class="article-meta-bar">
    <div class="meta-left">
      <span class="meta-tag">政策解析</span>
      <div class="meta-divider"></div>
      <span class="meta-text">{city if city else "OPC"}</span>
      <div class="meta-divider"></div>
      <span class="meta-text">{tags[0] if tags else "OPC"}</span>
    </div>
    <div class="meta-right">{date_str}</div>
  </div>

  <div class="headline-area">
    <h1>{title}</h1>
    <div class="headline-sub">{description if description else "政策深度解读"}</div>
    <p class="headline-lead">{lead_text}</p>
  </div>

{body_html}

  <div class="article-footer">
    <div class="footer-author">
      <strong>{author}</strong> · OPC创业汇
    </div>
    <div class="footer-source">POLICY · PRACTICE · PEOPLE</div>
  </div>

  <div class="back-link">
    <a href="./">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      返回政策解析列表
    </a>
  </div>

</article>
"""

    with open(OUTPUT_DIR / f"{slug}.html", "w", encoding="utf-8") as f:
        f.write(html)

    dt = datetime.strptime(str(date_str), "%Y-%m-%d")
    articles.append({
        "title": title,
        "url": f"/policy/analysis/{slug}.html",
        "date": date_str,
        "day": dt.strftime("%d"),
        "month_year": dt.strftime("%m/%Y"),
        "desc": description
    })

    print(f"✓ {filename}")


items = ""
for art in sorted(articles, key=lambda x: x["date"], reverse=True):
    items += f"""
    <article class="post-item">
      <div class="post-left">
        <div class="post-date-day">{art["day"]}</div>
        <div class="post-date-month">{art["month_year"]}</div>
      </div>
      <div class="post-main">
        <h2 class="post-title"><a href="{art["url"]}">{art["title"]}</a></h2>
        <p class="post-description">{art["desc"]}</p>
        <div class="post-footer">
          <div class="post-tags-inline">
            <span class="post-tag-inline">政策解析</span>
          </div>
        </div>
      </div>
    </article>"""

index_html = f"""---
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
"""

with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
    f.write(index_html)


data_dir = Path("_data")
data_dir.mkdir(exist_ok=True)

analysis_data = []
for art in sorted(articles, key=lambda x: x["date"], reverse=True):
    analysis_data.append({
        "title": art["title"],
        "url": art["url"],
        "date": art["date"],
        "description": art["desc"]
    })

with open(data_dir / "analysis.yml", "w", encoding="utf-8") as f:
    yaml.dump(analysis_data, f, allow_unicode=True, sort_keys=False)

print(f"\n✅ 完成！共 {len(articles)} 篇文章 + 列表页 + _data/analysis.yml")
