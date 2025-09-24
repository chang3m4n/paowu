import os
from PIL import Image

# --------------------------
# 在这里设置你的参数
# --------------------------
FOLDER_PATH = "trainingdata/11/JPEGImages"  # 替换为你的BMP文件所在文件夹路径
JPG_QUALITY = 90  # JPG图像质量(1-100)


# --------------------------

def convert_bmp_to_jpg():
    """批量将指定文件夹中的BMP文件转换为JPG文件，并删除原始BMP文件"""
    # 检查文件夹是否存在
    if not os.path.isdir(FOLDER_PATH):
        print(f"错误: 文件夹 '{FOLDER_PATH}' 不存在，请检查路径是否正确")
        return

    # 获取所有BMP文件
    bmp_files = [
        f for f in os.listdir(FOLDER_PATH)
        if os.path.isfile(os.path.join(FOLDER_PATH, f)) and
           f.lower().endswith('.bmp')
    ]

    if not bmp_files:
        print(f"在 '{FOLDER_PATH}' 中未找到BMP文件")
        return

    print(f"发现 {len(bmp_files)} 个BMP文件，开始转换并会自动删除原始文件...")

    # 逐个转换文件
    success_count = 0
    fail_count = 0

    for bmp_file in bmp_files:
        bmp_path = os.path.join(FOLDER_PATH, bmp_file)
        # 构建JPG文件名
        jpg_file = os.path.splitext(bmp_file)[0] + '.jpg'
        jpg_path = os.path.join(FOLDER_PATH, jpg_file)

        try:
            # 打开BMP文件并转换为JPG
            with Image.open(bmp_path) as img:
                # 处理带有alpha通道的图像
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
                    background.paste(img, img.split()[-1])
                    img = background

                img.save(jpg_path, 'JPEG', quality=JPG_QUALITY)

            # 转换成功后删除原BMP文件
            os.remove(bmp_path)
            print(f"已转换并删除原始文件: {bmp_file} -> {jpg_file}")
            success_count += 1

        except Exception as e:
            print(f"转换失败，未删除原始文件: {bmp_file}，错误: {str(e)}")
            fail_count += 1

    print(f"\n转换完成！成功转换并删除: {success_count} 个, 转换失败: {fail_count} 个")


if __name__ == "__main__":
    convert_bmp_to_jpg()
