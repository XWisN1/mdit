import os
class FileHandler:
    def __init__(self, files):
        # 初始化，传入文件列表
        self.files = files
        self.md_files = self._extract_md_files()
        self.readme_files = self._extract_readme_files()

    def _extract_md_files(self):
        # 从文件列表中提取出markdown文件
        return [file for file in self.files if file.endswith('.md')]
    def _extract_readme_files(self):
        # 从文件列表中提取出README.md文件
        return [file for file in self.files if os.path.basename(file).lower() == 'readme.md']