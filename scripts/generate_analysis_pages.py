#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_analysis_pages.py
批量将 OPC 政策解析 Markdown 文件转换为结构化的多文章 HTML 预览页。

改进特性：
1. 自动删除与标题重复的正文内容
2. 删除 "政策深度解读" 等冗余 headline-sub
3. 过滤装饰性内容（COLD, TAKE, Labo, 纯符号等）
4. 独立编号识别：正文中的孤立数字（03/04/05）自动提升为独立 section
5. section-num 与 chapter-number 严格左对齐（负 margin 方案）
6. KV 行智能过滤：删除无意义或重复的 KV 对
7. 移动端响应式适配
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# =============================================================================
# 配置
# =============================================================================

INPUT_DIR = Path("./_analysis")      # Markdown 源文件目录
OUTPUT_DIR = Path("./_site/analysis") # HTML 输出目录
OUTPUT_FILE = OUTPUT_DIR / "index.html" # 合并输出文件

# 装饰性内容黑名单（小写）
DECORATIVE_WORDS = {
    "cold", "take", "labo", "▎", "---", "***", "===", 
    "policy depth interpretation", "policy interpretation",
    "政策深度解读", "深度解读", "政策解读"
}

# 独立编号正则：匹配行首的 01-99 或 1-9 纯数字
SECTION_NUMBER_RE = re.compile(r'^(\d{1,2})$')

# KV 行正则：匹配 "key  value" 或 "key: value" 或 "key	value"
KV_RE = re.compile(r'^(?P<key>[^：:]+)[：:\t]+(?P<val>.+)$')

# 标题重复检测阈值（Jaccard 相似度）
DEDUP_SIMILARITY_THRESHOLD = 0.65


# =============================================================================
# HTML 模板
# =============================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<style>
@import url("https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap");
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
  --ink: #1a1a1a; --charcoal: #2d2d2d; --warm-gray: #8a8279;
  --mist: #e8e4df; --parchment: #f5f3f0; --brass: #b8956a;
  --brass-light: #d4b896; --brass-dim: rgba(184,149,106,0.12);
  --white: #ffffff; --bg-warm: #faf8f5; --bg-cream: #fdfcfa;
  --card-bg: #ffffff; --card-border: #edeae6;
}}
body {{
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  background: var(--bg-warm); color: var(--ink); line-height: 1.85;
  -webkit-font-smoothing: antialiased;
}}

/* 导航栏 */
.nav-bar {{
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  background: rgba(250, 248, 245, 0.95); backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--mist); padding: 12px 24px;
  display: flex; align-items: center; gap: 16px; overflow-x: auto;
}}
.nav-bar h3 {{
  font-family: "Noto Serif SC", serif; font-size: 16px; font-weight: 700;
  color: var(--ink); white-space: nowrap; margin-right: 12px;
}}
.nav-bar a {{
  font-size: 13px; color: var(--warm-gray); text-decoration: none;
  padding: 6px 14px; border: 1px solid var(--mist); border-radius: 20px;
  white-space: nowrap; transition: all 0.2s;
}}
.nav-bar a:hover {{
  color: var(--brass); border-color: var(--brass-light); background: var(--brass-dim);
}}
.nav-spacer {{ height: 60px; }}

/* 文章容器 */
.article-container {{ max-width: 720px; margin: 0 auto; padding: 48px 24px 80px; }}

/* Meta bar */
.article-meta-bar {{
  display: flex; align-items: center; justify-content: space-between;
  padding: 24px 0; border-bottom: 1px solid var(--mist); margin-bottom: 48px;
}}
.meta-left {{ display: flex; align-items: center; gap: 16px; }}
.meta-tag {{
  font-size: 12px; padding: 6px 16px; background: var(--brass-dim);
  color: var(--brass); font-weight: 600; letter-spacing: 1px;
}}
.meta-divider {{ width: 1px; height: 16px; background: var(--mist); }}
.meta-text {{ font-size: 13px; color: var(--warm-gray); }}
.meta-right {{ font-size: 13px; color: var(--warm-gray); }}

/* Headline */
.headline-area {{ margin-bottom: 56px; }}
.headline-area h1 {{
  font-family: "Noto Serif SC", serif; font-size: 40px; font-weight: 900;
  line-height: 1.25; color: var(--ink); margin-bottom: 12px; letter-spacing: 0.5px;
}}
.headline-area .headline-lead {{
  font-size: 17px; color: var(--warm-gray); line-height: 1.8;
  max-width: 560px; font-weight: 400; padding-left: 16px;
  border-left: 3px solid var(--brass-dim);
}}

/* Chapter */
.chapter {{ margin-bottom: 48px; display: flex; gap: 20px; align-items: flex-start; }}
.chapter-number {{
  flex-shrink: 0; width: 40px; height: 40px; background: var(--ink); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: var(--brass-light); font-family: "Noto Serif SC", serif;
  font-size: 16px; font-weight: 700; margin-top: 2px;
}}
.chapter-content {{ flex: 1; }}
.chapter-content h2 {{
  font-family: "Noto Serif SC", serif; font-size: 22px; font-weight: 700;
  color: var(--ink); margin-bottom: 16px; line-height: 1.4;
  padding-bottom: 8px; border-bottom: 1px solid var(--mist);
}}
.chapter-content h3 {{
  font-family: "Noto Serif SC", serif; font-size: 17px; font-weight: 600;
  color: var(--charcoal); margin: 20px 0 10px; padding-left: 12px;
  border-left: 3px solid var(--brass-light);
}}
.chapter-content p {{
  font-size: 15.5px; line-height: 2; color: var(--charcoal); margin-bottom: 14px; text-align: justify;
}}
.chapter-content p:last-child {{ margin-bottom: 0; }}

/* Part header */
.part-header {{
  margin: 48px 0 32px; padding: 16px 0; border-bottom: 2px solid var(--ink);
  font-family: "Noto Serif SC", serif; font-size: 18px; font-weight: 700;
}}
.part-label {{
  display: inline-block; background: var(--ink); color: var(--brass-light);
  padding: 4px 12px; border-radius: 4px; margin-right: 12px; font-size: 14px;
}}

/* Numbered section — 核心对齐方案 */
.numbered-section {{
  margin: 24px 0; background: var(--card-bg);
  border: 1px solid var(--card-border); border-radius: 12px;
  /* 负 margin 让卡片左边缘与 chapter-number 左边缘对齐 */
  margin-left: -60px;
  padding: 24px;
  padding-left: 0;
}}
.section-header {{
  display: flex; align-items: center; gap: 12px; margin-bottom: 16px;
  padding-bottom: 12px; border-bottom: 1px solid var(--mist);
  padding-left: 52px; /* 40px num + 12px gap */
}}
.section-num {{
  font-family: "Noto Serif SC", serif; font-size: 28px; font-weight: 700;
  color: var(--brass);
  width: 40px; min-width: 40px; max-width: 40px;
  text-align: center; flex-shrink: 0; line-height: 1; padding: 0;
  /* 负 margin 让 section-num 左边缘与 chapter-number 左边缘严格对齐 */
  margin-left: -52px;
}}
.section-title {{
  font-family: "Noto Serif SC", serif; font-size: 18px; font-weight: 600;
  color: var(--ink); flex: 1;
}}
.section-body {{
  padding-left: 52px; /* 与 section-title 左对齐 */
}}
.section-body p {{
  font-size: 15px; line-height: 1.9; color: var(--charcoal); margin-bottom: 10px;
}}
.section-body p:last-child {{ margin-bottom: 0; }}

/* Emoji heading */
.emoji-heading {{
  display: flex; align-items: center; gap: 10px;
  margin: 20px 0 12px; padding: 12px 16px;
  background: var(--parchment); border-left: 4px solid var(--brass);
  border-radius: 0 8px 8px 0;
}}
.emoji-h-icon {{ font-size: 20px; }}
.emoji-h-title {{
  font-family: "Noto Serif SC", serif; font-size: 16px; font-weight: 600;
  color: var(--ink);
}}

/* Highlight box */
.highlight-box {{
  background: var(--parchment); border-left: 4px solid var(--brass);
  padding: 20px 24px; margin: 20px 0; font-size: 15px; line-height: 1.8; color: var(--charcoal);
  border-radius: 0 8px 8px 0;
}}
.highlight-box strong {{ color: var(--ink); font-weight: 600; }}

/* Table */
.table-wrap {{ margin: 20px 0; overflow-x: auto; border-radius: 8px; }}
.table-wrap table {{
  width: 100%; border-collapse: collapse; font-size: 14px;
  background: var(--white); border: 1px solid var(--mist);
  border-radius: 8px; overflow: hidden;
}}
.table-wrap th {{
  background: var(--parchment); padding: 12px 16px; text-align: left;
  font-weight: 600; color: var(--ink); border-bottom: 2px solid var(--brass);
  white-space: nowrap; font-size: 13px; letter-spacing: 0.5px;
}}
.table-wrap td {{
  padding: 10px 16px; border-bottom: 1px solid var(--mist);
  color: var(--charcoal); line-height: 1.6; font-size: 14px;
}}
.table-wrap tr:last-child td {{ border-bottom: none; }}
.table-wrap tr:hover td {{ background: var(--bg-cream); }}

/* List */
.article-list {{
  margin: 14px 0 14px 20px; padding: 0;
  font-size: 15px; line-height: 1.9; color: var(--charcoal);
}}
.article-list li {{ margin-bottom: 6px; }}

/* KV grid */
.kv-grid {{
  margin: 20px 0; display: flex; flex-direction: column; gap: 2px;
  background: var(--card-bg); border: 1px solid var(--card-border);
  border-radius: 12px; overflow: hidden;
}}
.kv-row {{
  display: flex; align-items: flex-start; gap: 16px;
  padding: 14px 20px; border-bottom: 1px solid var(--mist);
}}
.kv-row:last-child {{ border-bottom: none; }}
.kv-row:hover {{ background: var(--bg-cream); }}
.kv-key {{
  font-size: 13px; font-weight: 600; color: var(--warm-gray);
  min-width: 80px; max-width: 120px; flex-shrink: 0;
  letter-spacing: 0.5px; padding-top: 2px;
}}
.kv-val {{
  font-size: 15px; color: var(--charcoal); line-height: 1.7; flex: 1;
}}

/* Metric grid */
.metric-grid {{
  display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px; margin: 24px 0;
}}
.metric-card {{
  background: var(--card-bg); border: 1px solid var(--card-border);
  border-radius: 12px; padding: 20px 16px; text-align: center;
  transition: box-shadow 0.2s, transform 0.2s;
}}
.metric-card:hover {{
  box-shadow: 0 4px 20px rgba(0,0,0,0.06); transform: translateY(-2px);
}}
.metric-value {{
  font-family: "Noto Serif SC", serif; font-size: 32px; font-weight: 700;
  color: var(--brass); margin-bottom: 6px; line-height: 1;
}}
.metric-label {{
  font-size: 14px; font-weight: 600; color: var(--ink);
  margin-bottom: 4px; line-height: 1.4;
}}
.metric-sub {{
  font-size: 12px; color: var(--warm-gray); line-height: 1.4;
}}

/* Conclusion */
.conclusion {{ margin-top: 56px; padding-top: 32px; border-top: 2px solid var(--ink); }}
.conclusion h2 {{
  font-family: "Noto Serif SC", serif; font-size: 22px; font-weight: 700;
  color: var(--ink); margin-bottom: 20px;
}}
.conclusion p {{
  font-size: 15.5px; line-height: 2; color: var(--charcoal); margin-bottom: 14px; text-align: justify;
}}
.conclusion .closing-line {{
  font-family: "Noto Serif SC", serif; font-size: 17px; font-weight: 700;
  color: var(--brass); margin-top: 24px; text-align: center; letter-spacing: 2px;
}}

/* Footer */
.article-footer {{
  margin-top: 56px; padding-top: 24px; border-top: 1px solid var(--mist);
  display: flex; justify-content: space-between; align-items: center;
}}
.footer-author {{ font-size: 14px; color: var(--warm-gray); }}
.footer-author strong {{ color: var(--ink); font-weight: 600; }}
.footer-source {{ font-size: 13px; color: var(--warm-gray); letter-spacing: 1px; }}
.back-link {{ text-align: center; margin-top: 48px; }}
.back-link a {{
  display: inline-flex; align-items: center; gap: 8px; color: var(--warm-gray);
  text-decoration: none; font-size: 14px; transition: color 0.2s;
  padding: 10px 24px; border: 1px solid var(--mist); border-radius: 4px;
}}
.back-link a:hover {{ color: var(--brass); border-color: var(--brass-light); }}

/* Article separator */
.article-separator {{
  height: 80px; background: linear-gradient(to bottom, var(--bg-warm), var(--mist), var(--bg-warm));
  margin: 0; border: none;
}}

@media (max-width: 640px) {{
  .nav-bar {{ padding: 8px 16px; }}
  .nav-bar h3 {{ font-size: 14px; }}
  .nav-bar a {{ font-size: 12px; padding: 4px 10px; }}
  .headline-area h1 {{ font-size: 28px; }}
  .chapter {{ gap: 14px; }}
  .chapter-number {{ width: 32px; height: 32px; font-size: 13px; }}
  .chapter-content h2 {{ font-size: 18px; }}
  .numbered-section {{
    margin-left: -46px; /* 32px number + 14px gap */
    padding: 16px;
    padding-left: 0;
  }}
  .section-header {{ padding-left: 44px; }} /* 32px + 12px gap */
  .section-num {{
    font-size: 22px;
    width: 32px; min-width: 32px; max-width: 32px;
    margin-left: -44px;
  }}
  .section-title {{ font-size: 16px; }}
  .section-body {{ padding-left: 44px; }}
  .table-wrap {{ margin: 16px -12px; width: calc(100% + 24px); border-radius: 0; }}
  .table-wrap table {{ font-size: 13px; }}
  .table-wrap th, .table-wrap td {{ padding: 8px 12px; }}
  .kv-row {{ flex-direction: column; gap: 4px; padding: 12px 16px; }}
  .kv-key {{ min-width: auto; }}
  .metric-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .metric-value {{ font-size: 26px; }}
}}
</style>
<base target="_blank">
</head>
<body>

<!-- 导航栏 -->
<div class="nav-bar">
  <h3>📚 政策解析合集</h3>
{nav_links}
</div>
<div class="nav-spacer"></div>

{articles}

</body>
</html>
"""

ARTICLE_TEMPLATE = """
<article class="article-container" id="{article_id}">

  <div class="article-meta-bar">
    <div class="meta-left">
      <span class="meta-tag">政策解析</span>
      <div class="meta-divider"></div>
      <span class="meta-text">OPC</span>
      <div class="meta-divider"></div>
      <span class="meta-text">超级个体</span>
    </div>
    <div class="meta-right">{date}</div>
  </div>

  <div class="headline-area">
    <h1>{title}</h1>
    <p class="headline-lead">{lead}</p>
  </div>

{body}

  <div class="article-footer">
    <div class="footer-author">
      <strong>潇韬</strong> · OPC创业汇
    </div>
    <div class="footer-source">POLICY · PRACTICE · PEOPLE</div>
  </div>

</article>
<div class="article-separator"></div>
"""


# =============================================================================
# 工具函数
# =============================================================================

def jaccard_similarity(a: str, b: str) -> float:
    """计算两个字符串的 Jaccard 相似度（基于字符集合）"""
    set_a = set(a)
    set_b = set(b)
    if not set_a and not set_b:
        return 1.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0


def is_decorative(text: str) -> bool:
    """判断文本是否为装饰性/无意义内容"""
    t = text.strip()
    if not t:
        return True
    # 纯符号或极短
    if len(t) <= 2 and not any(c.isalnum() for c in t):
        return True
    # 黑名单匹配
    lower = t.lower()
    for word in DECORATIVE_WORDS:
        if lower == word or lower.startswith(word + " ") or lower.endswith(" " + word):
            return True
    # 纯英文无意义短词
    if re.match(r'^[A-Za-z]+$', t) and len(t) <= 6:
        return True
    return False


def is_title_duplicate(title: str, paragraph: str, threshold: float = DEDUP_SIMILARITY_THRESHOLD) -> bool:
    """判断段落是否与标题重复"""
    # 提取标题核心短语（去掉前缀城市名）
    title_core = re.sub(r'^[^:]+[：:]', '', title).strip()
    # 如果段落包含标题核心短语超过 80%，视为重复
    if title_core and len(title_core) > 8:
        if title_core in paragraph or paragraph in title_core:
            return True
    # Jaccard 相似度兜底
    sim = jaccard_similarity(title, paragraph)
    return sim >= threshold


def extract_front_matter(content: str) -> Tuple[Dict[str, str], str]:
    """提取 YAML front matter 和正文"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()
            fm = {}
            for line in fm_text.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"').strip("'")
            return fm, body
    return {}, content


def parse_date_from_filename(filename: str) -> str:
    """从文件名提取日期，默认返回空"""
    m = re.search(r'(20\d{2})[-]?(\d{2})[-]?(\d{2})', filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return ""


def md_to_html_paragraphs(md_body: str, title: str) -> str:
    """
    将 Markdown 正文转换为 HTML 结构。
    核心逻辑：
    1. 过滤与标题重复的段落
    2. 过滤装饰性内容
    3. 识别独立编号并提升为 section
    4. 解析 KV 行、列表、表格等
    """
    lines = md_body.split("\n")
    html_parts = []
    i = 0
    current_section = None
    in_list = False
    list_items = []
    in_kv = False
    kv_rows = []

    def flush_list():
        nonlocal in_list, list_items
        if in_list and list_items:
            html_parts.append(f'<ul class="article-list">\n{ "\n".join(list_items) }\n</ul>')
            list_items = []
            in_list = False

    def flush_kv():
        nonlocal in_kv, kv_rows
        if in_kv and kv_rows:
            html_parts.append(f'<div class="kv-grid">\n{ "\n".join(kv_rows) }\n</div>')
            kv_rows = []
            in_kv = False

    def flush_section():
        nonlocal current_section
        if current_section:
            html_parts.append("  </div>\n</div>")
            current_section = None

    def start_section(num: str, title_text: str):
        nonlocal current_section
        flush_section()
        flush_list()
        flush_kv()
        current_section = num
        html_parts.append(
            f'<div class="numbered-section">\n'
            f'  <div class="section-header">\n'
            f'    <span class="section-num">{num}</span>\n'
            f'    <span class="section-title">{title_text}</span>\n'
            f'  </div>\n'
            f'  <div class="section-body">'
        )

    while i < len(lines):
        line = lines[i].strip()
        raw_line = lines[i]

        # 跳过空行
        if not line:
            flush_list()
            flush_kv()
            i += 1
            continue

        # 1. 过滤与标题重复
        if is_title_duplicate(title, line):
            i += 1
            continue

        # 2. 过滤装饰性内容
        if is_decorative(line):
            i += 1
            continue

        # 3. 独立编号识别：纯数字行（如 03, 04, 05）
        m_num = SECTION_NUMBER_RE.match(line)
        if m_num:
            num = m_num.group(1).zfill(2)
            # 查看下一行是否有内容作为标题
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if next_line and not SECTION_NUMBER_RE.match(next_line) and not is_decorative(next_line):
                # 如果当前在 section 内，先关闭当前 section，用新编号开新 section
                if current_section:
                    flush_section()
                start_section(num, next_line)
                i += 2
                continue
            else:
                # 下一行也是数字或装饰，当前数字作为段落内容
                pass

        # 4. Markdown 标题 ## / ###
        if line.startswith("## "):
            flush_list()
            flush_kv()
            h_text = line[3:].strip()
            # 检查是否是 chapter 标题（如 "一、政策核心内容"）
            if re.match(r'^[一二三四五六七八九十]+[、\s]', h_text):
                flush_section()
                cn = h_text[0]
                h_text = h_text[2:].strip()
                html_parts.append(
                    f'<div class="chapter">\n'
                    f'  <div class="chapter-number">{cn}</div>\n'
                    f'  <div class="chapter-content">\n'
                    f'    <h2>{h_text}</h2>'
                )
            else:
                # 普通 h2，如果不在 section 内，自动开 section
                if not current_section:
                    # 尝试从文本中提取编号
                    m_sec = re.match(r'^(\d+)[.\s、)）\-]+(.+)$', h_text)
                    if m_sec:
                        start_section(m_sec.group(1).zfill(2), m_sec.group(2).strip())
                    else:
                        html_parts.append(f'<h2>{h_text}</h2>')
                else:
                    html_parts.append(f'<h2>{h_text}</h2>')
            i += 1
            continue

        if line.startswith("### "):
            flush_list()
            flush_kv()
            h_text = line[4:].strip()
            html_parts.append(f'<h3>{h_text}</h3>')
            i += 1
            continue

        # 5. 列表项
        if line.startswith("- ") or line.startswith("* "):
            flush_kv()
            if not in_list:
                in_list = True
            item_text = line[2:].strip()
            item_text = inline_md_to_html(item_text)
            list_items.append(f'        <li>{item_text}</li>')
            i += 1
            continue

        # 6. KV 行检测
        m_kv = KV_RE.match(line)
        if m_kv:
            flush_list()
            if not in_kv:
                in_kv = True
            key = m_kv.group("key").strip()
            val = m_kv.group("val").strip()
            # 过滤无意义 KV
            if is_decorative(key) or is_decorative(val) or is_title_duplicate(title, f"{key}{val}"):
                i += 1
                continue
            key_html = inline_md_to_html(key)
            val_html = inline_md_to_html(val)
            kv_rows.append(
                f'      <div class="kv-row">\n'
                f'        <div class="kv-key">{key_html}</div>\n'
                f'        <div class="kv-val">{val_html}</div>\n'
                f'      </div>'
            )
            i += 1
            continue

        # 7. 表格（简化处理：| a | b |）
        if line.startswith("|"):
            flush_list()
            flush_kv()
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().split("|")[1:-1]]
                if cells and not all(set(c) <= set("-|: ") for c in cells):  # 跳过分隔行
                    table_rows.append(cells)
                i += 1
            if table_rows:
                html_parts.append(render_table(table_rows))
            continue

        # 8. 普通段落
        flush_list()
        flush_kv()
        p_text = inline_md_to_html(line)
        if current_section:
            html_parts.append(f'      <p>{p_text}</p>')
        else:
            html_parts.append(f'<p>{p_text}</p>')
        i += 1

    # 收尾
    flush_list()
    flush_kv()
    flush_section()

    return "\n".join(html_parts)


def inline_md_to_html(text: str) -> str:
    """简单的行内 Markdown 转换"""
    # 粗体
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # 高亮 ==text==
    text = re.sub(r'==(.+?)==', r'<mark>\1</mark>', text)
    return text


def render_table(rows: List[List[str]]) -> str:
    """渲染 Markdown 表格为 HTML"""
    if not rows:
        return ""
    html = ['<div class="table-wrap"><table>']
    # 第一行作为表头
    html.append("  <tr>" + "".join(f"<th>{inline_md_to_html(c)}</th>" for c in rows[0]) + "</tr>")
    for row in rows[1:]:
        html.append("  <tr>" + "".join(f"<td>{inline_md_to_html(c)}</td>" for c in row) + "</tr>")
    html.append("</table></div>")
    return "\n".join(html)


def sanitize_id(title: str) -> str:
    """生成 URL 安全的锚点 ID"""
    t = re.sub(r'[^\w\u4e00-\u9fff]+', '-', title)
    t = t.strip('-')
    return f"article-{t[:60]}"


# =============================================================================
# 主流程
# =============================================================================

def process_single_file(md_path: Path) -> Dict[str, str]:
    """处理单个 Markdown 文件，返回渲染所需字段"""
    content = md_path.read_text(encoding="utf-8")
    fm, body = extract_front_matter(content)

    title = fm.get("title", md_path.stem)
    date = fm.get("date", parse_date_from_filename(md_path.name))
    lead = fm.get("excerpt", fm.get("lead", ""))

    # 删除 headline-sub 中的「政策深度解读」等冗余词
    lead = re.sub(r'政策深度解读[：:]?\s*', '', lead).strip()

    body_html = md_to_html_paragraphs(body, title)

    return {
        "article_id": sanitize_id(title),
        "title": title,
        "date": date,
        "lead": lead,
        "body": body_html,
    }


def build_page(articles_data: List[Dict[str, str]]) -> str:
    """组装完整 HTML 页面"""
    # 导航链接
    nav_links = "\n".join(
        f'  <a href="#{a["article_id"]}">{a["title"][:18]}...</a>'
        for a in articles_data
    )

    # 文章区块
    articles_html = "\n".join(
        ARTICLE_TEMPLATE.format(**a)
        for a in articles_data
    )

    return HTML_TEMPLATE.format(
        page_title="OPC政策解析 - 多文章结构适配",
        nav_links=nav_links,
        articles=articles_html,
    )


def main():
    input_dir = Path(INPUT_DIR)
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists():
        print(f"[错误] 输入目录不存在: {input_dir}")
        sys.exit(1)

    md_files = sorted(input_dir.glob("*.md"))
    if not md_files:
        print(f"[警告] 未找到 Markdown 文件: {input_dir}")
        sys.exit(0)

    print(f"[信息] 发现 {len(md_files)} 个 Markdown 文件")

    articles_data = []
    for md_path in md_files:
        print(f"  处理: {md_path.name}")
        try:
            data = process_single_file(md_path)
            articles_data.append(data)
        except Exception as e:
            print(f"  [错误] {md_path.name}: {e}")

    page_html = build_page(articles_data)
    output_file = output_dir / "index.html"
    output_file.write_text(page_html, encoding="utf-8")
    print(f"[完成] 已生成: {output_file}")


if __name__ == "__main__":
    main()
