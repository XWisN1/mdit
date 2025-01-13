from mdit_utils.logic import logic
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='移动图片到指定文件夹并更新markdown文件中的图片链接')
    parser.add_argument('-i', '--input_dir', default='.', help='选择要处理包含markdown文件的目录')
    parser.add_argument('-o', '--output_image_dir', default='./images', help='选择移动图片的目录，拼接到markdown文件所在目录下')
    parser.add_argument('-t', '--image_type', nargs='+', default=['png','jpg'], choices=['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'], help='拓展支持图片类型')
    parser.add_argument('-m', '--move_method', default='move', choices=['move', 'copy', 'link', 'symlink'], help='图片文件移动方式')
    # '-h' 和 '--help' 是 argparse 自动添加的，无需再手动添加
    return parser.parse_args()

def cli():
    args = parse_args()
    logic(args.input_dir, args.output_image_dir, args.image_type, args.move_method)


if __name__ == '__main__':
    cli()