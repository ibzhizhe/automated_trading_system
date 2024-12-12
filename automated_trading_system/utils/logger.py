import logging


class Logger:
    def __init__(self):
        logging.basicConfig(filename='trading_log.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger('trading_system')

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)


class SystemMonitor:
    def __init__(self):
        self.logger = Logger()

    def check_health(self):
        print("系统运行正常")

    def log_error(self, error):
        self.logger.error(f"发生错误: {error}")
