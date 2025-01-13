import os
import re

class ImageHandler:
    def __init__(self, md_files, image_types):
        # 初始化，传入markdown文件列表和图片类型列表
        self.md_files = md_files
        self.image_types = image_types
        self.image_info = self._extract_images_md()
        self.network_images, self.local_absolute_images, self.local_relative_images = self.separate_images()

    def _extract_images_md(self):
        # 从markdown文件中提取指定类型的图片文件，返回json格式数据
        image_info = []
        for md_file in self.md_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 使用正则表达式匹配整个Markdown图片行
                md_image_lines = re.findall(r'(!\[.*?\]\(.*?\))', content)
                # 过滤出以指定图片类型结尾的图片行
                filtered_md_image_lines = [
                    line for line in md_image_lines
                    if any(re.search(r'\((.*?)\)', line).group(1).endswith(img_type) for img_type in self.image_types)
                ]
                # 仅当filtered_md_image_lines非空时，才添加到image_info列表
                if filtered_md_image_lines:
                    image_info.append({'md_file_path': md_file, 'md_images_lines': filtered_md_image_lines})
        return image_info

    def separate_images(self):
        # 将图片分为网络图片、本地绝对路径图片和本地相对路径图片
        network_images = []
        local_absolute_images = []
        local_relative_images = []
        for info in self.image_info:
            for line in info['md_images_lines']:
                # 提取图片路径
                image_path = re.search(r'\((.*?)\)', line).group(1)
                # 检查图片路径是否为网络图片
                if image_path.startswith('http://') or image_path.startswith('https://'):
                    network_images.append({'md_file_path': info['md_file_path'], 'md_image_line': line, 'image_path': image_path})
                else:
                    # 检查是否为绝对路径
                    if os.path.isabs(image_path):
                        local_absolute_images.append({'md_file_path': info['md_file_path'], 'md_image_line': line, 'image_path': image_path})
                    else:
                        # 相对路径
                        local_relative_images.append({'md_file_path': info['md_file_path'], 'md_image_line': line, 'image_path': image_path})
        return network_images, local_absolute_images, local_relative_images
    
    def process_images(self, readme_files):
        # 处理三类图片数据，添加项目根路径和下载路径
        processed_network_images = []
        processed_local_absolute_images = []
        processed_local_relative_images = []

        for image in self.network_images:
            project_root = self._get_project_root(image['md_file_path'], readme_files)
            download_path = os.path.join(project_root, '[mdit]mdit[mdit]_download_images')
            image['project_root'] = project_root
            image['download_path'] = download_path
            processed_network_images.append(image)
            # 确保下载目录存在
            if not os.path.exists(download_path):
                os.makedirs(download_path)
                print(f"创建目录: {download_path}")

        for image in self.local_absolute_images:
            project_root = self._get_project_root(image['md_file_path'], readme_files)
            # 检查图片路径和项目根路径是否在同一个驱动器上
            if os.path.commonprefix([image['image_path'], project_root]):
                # 如果在同一个驱动器上，计算相对路径
                relative_path = os.path.relpath(image['image_path'], project_root)
                image['image_path'] = relative_path
            else:
                # 如果不在同一个驱动器上，直接使用绝对路径
                image['image_path'] = os.path.normpath(image['image_path'])
            move_path = os.path.join(project_root, '[mdit]mdit[mdit]_movelocal_images')
            image['project_root'] = project_root
            image['move_path'] = move_path
            processed_local_absolute_images.append(image)
             # 确保移动目录存在
            if not os.path.exists(move_path):
                os.makedirs(move_path)
                print(f"创建目录: {move_path}")

        for image in self.local_relative_images:
            project_root = self._get_project_root(image['md_file_path'], readme_files)
            # 提取相对路径部分
            relative_path = re.search(r'\((.*?)\)', image['md_image_line']).group(1)
            # 拼接完整路径
            full_path = os.path.normpath(os.path.join(project_root, relative_path.lstrip('./')))
            move_path = os.path.join(project_root, '[mdit]mdit[mdit]_movelocal_images')
            image['project_root'] = project_root
            image['image_path'] = full_path  # 更新为完整路径
            image['move_path'] = move_path
            processed_local_relative_images.append(image)
             # 确保移动目录存在
            if not os.path.exists(move_path):
                os.makedirs(move_path)
                print(f"创建目录: {move_path}")
            

        return processed_network_images, processed_local_absolute_images, processed_local_relative_images

    def _get_project_root(self, md_file_path, readme_files):
        # 从Markdown文件路径逐级向上查找，直到找到最近的README.md文件
        current_path = os.path.dirname(md_file_path)
        while True:
            for readme_file in readme_files:
                if current_path in readme_file:
                    return os.path.dirname(readme_file)
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:
                break
            current_path = parent_path
        return None

# 示例用法
if __name__ == "__main__":
    md_files = [
        'D:\\game\\xiao_tools\\POC-main\\Apache\\Apache ActiveMQ远程命令执行漏洞.md',
        'D:\\game\\xiao_tools\\POC-main\\README.md',
        'D:\\game\\xiao_tools\\POC-main\\Nginx\\Nginx安全漏洞.md',
        'D:\\game\\xiao_tools\\POC-main\\Nginx\\README.md',
        'D:\\game\\xiao_tools\\POC-main\\Tomcat\\Tomcat安全漏洞.md'
    ]
    image_types = ['.jpg', '.png', '.gif']
    handler = ImageHandler(md_files, image_types)
    processed_network_images, processed_local_absolute_images, processed_local_relative_images = handler.process_images(readme_files=[
        'D:\\game\\xiao_tools\\POC-main\\README.md',
        'D:\\game\\xiao_tools\\POC-main\\Nginx\\README.md'
    ])
    print(f"Processed Network Images (First 2): {processed_network_images[0:2]}")
    print(f"Processed Local Absolute Images (First 2): {processed_local_absolute_images[0:2]}")
    print(f"Processed Local Relative Images (First 2): {processed_local_relative_images[0:2]}")