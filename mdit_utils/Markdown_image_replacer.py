import os
import re
from mdit_utils.log_handler import LogHandler

class MarkdownImageReplacer:
    def __init__(self, network_mapping, local_relative_mapping, local_absolute_mapping):
        # 初始化，传入三种图片映射
        self.network_mapping = network_mapping
        self.local_relative_mapping = local_relative_mapping
        self.local_absolute_mapping = local_absolute_mapping
        self.processed_data = self._replace_images()

    def _replace_images(self):
        # 获取所有需要处理的文件路径
        log = LogHandler()
        all_files = set(
            item['md_file_path'] for item in self.network_mapping +
            self.local_relative_mapping +
            self.local_absolute_mapping
        )

        # 如果没有需要处理的文件，直接返回
        if not all_files:
            print("没有文件需要处理.")
            log.log("没有文件需要处理.")
            return []

        processed_data = []

        # 根据映射表替换markdown文件中的图片引用路径
        for file_path in all_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 创建映射字典
            network_dict = {item['image_path']: self._relative_path(item['local_path'], file_path) for item in self.network_mapping if item['md_file_path'] == file_path}
            local_relative_dict = {item['image_path']: self._relative_path(item['moved_image_path'], file_path) for item in self.local_relative_mapping if item['md_file_path'] == file_path}
            local_absolute_dict = {item['image_path']: self._relative_path(item['moved_image_path'], file_path) for item in self.local_absolute_mapping if item['md_file_path'] == file_path}

            # 替换网络图片路径
            for original_path, new_path in network_dict.items():
                content = content.replace(original_path, new_path)
                # print(f"Processing file: {file_path} - Replacing network image: {original_path} -> {new_path}")
                # LogHandler(f"处理文件: {file_path} - 替换网络图片: {original_path} -> {new_path}")
                log.log(f"处理文件: {file_path} - 替换网络图片: {original_path} -> {new_path}")

            # 替换本地相对路径图片路径
            for original_path, new_path in local_relative_dict.items():
                content = content.replace(original_path, new_path)
                # print(f"处理文件: {file_path} - 替换本地相对路径图片: {original_path} -> {new_path}")
                # LogHandler(f"处理文件: {file_path} - 替换本地相对路径图片: {original_path} -> {new_path}")
                log.log(f"处理文件: {file_path} - 替换本地相对路径图片: {original_path} -> {new_path}")

            # 替换本地绝对路径图片路径
            for original_path, new_path in local_absolute_dict.items():
                content = content.replace(original_path, new_path)
                # print(f"Processing file: {file_path} - Replacing local absolute image: {original_path} -> {new_path}")
                # LogHandler(f"处理文件: {file_path} - 替换本地绝对路径图片: {original_path} -> {new_path}")
                log.log(f"处理文件: {file_path} - 替换本地绝对路径图片: {original_path} -> {new_path}")

            # 将更新后的内容写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # 记录处理后的数据
            processed_data.append({
                'file_path': file_path,
                'network_replacements': network_dict,
                'local_relative_replacements': local_relative_dict,
                'local_absolute_replacements': local_absolute_dict
            })

        return processed_data

    def _relative_path(self, target_path, file_path):
        # 计算相对路径
        return os.path.relpath(target_path, start=os.path.dirname(file_path))

# 示例用法