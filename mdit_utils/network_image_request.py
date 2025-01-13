import os
import requests
from alive_progress import alive_bar
import re

class NetworkImageRequest:
    def __init__(self, image_infos):
        # 初始化，传入包含文件路径和图片URL的列表
        self.image_infos = image_infos
        self.mapping = self._download_images()

    def clean_filename(self, filename):
        # 去除文件名中的非法字符
        filename = re.sub(r'[\\/*?:"<>|]', '', filename)
        # 去除URL参数
        filename = filename.split('?')[0]
        if len(filename) > 100:
            filename = filename[:100]
        return filename

    def _download_images(self):
        # 下载网络图片到指定目录，并记录url与本地图片的映射关系
        mapping = []
        total_images = len(self.image_infos)
        skipped_count = 0
        success_count = 0
        failed_count = 0
        
        # 使用alive_bar显示进度条
        with alive_bar(total_images, title='Downloading Images', force_tty=True) as bar:
            for image_info in self.image_infos:
                url = image_info['image_path']
                md_file_path = image_info['md_file_path']
                download_path = image_info['download_path']
                image_name = os.path.basename(url)
                image_name = self.clean_filename(image_name)
                local_path = os.path.join(download_path, image_name)
                
                # 规范化路径
                local_path = os.path.normpath(local_path)
                
                # 确保目标目录存在
                os.makedirs(download_path, exist_ok=True)
                
                # 检查目标目录中是否已存在该图片文件
                if os.path.exists(local_path):
                    skipped_count += 1
                    bar.text = f'=> Skipped: {image_name}'  # 更新跳过信息
                    mapping.append({
                        'md_file_path': md_file_path,
                        'md_image_line': image_info['md_image_line'],
                        'image_path': url,
                        'project_root': image_info['project_root'],
                        'download_path': download_path,
                        'local_path': local_path
                    })
                else:
                    try:
                        response = requests.get(url, stream=True)
                        if response.status_code == 200:
                            with open(local_path, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            success_count += 1
                            bar.text = f'=> Downloaded: {image_name}'  # 更新下载信息
                            mapping.append({
                                'md_file_path': md_file_path,
                                'md_image_line': image_info['md_image_line'],
                                'image_path': url,
                                'project_root': image_info['project_root'],
                                'download_path': download_path,
                                'local_path': local_path
                            })
                        else:
                            failed_count += 1
                            bar.text = f'=> Failed: {image_name} (Status: {response.status_code})'
                            mapping.append(image_info)
                            print(f"Failed to download {url}. Status code: {response.status_code}.")
                    except requests.RequestException as e:
                        failed_count += 1
                        bar.text = f'=> Failed: {image_name} (Error: {e})'
                        mapping.append(image_info)
                        print(f"Failed to download {url}. Error: {e}.")
                bar()  # 更新进度条

        # 打印统计信息
        if skipped_count != 0:
            print(f"下载文件跳过 {skipped_count} 次，已存在本地文件.")
        if success_count != 0:
            print(f"下载文件成功 {success_count} 次.")
        if failed_count != 0:
            print(f"下载文件失败 {failed_count} 次，请检查网络后重新运行脚本.")

        return mapping

# 示例用法