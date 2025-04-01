import os
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def generate_summary(directory, base_path="", ignore_dirs=[], level=0, use_natural_sort=False, exclude_files=[]):
    summary_lines = []
    items = [item for item in os.listdir(directory) if item not in ignore_dirs]
    
    # 排除需要忽略的文件和SUMMARY.md
    items = [item for item in items if item != "SUMMARY.md" and item not in exclude_files]
    
    # 顶层处理时移除README.md，后面单独处理
    if level == 0:
        items = [item for item in items if item != "README.md"]
    
    # 排序处理
    if use_natural_sort:
        items.sort(key=natural_sort_key)
    else:
        items.sort(key=lambda x: x.lower())
    
    indent = '    ' * level

    for item in items:
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            # 检查目录下是否存在README.md
            readme_path = os.path.join(path, "README.md")
            readme_exists = os.path.isfile(readme_path)
            
            # 生成目录链接
            if readme_exists:
                link = os.path.join(base_path, item, "README.md").replace('\\', '/')
            else:
                link = ""
            summary_lines.append(f"{indent}- [{item}]({link})")
            
            # 递归处理子目录，排除README.md如果存在
            new_base = os.path.join(base_path, item)
            sub_exclude = ["README.md"] if readme_exists else []
            sub_summary = generate_summary(
                path, new_base, ignore_dirs, level + 1, use_natural_sort, sub_exclude
            )
            if sub_summary.strip():  # 避免空行
                summary_lines.append(sub_summary)
        elif item.endswith(".md"):
            # 处理普通md文件
            link = os.path.join(base_path, item).replace('\\', '/')
            name = os.path.splitext(item)[0]
            summary_lines.append(f"{indent}- [{name}]({link})")
    
    # 在顶层添加top page条目
    if level == 0:
        top_readme = os.path.join(directory, "README.md")
        if os.path.exists(top_readme):
            summary_lines.insert(0, "- [top page](README.md)")
    
    return '\n'.join(summary_lines)

def create_summary_file(src_directory, output_file="SUMMARY.md", ignore_dirs=[], use_natural_sort=False):
    summary_content = generate_summary(src_directory, "", ignore_dirs, 0, use_natural_sort)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary_content)
    print(f"SUMMARY.md has been created at {output_file}")

# 配置参数
src_directory = "../src/"
ignore_dirs = ["ignore_this_folder", "figs", "examples"]
create_summary_file(src_directory, ignore_dirs=ignore_dirs, use_natural_sort=True)
