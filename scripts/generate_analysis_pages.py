#!/usr/bin/env python3
"""
generate_analysis_pages.py - 政策解析页面生成脚本
v3.2: 针对清洗后MD优化：严格去重、合并短行、严格KV、跳过表格残留
"""
import os
import re
import yaml
from pathlib import Path
from datetime import datetime

SOURCE_DIR = Path("_tmp_source/analysis")
OUTPUT_DIR = Path("policy/analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DECORATIVE_WORDS = {
    "cold", "take", "labo", "policy depth interpretation", "policy interpretation",
    "政策深度解读", "深度解读", "政策解读"
}
CN_MAP = {'壹':'一','贰':'二','叁':'三','肆':'四','伍':'五','陆':'六','柒':'七','捌':'八','玖':'九','拾':'十'}
FW_MAP = {'𝟎':'0','𝟏':'1','𝟐':'2','𝟑':'3','𝟒':'4','𝟓':'5','𝟔':'6','𝟕':'7','𝟖':'8','𝟗':'9'}

def fw_to_cn(text):
    s = ''.join(FW_MAP.get(c, c) for c in text)
    num_map = {'01':'一','02':'二','03':'三','04':'四','05':'五','06':'六','07':'七','08':'八','09':'九','10':'十','11':'十一','12':'十二','1':'一','2':'二','3':'三','4':'四','5':'五','6':'六','7':'七','8':'八','9':'九'}
    return num_map.get(s, s)

def slugify(title):
    return re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "-").replace("_", "-")[:50]

def jaccard_similarity(a, b):
    set_a, set_b = set(a), set(b)
    if not set_a and not set_b: return 1.0
    return len(set_a & set_b) / len(set_a | set_b) if (set_a | set_b) else 0.0

def is_decorative(text):
    t = text.strip()
    if not t: return True
    if len(t) <= 2 and not any(c.isalnum() for c in t): return True
    if t.lower() in DECORATIVE_WORDS: return True
    if re.match(r'^[A-Za-z]+$', t) and len(t) <= 6: return True
    return False

def is_image_placeholder(line):
    s = line.strip()
    if not s: return False
    if s == '图片': return True
    if re.match(r'^.*\.(jpg|jpeg|png|gif|webp|svg)$', s, re.I): return True
    if len(s) <= 12:
        img_kws = ['航拍','全景','效果图','示意图','配图','封面','插图','摄影','实景','夜景']
        if any(k in s for k in img_kws): return True
    return False

def is_table_line(line):
    s = line.strip()
    return s.startswith('|') and s.endswith('|') and '|' in s[1:-1]

def is_table_divider(line):
    return re.match(r'^\s*\|?[\s\-:]+\|', line.strip())

def is_intro_block(line):
    s = line.strip()
    return any(re.match(p, s) for p in [
        r'^【导语】', r'^导读[：:]', r'^导语[：:]', r'^📖\s*导语',
        r'^📅\s*\d{4}', r'^📄\s*文件', r'^京经信发〔\d{4}〕\d+号',
        r'^发布时间[：:]', r'^发布主体[：:]', r'^政策名称[：:]',
        r'^状态[：:]', r'^征求意见[：:]', r'^有效期[：:]', r'^文件全称[：:]',
        r'^\d{4}年\d{1,2}月\d{1,2}日\s*·\s*政策解读',
    ])

def inline_md_to_html(text):
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text.strip()


def parse_markdown_body(body, title, description=""):
    lines = body.strip().split('\n')

    # 严格去重：检查前3行累积文本与 title+description 的相似度
    check_text = (title + " " + description).strip()
    if check_text:
        for cut in [3, 2, 1]:
            if len(lines) >= cut:
                leading = " ".join([l.strip() for l in lines[:cut] if l.strip()])
                if leading and (leading in check_text or check_text in leading or jaccard_similarity(leading, check_text) > 0.55):
                    lines = lines[cut:]
                    break

    # 预处理：合并连续短行（时间线、碎片）
    merged = []
    buffer = []
    for line in lines:
        s = line.strip()
        if not s:
            if buffer:
                merged.append(" ".join(buffer))
                buffer = []
            merged.append("")
            continue
        # 标题、列表、KV、引用、粗体不合并
        if (s.startswith("#") or re.match(r'^[-•]\s', s) or re.match(r'^\d+\.\s', s) or 
            re.match(r'^[^，。；！？、:：\t]{1,12}[：:\t]+', s) or s.startswith(">") or 
            (s.startswith("**") and s.endswith("**"))):
            if buffer:
                merged.append(" ".join(buffer))
                buffer = []
            merged.append(s)
        elif len(s) <= 20 and not re.search(r'[。；！？]', s):
            buffer.append(s)
        else:
            if buffer:
                merged.append(" ".join(buffer))
                buffer = []
            merged.append(s)
    if buffer:
        merged.append(" ".join(buffer))
    lines = [l for l in merged if l is not None]

    html_parts = []
    chapter_idx = 0
    in_chapter = False
    chapter_buffer = []
    in_numbered = False
    numbered_buffer = []
    numbered_num = ""
    in_list = False
    list_items = []
    list_type = "ul"
    first_para = True
    i = 0

    # KV key 黑名单：这些词出现在key位置说明是正文，不是真正的key
    KV_KEY_BLACKLIST = {"口径", "旧版", "保障型", "三年", "阶梯式", "模型券", "算力券", 
                        "年度", "上限", "合计", "如理", "补贴", "人才", "公寓", "住房",
                        "发布", "时间", "主体", "名称", "状态", "有效期", "文件", "全称"}

    def flush_list():
        nonlocal in_list, list_items, list_type
        if in_list and list_items:
            tag = "ul" if list_type == "ul" else "ol"
            items_html = "\n".join([f'        <li>{inline_md_to_html(item)}</li>' for item in list_items])
            html = f'<{tag} class="article-list">\n{items_html}\n</{tag}>'
            if in_numbered: numbered_buffer.append(("list", html))
            elif in_chapter: chapter_buffer.append(("list", html))
            else: html_parts.append(html)
            list_items = []
            in_list = False

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

    def is_strict_kv(line):
        """严格KV判断：key<=12字，无标点，不是正文词，val明显更长"""
        m = re.match(r'^([^，。；！？、:：\t]{1,12})[：:\t]+(.+)$', line)
        if not m: return False
        key = m.group(1).strip()
        val = m.group(2).strip()
        if len(val) <= len(key): return False
        if any(bw in key for bw in KV_KEY_BLACKLIST): return False
        # key 应该是属性名（较短、较抽象），不是叙述句
        if re.search(r'[是为在将了对从由向按]', key) and len(key) > 6: return False
        return True

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            flush_list(); flush_chapter(); flush_numbered()
            i += 1; continue

        if is_image_placeholder(s) or is_decorative(s) or is_intro_block(s):
            i += 1; continue

        # 跳过表格残留
        if is_table_line(s) or is_table_divider(s):
            i += 1; continue

        # 列表项
        ul_m = re.match(r'^[-•]\s+(.+)$', s)
        ol_m = re.match(r'^(\d+)\.\s+(.+)$', s)
        if ul_m or ol_m:
            flush_chapter(); flush_numbered()
            new_type = "ul" if ul_m else "ol"
            if in_list and list_type != new_type:
                flush_list(); in_list = True; list_type = new_type
            elif not in_list:
                in_list = True; list_type = new_type
            item_text = ul_m.group(1) if ul_m else ol_m.group(2)
            list_items.append(item_text)
            i += 1; continue

        # 结语
        if re.match(r'^#{1,2}\s*结语', s) or re.match(r'^#{1,2}\s*Conclusion', s, re.I):
            flush_list(); flush_chapter(); flush_numbered()
            conclusion_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("#"):
                if lines[i].strip() and not is_decorative(lines[i].strip()):
                    conclusion_lines.append(lines[i].strip())
                i += 1
            html_parts.append(render_conclusion(conclusion_lines))
            continue

        # h2
        h2_m = re.match(r'^#{2}\s+(.+)$', s)
        if h2_m:
            h2_text = h2_m.group(1).strip()
            cn_m = re.match(r'^(?:([一二三四五六七八九十]+)、|第([一二三四五六七八九十\d]+)条)\s*(.+)$', h2_text)
            if cn_m:
                flush_list(); flush_numbered(); flush_chapter()
                in_chapter = True
                chapter_buffer.append(("h2", cn_m.group(3) if cn_m.group(3) else h2_text))
                i += 1; continue
            num_m = re.match(r'^(\d{1,2})[\.、\s)）]+\s*(.+)$', h2_text)
            if num_m:
                flush_list(); flush_chapter(); flush_numbered()
                in_numbered = True
                numbered_num = num_m.group(1).zfill(2)
                numbered_buffer.append(("title", num_m.group(2).strip()))
                i += 1; continue
            flush_list(); flush_numbered(); flush_chapter()
            in_chapter = True
            chapter_buffer.append(("h2", h2_text))
            i += 1; continue

        # h3
        h3_m = re.match(r'^#{3}\s+(.+)$', s)
        if h3_m:
            flush_list()
            h3_text = h3_m.group(1).strip()
            if in_numbered: numbered_buffer.append(("h3", h3_text))
            elif in_chapter: chapter_buffer.append(("h3", h3_text))
            else: html_parts.append(f"<h3>{inline_md_to_html(h3_text)}</h3>")
            i += 1; continue

        # 无#前缀中文编号
        cn_chapter = re.match(r'^(?:[一二三四五六七八九十]+、|第[一二三四五六七八九十\d]+条)\s*(.+)$', s)
        if cn_chapter and len(s) < 60:
            flush_list(); flush_numbered(); flush_chapter()
            in_chapter = True
            chapter_buffer.append(("h2", cn_chapter.group(1)))
            i += 1; continue

        # 独立数字+下一行
        m_num = re.match(r'^(\d{1,2})$', s)
        if m_num:
            next_s = lines[i+1].strip() if i+1 < len(lines) else ""
            if next_s and len(next_s) < 40 and not next_s.startswith("#") and not re.match(r'^\d{1,2}$', next_s):
                flush_list(); flush_chapter(); flush_numbered()
                in_numbered = True
                numbered_num = m_num.group(1).zfill(2)
                numbered_buffer.append(("title", next_s))
                i += 2; continue

        # 严格KV
        if is_strict_kv(s):
            m = re.match(r'^([^，。；！？、:：\t]{1,12})[：:\t]+(.+)$', s)
            key = m.group(1).strip()
            val = m.group(2).strip()
            flush_list()
            if in_numbered: numbered_buffer.append(("kv", (key, val)))
            elif in_chapter: chapter_buffer.append(("kv", (key, val)))
            else: html_parts.append(render_kv_row(key, val))
            i += 1; continue

        # 引用
        if s.startswith(">"):
            flush_list()
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q = lines[i].strip()[1:].strip()
                if q and not is_decorative(q): quote_lines.append(q)
                i += 1
            if quote_lines:
                text = " ".join(quote_lines)
                if in_numbered: numbered_buffer.append(("quote", text))
                elif in_chapter: chapter_buffer.append(("quote", text))
                else: html_parts.append(render_highlight(text))
            continue

        # 整行粗体
        if s.startswith("**") and s.endswith("**"):
            flush_list()
            text = s[2:-2]
            if in_numbered: numbered_buffer.append(("strong_p", text))
            elif in_chapter: chapter_buffer.append(("strong_p", text))
            else: html_parts.append(f"<p><strong>{inline_md_to_html(text)}</strong></p>")
            i += 1; continue

        # 普通段落
        flush_list()
        p_text = inline_md_to_html(s)
        if in_numbered: numbered_buffer.append(("p", p_text))
        elif in_chapter: chapter_buffer.append(("p", p_text))
        else:
            if first_para and 50 <= len(s) <= 200:
                html_parts.append(f'<div class="drop-cap-section"><p>{p_text}</p></div>')
            else:
                html_parts.append(f"<p>{p_text}</p>")
            first_para = False
        i += 1

    flush_list(); flush_chapter(); flush_numbered()
    return "\n".join(html_parts)


def render_chapter(idx, items):
    h2_title = h3_sub = ""
    body_parts = []
    kv_rows = []
    for typ, content in items:
        if typ == "h2": h2_title = content
        elif typ == "h3": h3_sub = content
        elif typ == "quote": body_parts.append(render_highlight(content))
        elif typ == "strong_p": body_parts.append(f"<p><strong>{inline_md_to_html(content)}</strong></p>")
        elif typ == "kv": k, v = content; kv_rows.append(render_kv_row(k, v))
        elif typ == "list": body_parts.append(content)
        elif typ == "p": body_parts.append(f"<p>{inline_md_to_html(content)}</p>")
    sub_html = f'<div class="chapter-sub">{inline_md_to_html(h3_sub)}</div>' if h3_sub else ""
    kv_html = ('<div class="kv-grid">\n' + "\n".join(kv_rows) + '\n</div>') if kv_rows else ""
    body_html = "\n".join(body_parts)
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
        if typ == "title": title = content
        elif typ == "h3": body_parts.append(f"<h3>{inline_md_to_html(content)}</h3>")
        elif typ == "quote": body_parts.append(render_highlight(content))
        elif typ == "strong_p": body_parts.append(f"<p><strong>{inline_md_to_html(content)}</strong></p>")
        elif typ == "kv": k, v = content; kv_rows.append(render_kv_row(k, v))
        elif typ == "list": body_parts.append(content)
        elif typ == "p": body_parts.append(f"<p>{inline_md_to_html(content)}</p>")
    kv_html = ('<div class="kv-grid">\n' + "\n".join(kv_rows) + '\n</div>') if kv_rows else ""
    body_html = "\n".join(body_parts)
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
        <div class="kv-key">{inline_md_to_html(key)}</div>
        <div class="kv-val">{inline_md_to_html(val)}</div>
      </div>"""


def render_highlight(text):
    text = re.sub(r"^\*\*(.+?)：\*\*", r"<strong>\1：</strong>", text)
    text = re.sub(r"^\*\*(.+?):\*\*", r"<strong>\1：</strong>", text)
    text = inline_md_to_html(text)
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
            paragraphs.append(f"<p>{inline_md_to_html(line)}</p>")
    closing_html = f'\n    <div class="closing-line">{inline_md_to_html(closing_line)}</div>' if closing_line else ""
    return f"""  <div class="conclusion">
    <h2>结语</h2>
"\n".join(["    " + p for p in paragraphs]){closing_html}
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
.chapter { margin-bottom: 48px; display: flex; gap: 24px; align-items: flex-start; }
.chapter-number { flex-shrink: 0; width: 48px; height: 48px; background: var(--ink); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--brass-light); font-family: "Noto Serif SC", serif; font-size: 18px; font-weight: 700; margin-top: 4px; }
.chapter-content { flex: 1; }
.chapter-content h2 { font-family: "Noto Serif SC", serif; font-size: 22px; font-weight: 700; color: var(--ink); margin-bottom: 4px; line-height: 1.4; }
.chapter-content .chapter-sub { font-size: 14px; color: var(--warm-gray); margin-bottom: 16px; font-style: italic; }
.chapter-content p { font-size: 16px; line-height: 2; color: var(--charcoal); margin-bottom: 16px; text-align: justify; }
.chapter-content p:last-child { margin-bottom: 0; }
.numbered-section { margin: 24px 0; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; margin-left: -60px; padding: 24px; padding-left: 0; }
.section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--mist); padding-left: 52px; }
.section-num { font-family: "Noto Serif SC", serif; font-size: 28px; font-weight: 700; color: var(--brass); width: 40px; min-width: 40px; max-width: 40px; text-align: center; flex-shrink: 0; line-height: 1; padding: 0; margin-left: -52px; }
.section-title { font-family: "Noto Serif SC", serif; font-size: 18px; font-weight: 600; color: var(--ink); flex: 1; }
.section-body { padding-left: 52px; }
.section-body p { font-size: 15px; line-height: 1.9; color: var(--charcoal); margin-bottom: 10px; }
.section-body p:last-child { margin-bottom: 0; }
.kv-grid { margin: 20px 0; display: flex; flex-direction: column; gap: 2px; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; overflow: hidden; }
.kv-row { display: flex; align-items: flex-start; gap: 16px; padding: 14px 20px; border-bottom: 1px solid var(--mist); }
.kv-row:last-child { border-bottom: none; }
.kv-row:hover { background: var(--bg-warm); }
.kv-key { font-size: 13px; font-weight: 600; color: var(--warm-gray); min-width: 80px; max-width: 120px; flex-shrink: 0; letter-spacing: 0.5px; padding-top: 2px; }
.kv-val { font-size: 15px; color: var(--charcoal); line-height: 1.7; flex: 1; }
.article-list { margin: 14px 0 14px 20px; padding: 0; font-size: 15px; line-height: 1.9; color: var(--charcoal); }
.article-list li { margin-bottom: 6px; }
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
@media (max-width: 640px) { .headline-area h1 { font-size: 28px; } .chapter { gap: 16px; } .chapter-number { width: 36px; height: 36px; font-size: 14px; } .chapter-content h2 { font-size: 18px; } .drop-cap-section p::first-letter { font-size: 56px; } .numbered-section { margin-left: -46px; padding: 16px; padding-left: 0; } .section-header { padding-left: 44px; } .section-num { font-size: 22px; width: 32px; min-width: 32px; max-width: 32px; margin-left: -44px; } .section-title { font-size: 16px; } .section-body { padding-left: 44px; } .kv-row { flex-direction: column; gap: 4px; padding: 12px 16px; } .kv-key { min-width: auto; } }
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

    display_tags = []
    for t in tags:
        if t not in display_tags and t != "政策解析":
            display_tags.append(t)
    if not display_tags:
        display_tags = ["OPC"]

    if description and len(description) <= 30 and description != "政策深度解读":
        sub_title = description
        lead_text = ""
    else:
        sub_title = ""
        lead_text = description if description and description != "政策深度解读" else ""

    body_html = parse_markdown_body(body, title, description)

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
