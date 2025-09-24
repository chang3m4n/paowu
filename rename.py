import os
import argparse
import xml.etree.ElementTree as ET


def modify_annotation_name(input_dir, output_dir, old_name=None, new_name=None, set_all=None):
    """
    修改Pascal VOC格式标注文件中的name字段

    参数:
    input_dir (str): 输入标注文件目录
    output_dir (str): 输出标注文件目录
    old_name (str, optional): 需要替换的旧标签名
    new_name (str, optional): 替换后的新标签名
    set_all (str, optional): 将所有name字段设置为该值，忽略old_name和new_name
    """
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有XML文件
    xml_files = [f for f in os.listdir(input_dir) if f.endswith('.xml')]

    for xml_file in xml_files:
        xml_path = os.path.join(input_dir, xml_file)
        output_path = os.path.join(output_dir, xml_file)

        try:
            # 解析XML文件
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # 遍历所有object标签
            for obj in root.findall('object'):
                name_elem = obj.find('name')
                if name_elem is not None:
                    if set_all is not None:
                        # 直接设置所有name字段为指定值
                        name_elem.text = set_all
                    elif old_name is not None and new_name is not None:
                        # 只替换特定的旧标签名
                        if name_elem.text == old_name:
                            name_elem.text = new_name

            # 保存修改后的XML文件
            tree.write(output_path, encoding='utf-8', xml_declaration=True)
            print(f"已修改: {xml_file}")

        except Exception as e:
            print(f"处理文件 {xml_file} 时出错: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='修改Pascal VOC标注文件中的name字段')
    parser.add_argument('--input_dir', required=True, help='输入标注文件目录')
    parser.add_argument('--output_dir', required=True, help='输出标注文件目录')
    parser.add_argument('--old_name', help='需要替换的旧标签名')
    parser.add_argument('--new_name', help='替换后的新标签名')
    parser.add_argument('--set_all', help='将所有name字段设置为该值，忽略old_name和new_name')

    args = parser.parse_args()

    # 验证参数
    if args.set_all is None:
        if args.old_name is None or args.new_name is None:
            parser.error("当不使用--set_all时，必须同时提供--old_name和--new_name")

    modify_annotation_name(
        args.input_dir,
        args.output_dir,
        args.old_name,
        args.new_name,
        args.set_all
    )