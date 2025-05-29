import os
import re

# 清理标题为合法文件名
def format_title_to_filename(title):
    title = title.lstrip('#').strip()
    title = title.replace(' ', '-')
    # 去除Windows非法字符
    title = re.sub(r'[\\/:*?"<>|]', '', title)
    return title

# 获取第一行非空内容
def get_first_non_empty_line(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                return line
    return "untitled"

def main():
    # 1. 获取所有以数字开头的 .md 文件
    md_files = [f for f in os.listdir('.') if f.endswith('.md') and re.match(r'^\d+', f)]
    
    # 2. 按文件名中的数字前缀排序（如01、10、2排序为 1,2,10）
    def extract_number_prefix(fname):
        match = re.match(r'^(\d+)', fname)
        return int(match.group(1)) if match else float('inf')
    
    md_files.sort(key=extract_number_prefix)

    # 3. 遍历重命名
    for idx, filename in enumerate(md_files, start=1):
        first_line = get_first_non_empty_line(filename)
        name_part = format_title_to_filename(first_line)

        new_filename = f"{idx:02d}-{name_part}.md"

        # 防止重名
        if new_filename == filename:
            continue
        counter = 1
        original_new_filename = new_filename
        while os.path.exists(new_filename):
            new_filename = f"{original_new_filename.rsplit('.md', 1)[0]}_{counter}.md"
            counter += 1

        os.rename(filename, new_filename)
        print(f"Renamed: {filename} -> {new_filename}")

if __name__ == '__main__':
    main()
