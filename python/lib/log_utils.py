import logging
import sys


def init_root_logger():
    log_format = "%(asctime)s - %(name)s (%(lineno)s) - %(levelname)-8s - %(threadName)-12s - %(message)s"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    logging.basicConfig(format=log_format, handlers=[console_handler])
