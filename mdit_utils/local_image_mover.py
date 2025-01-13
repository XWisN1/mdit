import os
import shutil
import re

class LocalImageMover1:
    # 绝对路径
    def __init__(self, local_images, move_method='copy'):
        # 初始化，传入本地图片列表和移动方式
        self.local_images = local_images
        self.move_method = move_method
        self.mapping, self.missing_images = self._move_images()

    def _move_images(self):
        # 根据指定方式移动本地图片到目标目录，并记录映射关系
        mapping = []
        missing_images = []
        for image_info in self.local_images:
            image_path = image_info['image_path']
            file_path = image_info['md_file_path']
            move_path = image_info['move_path']
            if not os.path.exists(image_path):
                missing_images.append({'file_path': file_path, 'local_image_path': image_path})
                continue
            image_name = os.path.basename(image_path)
            target_path = os.path.join(move_path, image_name)
            target_path = os.path.normpath(target_path)  # 规范化路径

            if self.move_method == 'copy':
                shutil.copy(image_path, target_path)
            elif self.move_method == 'move':
                shutil.move(image_path, target_path)
            elif self.move_method == 'link':
                os.link(image_path, target_path)
            elif self.move_method == 'symlink':
                os.symlink(image_path, target_path)

            # 更新 image_info 字典，添加移动后的路径
            image_info['moved_image_path'] = target_path
            mapping.append(image_info)
        # print(f"本次:{self.move_method},丢失图片数量:{len(missing_images)}")

        return mapping, missing_images
    
class LocalImageMover2:
    def __init__(self, local_images, move_method):
        # 初始化，传入本地图片列表和移动方式
        self.local_images = local_images
        self.move_method = move_method
        self.mapping, self.missing_images = self._move_images()

    def _move_images(self):
        # 根据指定方式移动本地图片到目标目录，并记录映射关系
        # print(f"{self.local_images[0:2]}")
        mapping = []
        missing_images = []
        for image_info in self.local_images:
            project_root = image_info['project_root']
            md_image_line = image_info['md_image_line']
            move_path = image_info['move_path']

            # 从md_image_line中提取相对路径
            relative_path = re.search(r'\((.*?)\)', md_image_line).group(1)
            
            # print(f"project_root: {project_root}")
            # 拼接实际的图片路径
            # 将相对路径转为规范的完整路径
            if relative_path.startswith("..\\") or relative_path.startswith("../"):
                relative_path = relative_path.replace("..\\", "").replace("../", "")
                # print(f"更新后的 relative_path: {relative_path}")
            image_path = os.path.normpath(os.path.abspath(os.path.join(project_root, relative_path)))
            # print(f"relative_path: {relative_path}")
            # print(f"project_root: {project_root}")
            # print(f"image_path: {image_path}")

            file_path = image_info['md_file_path']
            if not os.path.exists(image_path):
                missing_images.append({'file_path': file_path, 'local_image_path': image_path})
                # print(f"图片存在: {image_path}")
                continue

            image_name = os.path.basename(image_path)
            target_path = os.path.join(move_path, image_name)
            target_path = os.path.normpath(target_path)  # 规范化路径

            if self.move_method == 'copy':
                shutil.copy(image_path, target_path)
            elif self.move_method == 'move':
                shutil.move(image_path, target_path)
            elif self.move_method == 'link':
                os.link(image_path, target_path)
            elif self.move_method == 'symlink':
                os.symlink(image_path, target_path)

            # 更新 image_info 字典，添加移动后的路径
            image_info['moved_image_path'] = image_path
            mapping.append(image_info)

        # 打印缺失图片数量
        # print(f"本次操作: {self.move_method}, 丢失图片数量: {len(missing_images)}")

        return mapping, missing_images


# 示例用法
if __name__ == "__main__":
    processed_local_images = [
        {'md_file_path': 'D:\\game\\xiao_tools\\POC-main\\POC-main\\短剧影视小程序\\短剧影视小程序前台未授权 漏洞.md', 
         'md_image_line': '![image-20240902103321159](C:/Users/26927/AppData/Roaming/Typora/typora-user-images/image-20240902103321159.png)', 
         'image_path': 'C:\\Users\\26927\\AppData\\Roaming\\Typora\\typora-user-images\\image-20240902103321159.png', 
         'project_root': 'D:\\game\\xiao_tools\\POC-main\\POC-main', 
         'move_path': 'D:\\game\\xiao_tools\\POC-main\\POC-main\\[mdit]mdit[mdit]_movelocal_images'},
        {'md_file_path': 'D:\\game\\xiao_tools\\POC-main\\POC-main\\Apache\\Apache ActiveMQ远程命令执行漏洞.md', 
         'md_image_line': '![](./assets/20231117150110.png)', 
         'image_path': 'D:\\game\\xiao_tools\\POC-main\\POC-main\\assets\\20231117150110.png', 
         'project_root': 'D:\\game\\xiao_tools\\POC-main\\POC-main', 
         'move_path': 'D:\\game\\xiao_tools\\POC-main\\POC-main\\[mdit]mdit[mdit]_movelocal_images'}
    ]
    move_method = 'copy'  # 可以是 'copy', 'move', 'link', 'symlink'
    local_image_mover = LocalImageMover1(processed_local_images, move_method)
    print("Mapping:", local_image_mover.mapping)
    print("Missing Images:", local_image_mover.missing_images)