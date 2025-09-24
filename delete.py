import os


def filter_lines_by_last_char(input_file, output_file, delete_char='g'):
    """
    过滤文本文件中的行，删除行末字符为指定字符的行

    参数:
    input_file (str): 输入文件路径
    output_file (str): 输出文件路径
    delete_char (str): 需要删除的行末字符，默认为 'g'
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    filtered_lines = []
    for line in lines:
        stripped_line = line.rstrip('\r\n')  # 移除行末换行符
        if not stripped_line or stripped_line[-1] != delete_char:
            filtered_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(filtered_lines)

    print(f"处理完成！从 {input_file} 中删除了 {len(lines) - len(filtered_lines)} 行，输出到 {output_file}")


if __name__ == "__main__":
    input_path = "train.txt"  # 替换为实际输入文件路径
    output_path = "train.txt"  # 替换为实际输出文件路径

    # 检查输入文件是否存在
    if not os.path.exists(input_path):
        print(f"错误：输入文件 '{input_path}' 不存在！")
    else:
        filter_lines_by_last_char(input_path, output_path)