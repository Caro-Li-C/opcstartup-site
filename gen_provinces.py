import yaml
import os

with open("_data/policies.yml", "r", encoding="utf-8") as f:
    policies = yaml.safe_load(f)

provinces = {}
for p in policies:
    prov = p["province"]
    if prov not in provinces:
        provinces[prov] = {"region": p["region"], "cities": {}}
    city = p["city"]
    if city not in provinces[prov]["cities"]:
        provinces[prov]["cities"][city] = []
    provinces[prov]["cities"][city].append(p)

template = """---
layout: default
title: "{province} · OPC政策汇编"
---

<style>
  .policy-page {{ max-width: 900px; margin: 0 auto; padding: 60px 48px; }}
  .policy-page h1 {{ font-family: 'Noto Serif SC', serif; font-size: 32px; margin-bottom: 8px; }}
  .policy-page .region-tag {{ color: #8a8279; font-size: 14px; margin-bottom: 48px; display: block; }}
  .city-group {{ margin-bottom: 48px; }}
  .city-group h2 {{ font-size: 20px; font-weight: 700; color: #1a1a1a; padding-bottom: 12px; border-bottom: 2px solid #b8956a; margin-bottom: 20px; }}
  .policy-item {{ padding: 20px 0; border-bottom: 1px solid #e8e4df; }}
  .policy-item:last-child {{ border-bottom: none; }}
  .policy-item h3 {{ font-size: 17px; font-weight: 600; color: #1a1a1a; margin-bottom: 8px; line-height: 1.5; }}
  .policy-item h3 a {{ color: inherit; text-decoration: none; }}
  .policy-item h3 a:hover {{ color: #8a6d4b; }}
  .policy-meta {{ font-size: 13px; color: #8a8279; }}
  .policy-meta span {{ margin-right: 12px; }}
  .policy-tag {{ background: #f5f3f0; padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
</style>

<div class="policy-page">
  <h1>{province}OPC政策</h1>
  <span class="region-tag">{region} · 共 {count} 项</span>

{cities_html}
</div>
"""

os.makedirs("policy", exist_ok=True)

for province, data in provinces.items():
    cities_html = ""
    for city, items in data["cities"].items():
        cities_html += f'  <div class="city-group">\n    <h2>{city}</h2>\n'
        for item in items:
            cities_html += f"""    <article class="policy-item">
      <h3><a href="{item['original_url']}" target="_blank">{item['title']}</a></h3>
      <div class="policy-meta">
        <span>{item['date']}</span>
        <span class="policy-tag">{item['category']}</span>
        <span>编号 {item['id']}</span>
      </div>
    </article>
"""
        cities_html += "  </div>\n"

    content = template.format(
        province=province,
        region=data["region"],
        count=sum(len(v) for v in data["cities"].values()),
        cities_html=cities_html,
    )

    with open(f"policy/{province}.html", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ {province}.html（{data['region']} · {len(data['cities'])} 个城市）")

print(f"\n🎉 完成：共 {len(provinces)} 个省份/直辖市")
