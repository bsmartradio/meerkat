import logging
import sys
from datetime import datetime


def init(loglevel, log_path, file_name):
    logging.basicConfig(level=loglevel)

    root_logger = logging.getLogger()

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    file_handler = logging.FileHandler("{0}/{1}.log".format(log_path, f'{file_name}-{datetime.now().strftime("%Y%m%d")}'))
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)
