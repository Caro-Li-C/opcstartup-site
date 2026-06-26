import os, re, glob
POLICY_DIR = "opc-content-source/policy"
DRY_RUN = True
CHAPTER_PATTERNS = [
    r'^第[一二三四五六七八九十百千]+[章节]\s+.*',
    r'^附件[一二三四五六七八九十]\s+.*',
    r'^附录[一二三四五六七八九十ABCDEF]\s*.*',
]

def clean_file(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        original = f.read()
    changed = False; actions = []
    fm_match = re.match(r'^(---\s*\n.*?\n---\s*\n)', original, re.DOTALL)
    if not fm_match: return None, []
    front_matter = fm_match.group(1); body = original[fm_match.end():]
    title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', front_matter, re.MULTILINE)
    if title_match:
        yaml_title = title_match.group(1).strip()
        lines = body.split('\n')
        first_idx = next((i for i, l in enumerate(lines) if l.strip()), None)
        if first_idx is not None and lines[first_idx].strip() == yaml_title:
            removed = lines.pop(first_idx); actions.append(f"删标题: {removed[:60]}")
            while first_idx < len(lines) and not lines[first_idx].strip(): lines.pop(first_idx)
            body = '\n'.join(lines); changed = True
    lines = body.split('\n'); delete_from = None
    for i in range(len(lines)-1, -1, -1):
        line = lines[i].strip()
        if not line: continue
        for p in CHAPTER_PATTERNS:
            if re.match(p, line): delete_from = i; break
        if delete_from is not None: break
    if delete_from is not None:
        removed = lines[delete_from:]; lines = lines[:delete_from]
        while lines and not lines[-1].strip(): lines.pop()
        body = '\n'.join(lines); changed = True; actions.append(f"删底部({len(removed)}行): {removed[0][:60]}")
    if not changed: return None, []
    return front_matter + body + '\n', actions

md_files = sorted(glob.glob(os.path.join(POLICY_DIR, "*.md")))
print(f"扫描到 {len(md_files)} 个文件\n")
changed = 0
for fp in md_files:
    new_content, actions = clean_file(fp)
    fname = os.path.basename(fp)
    if new_content:
        changed += 1
        print(f"\n[✓ 修改] {fname}")
        for a in actions: print(f"  → {a}")
        old_lines = open(fp, 'r', encoding='utf-8').read().splitlines()
        new_lines = new_content.splitlines()
        print(f"  原末尾: {old_lines[-2:]}")
        print(f"  新末尾: {new_lines[-2:]}")
    else:
        print(f"[○ 跳过] {fname}")
print(f"\n【预览模式】将修改 {changed} 个文件，其余未改动")
