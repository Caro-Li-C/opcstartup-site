#!/usr/bin/env python3
"""
generate_analysis_pages.py - 政策解析页面生成脚本
改进版：标题去重、装饰过滤、独立编号提升、section 对齐修复
"""
import os
import re
import yaml
from pathlib import Path
from datetime import datetime

SOURCE_DIR = Path("_tmp_source/analysis")
OUTPUT_DIR = Path("policy/analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 装饰性内容黑名单（小写）
DECORATIVE_WORDS = {
    "cold", "take", "labo", "▎", "---", "***", "===",
    "policy depth interpretation", "policy interpretation",
    "政策深度解读", "深度解读", "政策解读"
}

# 标题重复检测阈值
DEDUP_THRESHOLD = 0.65


def slugify(title):
    return re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "-").replace("_", "-")[:50]


def jaccard_similarity(a, b):
    set_a, set_b = set(a), set(b)
    if not set_a and not set_b:
        return 1.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return inter / union if union else 0.0


def is_decorative(text):
    t = text.strip()
    if not t:
        return True
    if len(t) <= 2 and not any(c.isalnum() for c in t):
        return True
    lower = t.lower()
    for word in DECORATIVE_WORDS:
        if lower == word or lower.startswith(word + " ") or lower.endswith(" " + word):
            return True
    if re.match(r'^[A-Za-z]+$', t) and len(t) <= 6:
        return True
    return False


def is_title_duplicate(title, paragraph):
    title_core = re.sub(r'^[^:]+[：:]', '', title).strip()
    if title_core and len(title_core) > 8:
        if title_core in paragraph or paragraph in title_core:
            return True
    return jaccard_similarity(title, paragraph) >= DEDUP_THRESHOLD


def parse_markdown_body(body, title):
    lines = body.strip().split("
")
    html_parts = []
    chapter_idx = 0
    in_chapter = False
    chapter_buffer = []
    in_numbered = False
    numbered_buffer = []
    numbered_num = ""
    first_para = True
    i = 0

    def flush_chapter():
        nonlocal in_chapter, chapter_buffer, chapter_idx
        if in_chapter and chapter_buffer:
            chapter_idx += 1
            html_parts.append(render_chapter(chapter_idx, chapter_buffer))
            chapter_buffer = []
            in_chapter = False

    def flush_numbered():
        nonlocal in_numbered, numbered_buffer, numbered_num
        if in_numbered and numbered_buffer:
            html_parts.append(render_numbered(numbered_num, numbered_buffer))
            numbered_buffer = []
            numbered_num = ""
            in_numbered = False

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            flush_chapter()
            flush_numbered()
            i += 1
            continue

        # 1. 过滤与标题重复或装饰性内容
        if is_title_duplicate(title, line) or is_decorative(line):
            i += 1
            continue

        # 2. 结语
        if re.match(r"^#{1,2}\s*结语", line) or re.match(r"^#{1,2}\s*Conclusion", line, re.I):
            flush_chapter()
            flush_numbered()
            conclusion_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("#"):
                if lines[i].strip() and not is_decorative(lines[i].strip()):
                    conclusion_lines.append(lines[i].strip())
                i += 1
            html_parts.append(render_conclusion(conclusion_lines))
            continue

        # 3. 独立编号行：纯数字（如 03, 4）且下一行有内容
        m_num = re.match(r"^(\d{1,2})$", line)
        if m_num:
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if next_line and not re.match(r"^\d{1,2}$", next_line) and not is_decorative(next_line):
                flush_chapter()
                flush_numbered()
                in_numbered = True
                numbered_num = m_num.group(1).zfill(2)
                numbered_buffer.append(("title", next_line))
                i += 2
                continue

        # 4. ## 标题
        h2_match = re.match(r"^#{2}\s+(.+)$", line)
        if h2_match:
            h2_text = h2_match.group(1).strip()
            # 中文大章节（一、二、三...）
            cn_match = re.match(r"^(?:[一二三四五六七八九十]+、|第[一二三四五六七八九十\d]+条)\s*(.+)$", h2_text)
            if cn_match and len(h2_text) < 60:
                flush_numbered()
                flush_chapter()
                in_chapter = True
                chapter_buffer.append(("h2", cn_match.group(1)))
                i += 1
                continue
            # 数字编号章节（1. 创业启动资金 / 01 政策全貌）
            num_match = re.match(r"^(\d{1,2})[\.、\s)）]+(.+)$", h2_text)
            if num_match:
                flush_chapter()
                flush_numbered()
                in_numbered = True
                numbered_num = num_match.group(1).zfill(2)
                numbered_buffer.append(("title", num_match.group(2).strip()))
                i += 1
                continue
            # 普通 h2 → 作为 chapter
            flush_numbered()
            flush_chapter()
            in_chapter = True
            chapter_buffer.append(("h2", h2_text))
            i += 1
            continue

        # 5. ### 标题
        h3_match = re.match(r"^#{3}\s+(.+)$", line)
        if h3_match:
            h3_text = h3_match.group(1).strip()
            if in_numbered:
                numbered_buffer.append(("h3", h3_text))
            elif in_chapter:
                chapter_buffer.append(("h3", h3_text))
            else:
                html_parts.append(f"<h3>{h3_text}</h3>")
            i += 1
            continue

        # 6. 中文编号行（无 # 前缀，如 "一、政策核心内容"）
        cn_chapter = re.match(r"^(?:[一二三四五六七八九十]+、|第[一二三四五六七八九十\d]+条)\s*(.+)$", line)
        if cn_chapter and len(line) < 60:
            flush_numbered()
            flush_chapter()
            in_chapter = True
            chapter_buffer.append(("h2", cn_chapter.group(1)))
            i += 1
            continue

        # 7. KV 行检测
        kv_match = re.match(r"^(.+?)[：:	]+(.+)$", line)
        if kv_match and len(line) < 300:
            key = kv_match.group(1).strip()
            val = kv_match.group(2).strip()
            if not is_decorative(key) and not is_decorative(val) and not is_title_duplicate(title, key + val):
                if in_numbered:
                    numbered_buffer.append(("kv", (key, val)))
                elif in_chapter:
                    chapter_buffer.append(("kv", (key, val)))
                else:
                    html_parts.append(render_kv_row(key, val))
                i += 1
                continue

        # 8. 引用块
        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q = lines[i].strip()[1:].strip()
                if q and not is_decorative(q):
                    quote_lines.append(q)
                i += 1
            if quote_lines:
                text = " ".join(quote_lines)
                if in_numbered:
                    numbered_buffer.append(("quote", text))
                elif in_chapter:
                    chapter_buffer.append(("quote", text))
                else:
                    html_parts.append(render_highlight(text))
            continue

        # 9. 粗体段落
        if line.startswith("**") and line.endswith("**"):
            text = line[2:-2]
            if in_numbered:
                numbered_buffer.append(("strong_p", text))
            elif in_chapter:
                chapter_buffer.append(("strong_p", text))
            else:
                html_parts.append(f"<p><strong>{text}</strong></p>")
            i += 1
            continue

        # 10. 普通段落
        if in_numbered:
            numbered_buffer.append(("p", line))
        elif in_chapter:
            chapter_buffer.append(("p", line))
        else:
            if first_para and 50 <= len(line) <= 200:
                html_parts.append(f'<div class="drop-cap-section"><p>{line}</p></div>')
            else:
                html_parts.append(f"<p>{line}</p>")
            first_para = False
        i += 1

    flush_chapter()
    flush_numbered()
    return "
".join(html_parts)


def render_chapter(idx, items):
    h2_title = ""
    h3_sub = ""
    body_parts = []
    kv_rows = []
    for typ, content in items:
        if typ == "h2":
            h2_title = content
        elif typ == "h3":
            h3_sub = content
        elif typ == "quote":
            body_parts.append(render_highlight(content))
        elif typ == "strong_p":
            body_parts.append(f"<p><strong>{content}</strong></p>")
        elif typ == "kv":
            k, v = content
            kv_rows.append(render_kv_row(k, v))
        elif typ == "p":
            body_parts.append(f"<p>{content}</p>")
    sub_html = f'<div class="chapter-sub">{h3_sub}</div>' if h3_sub else ""
    kv_html = f'<div class="kv-grid">
{"
".join(kv_rows)}
</div>' if kv_rows else ""
    body_html = "
".join(body_parts)
    return f"""  <div class="chapter">
    <div class="chapter-number">{idx}</div>
    <div class="chapter-content">
      <h2>{h2_title}</h2>
{sub_html}
{kv_html}
{body_html}
    </div>
  </div>"""


def render_numbered(num, items):
    title = ""
    body_parts = []
    kv_rows = []
    for typ, content in items:
        if typ == "title":
            title = content
        elif typ == "h3":
            body_parts.append(f"<h3>{content}</h3>")
        elif typ == "quote":
            body_parts.append(render_highlight(content))
        elif typ == "strong_p":
            body_parts.append(f"<p><strong>{content}</strong></p>")
        elif typ == "kv":
            k, v = content
            kv_rows.append(render_kv_row(k, v))
        elif typ == "p":
            body_parts.append(f"<p>{content}</p>")
    kv_html = f'<div class="kv-grid">
{"
".join(kv_rows)}
</div>' if kv_rows else ""
    body_html = "
".join(body_parts)
    return f"""  <div class="numbered-section">
    <div class="section-header">
      <span class="section-num">{num}</span>
      <span class="section-title">{title}</span>
    </div>
    <div class="section-body">
{kv_html}
{body_html}
    </div>
  </div>"""


def render_kv_row(key, val):
    return f"""      <div class="kv-row">
        <div class="kv-key">{key}</div>
        <div class="kv-val">{val}</div>
      </div>"""


def render_highlight(text):
    text = re.sub(r"^\*\*(.+?)：\*\*", r"<strong>：</strong>", text)
    text = re.sub(r"^\*\*(.+?):\*\*", r"<strong>：</strong>", text)
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
    closing_html = f'
    <div class="closing-line">{closing_line}</div>' if closing_line else ""
    return f"""  <div class="conclusion">
    <h2>结语</h2>
{"
".join(["    " + p for p in paragraphs])}{closing_html}
  </div>"""


CSS_TEMPLATE = """
@import url("https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap");
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --ink: #1a1a1a; --charcoal: #2d2d2d; --warm-gray: #8a8279; --mist: #e8e4df; --parchment: #f5f3f0; --brass: #b8956a; --brass-light: #d4b896; --brass-dim: rgba(184,149,106,0.12); --white: #ffffff; --bg-warm: #faf8f5; --card-bg: #ffffff; --card-border: #edeae6; }
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
.headline-area .headline-lead { font-size: 18px; color: var(--warm-gray); line-height: 1.8; max-width: 560px; font-weight: 400; }
.drop-cap-section { margin-bottom: 48px; }
.drop-cap-section p { font-size: 16px; line-height: 2; color: var(--charcoal); text-align: justify; }
.drop-cap-section p::first-letter { font-family: "Noto Serif SC", serif; font-size: 72px; font-weight: 900; float: left; line-height: 0.8; margin-right: 12px; margin-top: 8px; color: var(--brass); }
.section-divider { height: 2px; background: linear-gradient(to right, var(--brass), transparent); margin: 48px 0; max-width: 200px; }

/* Chapter */
.chapter { margin-bottom: 48px; display: flex; gap: 24px; align-items: flex-start; }
.chapter-number { flex-shrink: 0; width: 48px; height: 48px; background: var(--ink); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--brass-light); font-family: "Noto Serif SC", serif; font-size: 18px; font-weight: 700; margin-top: 4px; }
.chapter-content { flex: 1; }
.chapter-content h2 { font-family: "Noto Serif SC", serif; font-size: 22px; font-weight: 700; color: var(--ink); margin-bottom: 4px; line-height: 1.4; }
.chapter-content .chapter-sub { font-size: 14px; color: var(--warm-gray); margin-bottom: 16px; font-style: italic; }
.chapter-content p { font-size: 16px; line-height: 2; color: var(--charcoal); margin-bottom: 16px; text-align: justify; }
.chapter-content p:last-child { margin-bottom: 0; }

/* Numbered section — 核心对齐修复 */
.numbered-section { margin: 24px 0; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; margin-left: -60px; padding: 24px; padding-left: 0; }
.section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--mist); padding-left: 52px; }
.section-num { font-family: "Noto Serif SC", serif; font-size: 28px; font-weight: 700; color: var(--brass); width: 40px; min-width: 40px; max-width: 40px; text-align: center; flex-shrink: 0; line-height: 1; padding: 0; margin-left: -52px; }
.section-title { font-family: "Noto Serif SC", serif; font-size: 18px; font-weight: 600; color: var(--ink); flex: 1; }
.section-body { padding-left: 52px; }
.section-body p { font-size: 15px; line-height: 1.9; color: var(--charcoal); margin-bottom: 10px; }
.section-body p:last-child { margin-bottom: 0; }

/* KV grid */
.kv-grid { margin: 20px 0; display: flex; flex-direction: column; gap: 2px; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; overflow: hidden; }
.kv-row { display: flex; align-items: flex-start; gap: 16px; padding: 14px 20px; border-bottom: 1px solid var(--mist); }
.kv-row:last-child { border-bottom: none; }
.kv-row:hover { background: var(--bg-warm); }
.kv-key { font-size: 13px; font-weight: 600; color: var(--warm-gray); min-width: 80px; max-width: 120px; flex-shrink: 0; letter-spacing: 0.5px; padding-top: 2px; }
.kv-val { font-size: 15px; color: var(--charcoal); line-height: 1.7; flex: 1; }

/* Highlight box */
.highlight-box { background: var(--parchment); border-left: 4px solid var(--brass); padding: 24px 28px; margin: 24px 0; font-size: 15px; line-height: 1.8; color: var(--charcoal); }
.highlight-box strong { color: var(--ink); font-weight: 600; }

/* Conclusion */
.conclusion { margin-top: 64px; padding-top: 32px; border-top: 2px solid var(--ink); }
.conclusion h2 { font-family: "Noto Serif SC", serif; font-size: 24px; font-weight: 700; color: var(--ink); margin-bottom: 20px; }
.conclusion p { font-size: 16px; line-height: 2; color: var(--charcoal); margin-bottom: 16px; text-align: justify; }
.conclusion .closing-line { font-family: "Noto Serif SC", serif; font-size: 18px; font-weight: 700; color: var(--brass); margin-top: 24px; text-align: center; letter-spacing: 2px; }

/* Footer */
.article-footer { margin-top: 64px; padding-top: 24px; border-top: 1px solid var(--mist); display: flex; justify-content: space-between; align-items: center; }
.footer-author { font-size: 14px; color: var(--warm-gray); }
.footer-author strong { color: var(--ink); font-weight: 600; }
.footer-source { font-size: 13px; color: var(--warm-gray); letter-spacing: 1px; }
.back-link { text-align: center; margin-top: 48px; }
.back-link a { display: inline-flex; align-items: center; gap: 8px; color: var(--warm-gray); text-decoration: none; font-size: 14px; transition: color 0.2s; padding: 10px 24px; border: 1px solid var(--mist); }
.back-link a:hover { color: var(--brass); border-color: var(--brass-light); }

@media (max-width: 640px) {
  .headline-area h1 { font-size: 28px; }
  .chapter { gap: 16px; }
  .chapter-number { width: 36px; height: 36px; font-size: 14px; }
  .chapter-content h2 { font-size: 18px; }
  .drop-cap-section p::first-letter { font-size: 56px; }
  .numbered-section { margin-left: -46px; padding: 16px; padding-left: 0; }
  .section-header { padding-left: 44px; }
  .section-num { font-size: 22px; width: 32px; min-width: 32px; max-width: 32px; margin-left: -44px; }
  .section-title { font-size: 16px; }
  .section-body { padding-left: 44px; }
  .kv-row { flex-direction: column; gap: 4px; padding: 12px 16px; }
  .kv-key { min-width: auto; }
}
"""


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

    # 去重标签
    display_tags = []
    for t in tags:
        if t not in display_tags and t != "政策解析":
            display_tags.append(t)
    if not display_tags:
        display_tags = ["OPC"]

    # 副标题：超过30字不显示，且永远删除「政策深度解读」
    if description and len(description) <= 30 and description != "政策深度解读":
        sub_title = description
        lead_text = ""
    else:
        sub_title = ""
        lead_text = description if description and description != "政策深度解读" else ""

    body_html = parse_markdown_body(body, title)

    sub_title_html = f'<div class="headline-sub">{sub_title}</div>' if sub_title else ""

    html = f"""---
layout: default
title: "{title}"
---

<style>
{CSS_TEMPLATE}
</style>

<article class="article-container">

  <div class="article-meta-bar">
    <div class="meta-left">
      <span class="meta-tag">政策解析</span>
      <div class="meta-divider"></div>
      <span class="meta-text">{city if city else display_tags[0]}</span>
      <div class="meta-divider"></div>
      <span class="meta-text">{display_tags[1] if len(display_tags) > 1 else display_tags[0]}</span>
    </div>
    <div class="meta-right">{date_str}</div>
  </div>

  <div class="headline-area">
    <h1>{title}</h1>
{sub_title_html}
    {f'<p class="headline-lead">{lead_text}</p>' if lead_text else ''}
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
