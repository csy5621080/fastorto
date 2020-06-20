from fastapi.logger import logger as _logger
from logging.handlers import RotatingFileHandler
import logging
import sys
import os


def get_logger():
    LOG_ROOT = os.path.join(sys._MEIPASS, "logs") if getattr(sys, 'frozen', False) else './logs'
    formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")
    info_handler = RotatingFileHandler(f'{LOG_ROOT}/info.log', backupCount=0)
    error_handler = RotatingFileHandler(f'{LOG_ROOT}/error.log', backupCount=0)
    logging.getLogger().setLevel(logging.NOTSET)
    _logger.addHandler(info_handler)
    _logger.addHandler(error_handler)
    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    return _logger


logger = get_logger()