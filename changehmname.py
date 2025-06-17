import os
import re

def format_title_to_filename(title):
    title = title.lstrip('#').strip()
    title = title.replace(' ', '-')
    title = re.sub(r'[\\/:*?"<>|]', '', title)  # 移除非法字符
    return title

def get_first_non_empty_line(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                return line
    return "untitled"

def extract_numeric_prefix(filename):
    match = re.match(r'^(\d+)', filename)
    return int(match.group(1)) if match else None

def contains_letters(filename):
    """
    判断文件名中（不含扩展名）是否包含任何英文字母
    """
    name_only = os.path.splitext(os.path.basename(filename))[0]
    return bool(re.search(r'[a-zA-Z]', name_only))

def main():
    all_md_files = [f for f in os.listdir('.') if f.endswith('.md') and re.match(r'^\d+', f)]

    # 获取含英文字母的文件中的最大数字前缀
    max_existing_number = 0
    for f in all_md_files:
        if contains_letters(f):
            num = extract_numeric_prefix(f)
            if num is not None:
                max_existing_number = max(max_existing_number, num)

    print(f"max_existing_number:{max_existing_number}")

    # 过滤不含字母的目标文件，准备重命名
    target_files = [f for f in all_md_files if not contains_letters(f)]
    target_files.sort(key=extract_numeric_prefix)

    next_number = max_existing_number + 1

    print(f"target_files:{target_files}")

    for filename in target_files:
        title = get_first_non_empty_line(filename)
        formatted_title = format_title_to_filename(title)
        new_filename = f"{next_number:02d}-{formatted_title}.md"

        # 防止重名冲突
        counter = 1
        original_new_filename = new_filename
        while os.path.exists(new_filename):
            new_filename = f"{original_new_filename.rsplit('.md', 1)[0]}_{counter}.md"
            counter += 1

        os.rename(filename, new_filename)
        print(f"Renamed: {filename} -> {new_filename}")
        next_number += 1

if __name__ == '__main__':
    main()
