import os
import re
import glob

# 需要处理的文件夹
folders = ["_insights", "_operations"]

for folder in folders:
    if not os.path.exists(folder):
        print(f"跳过：{folder} 不存在")
        continue
    
    for filepath in glob.glob(os.path.join(folder, "*.md")):
        filename = os.path.basename(filepath)
        
        # 从文件名提取日期：匹配开头 YYYY-MM-DD
        match = re.match(r'^(\d{4}-\d{2}-\d{2})[-_]', filename)
        if not match:
            print(f"⚠️  跳过（文件名无日期）：{filename}")
            continue
        
        date_str = match.group(1)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有 date 字段
        if re.search(r'^date:\s', content, re.MULTILINE):
            print(f"✓ 已有 date：{filename}")
            continue
        
        # 检查是否有 front matter（--- 开头）
        if content.startswith('---'):
            # 在第一个 --- 后面插入 date
            # 找到第一个换行后的位置，插入 date
            lines = content.split('\n')
            # 找到第二个 --- 的位置，或者直接在第一个 --- 后插入
            insert_idx = 1  # 第一行是 ---，从第二行开始
            # 找到合适位置：在 title 后面插入比较规范
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    insert_idx = i
                    break
                if re.match(r'^(title|author|description|summary|source|layout):', line.strip()):
                    insert_idx = i + 1
            
            lines.insert(insert_idx, f"date: {date_str}")
            new_content = '\n'.join(lines)
        else:
            # 没有 front matter，创建一个
            new_content = f"---\ndate: {date_str}\n---\n\n{content}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ 已插入 date({date_str})：{filename}")

print("\n完成。")
