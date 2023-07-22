import logging
import os

log_directory = os.getcwd()+"/app/log"

if not os.path.exists(log_directory):
    os.makedirs(log_directory)


class SinLogger:
    def __init__(self, file_name):
        self.file_name = file_name
        self.log_filepath = os.path.join(log_directory, f'{file_name}_log.txt')
        self.logger = self._create_logger()

    def _create_logger(self):
        logger = logging.getLogger(self.file_name)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s %(message)s')

        file_handler = logging.FileHandler(self.log_filepath)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def info(self, log_content):
        self.logger.info(log_content)

    def warning(self, log_content):
        self.logger.warning(log_content)

    def error(self, log_content):
        self.logger.error(log_content)
