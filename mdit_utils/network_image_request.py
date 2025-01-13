import os
import requests
from alive_progress import alive_bar
import re

class NetworkImageRequest:
    def __init__(self, image_infos):
        self.image_infos = image_infos
        self.mapping = self._download_images()

    def clean_filename(self, filename):
        # 去除文件名中的非法字符和URL参数
        filename = re.sub(r'[\\/*?:"<>|]', '', filename.split('?')[0])
        # 如果文件名过长，截取最后一部分
        if len(filename) > 100:  # 举例，根据实际情况调整长度
            filename = filename[-100:]
        return filename

    def _download_images(self):
        mapping = []
        total_images = len(self.image_infos)
        
        with alive_bar(total_images, title='Downloading Images', force_tty=True) as bar:
            for image_info in self.image_infos:
                url = image_info['image_path']
                md_file_path = image_info['md_file_path']
                download_path = image_info['download_path']
                image_name = self.clean_filename(os.path.basename(url))
                local_path = os.path.join(download_path, image_name)
                
                os.makedirs(download_path, exist_ok=True)
                
                if os.path.exists(local_path):
                    bar.text = f'=> Skipped: {image_name}'
                    mapping.append(image_info)
                else:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                    try:
                        response = requests.get(url, headers=headers, stream=True)
                        if response.status_code == 200:
                            with open(local_path, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            bar.text = f'=> Downloaded: {image_name}'
                            mapping.append(image_info)
                        else:
                            bar.text = f'=> Failed: {image_name} (Status: {response.status_code})'
                            print(f"Failed to download {url}. Status code: {response.status_code}.")
                    except requests.RequestException as e:
                        bar.text = f'=> Failed: {image_name} (Error: {e})'
                        print(f"Failed to download {url}. Error: {e}.")
                bar()
        return mapping

# # 示例用法