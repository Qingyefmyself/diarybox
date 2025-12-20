import os
import json
from pathlib import Path

md_dir = Path("./writings")
output_file = Path("./philosophy.json")

def parse_md(file_path):
    with open(file_path, encoding="utf-8") as f:
        lines = [line.rstrip() for line in f if line.strip() != ""]

    title = ""
    date = ""
    content_lines = []

    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("@date:"):
            date = line[6:].strip()
        else:
            content_lines.append(line)

    if not date:
        name = file_path.stem
        if len(name) >= 10 and name[:10].count("-") == 2:
            date = name[:10]

    content = "\n".join(content_lines).strip()
    return {"title": title, "date": date, "content": content}

md_files = [md_dir / f for f in os.listdir(md_dir) if f.endswith(".md")]
entries = [parse_md(f) for f in md_files]
entries.sort(key=lambda x: x["date"], reverse=True)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print(f"✓ {output_file} 已生成，{len(entries)} 条内容")
