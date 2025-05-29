import os
import re

# 清理标题 -> 合法文件名
def format_title_to_filename(title):
    # 去除前导的#和空格，然后将中间空格换成-
    title = title.lstrip('#').strip()
    title = title.replace(' ', '-')

    # 去除Windows非法字符: \ / : * ? " < > |
    title = re.sub(r'[\\/:*?"<>|]', '', title)

    return title

# 获取第一行非空文本
def get_first_non_empty_line(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                return line
    return "untitled"

def main():
    for filename in os.listdir('.'):
        if filename.endswith('.md') and re.match(r'^\d+', filename):
            first_line = get_first_non_empty_line(filename)
            new_name_part = format_title_to_filename(first_line)

            # 如果想保留原编号前缀，比如“01-”，可以这样提取
            prefix = re.match(r'^(\d+)', filename).group(1)
            new_filename = f"{prefix}-{new_name_part}.md"

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
