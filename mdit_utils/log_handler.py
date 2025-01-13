from datetime import datetime
class LogHandler:
    def __init__(self, log_file='mdit_images.log'):
        # 初始化，指定日志文件路径
        self.log_file = log_file

    def log(self, message):
        # 将信息记录到日志文件
        with open(self.log_file, 'a',encoding='utf-8') as f:
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {message}\n')