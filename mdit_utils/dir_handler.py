import os

class DirHandler:
    def __init__(self, dir_path):
        # 初始化，传入目录路径，并转换为绝对路径
        self.dir_path = os.path.abspath(dir_path)
        self.excluded_dirs = ['mdit_utils']  # 默认排除的目录名称列表
        self.dirs, self.files = self._get_dirs_and_files()

    def _get_dirs_and_files(self):
        # 递归遍历目录，返回所有子目录和文件的绝对路径，排除指定的目录
        dirs = []
        files = []
        for root, subdirs, filenames in os.walk(self.dir_path):
            # 过滤掉排除的目录
            subdirs[:] = [d for d in subdirs if d not in self.excluded_dirs]
            for subdir in subdirs:
                dirs.append(os.path.abspath(os.path.join(root, subdir)))
            for filename in filenames:
                files.append(os.path.abspath(os.path.join(root, filename)))
        return dirs, files