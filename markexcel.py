import os
import re
from openpyxl import Workbook

# GitHub 链接前缀
GITHUB_PREFIX = "https://github.com/same4869/HarmonyNext-/blob/main/"

def is_target_md_file(filename):
    return (
        filename.endswith(".md") and
        re.match(r'^\d+', filename) and
        re.search(r'[a-zA-Z]', filename)
    )

def extract_title_without_prefix(filename):
    # 去掉前缀数字和连字符，例如 124-HarmonyOS-Next... -> HarmonyOS-Next...
    return re.sub(r'^\d+-', '', filename).rsplit('.md', 1)[0]

def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Markdown Files"
    ws.append(["Title", "GitHub Link"])  # 表头

    for filename in os.listdir('.'):
        if is_target_md_file(filename):
            title = extract_title_without_prefix(filename)
            link = GITHUB_PREFIX + filename
            ws.append([title, link])
            print(f"Added: {title}")

    output_file = "md_links.xlsx"
    wb.save(output_file)
    print(f"\n✅ Excel 文件已保存为: {output_file}")

if __name__ == '__main__':
    main()
