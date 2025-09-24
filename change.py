import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

# --------------------------
# 在这里设置你的参数
# --------------------------
ANNOTATIONS_FOLDER = "trainingdata/1/Annotations"  # 存放XML标注文件的文件夹路径


# --------------------------

def prettify_xml(element):
    """将XML元素格式化，保留缩进和换行"""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def update_xml_extension(xml_path):
    """修改单个XML文件中的文件名扩展名从.bmp到.jpg"""
    try:
        # 解析XML文件
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 查找并修改filename标签
        filename_elem = root.find('filename')
        if filename_elem is not None:
            old_filename = filename_elem.text
            if old_filename and old_filename.lower().endswith('.bmp'):
                # 替换扩展名为.jpg
                new_filename = os.path.splitext(old_filename)[0] + '.jpg'
                filename_elem.text = new_filename
                print(f"已修改: {old_filename} -> {new_filename}")

                # 查找并修改path标签（如果存在）
                path_elem = root.find('path')
                if path_elem is not None:
                    old_path = path_elem.text
                    if old_path:
                        new_path = os.path.splitext(old_path)[0] + '.jpg'
                        path_elem.text = new_path

                # 保存修改后的XML文件
                with open(xml_path, 'w', encoding='utf-8') as f:
                    # 使用prettify_xml保持XML格式美观
                    pretty_xml = prettify_xml(root)
                    # 去除空行
                    lines = [line for line in pretty_xml.split('\n') if line.strip()]
                    f.write('\n'.join(lines))
                return True
        return False

    except Exception as e:
        print(f"处理文件 {xml_path} 时出错: {str(e)}")
        return False


def batch_update_xmls():
    """批量处理文件夹中所有XML文件"""
    # 检查文件夹是否存在
    if not os.path.isdir(ANNOTATIONS_FOLDER):
        print(f"错误: 文件夹 '{ANNOTATIONS_FOLDER}' 不存在，请检查路径是否正确")
        return

    # 获取所有XML文件
    xml_files = [
        f for f in os.listdir(ANNOTATIONS_FOLDER)
        if os.path.isfile(os.path.join(ANNOTATIONS_FOLDER, f)) and
           f.lower().endswith('.xml')
    ]

    if not xml_files:
        print(f"在 '{ANNOTATIONS_FOLDER}' 中未找到XML文件")
        return

    print(f"发现 {len(xml_files)} 个XML文件，开始处理...")

    # 逐个处理XML文件
    updated_count = 0
    skipped_count = 0

    for xml_file in xml_files:
        xml_path = os.path.join(ANNOTATIONS_FOLDER, xml_file)
        if update_xml_extension(xml_path):
            updated_count += 1
        else:
            skipped_count += 1

    print(f"\n处理完成！已更新: {updated_count} 个, 未修改: {skipped_count} 个")


if __name__ == "__main__":
    batch_update_xmls()
