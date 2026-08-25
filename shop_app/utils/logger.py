import logging
import logging.handlers
from os import path, makedirs
from pathlib import Path
from datetime import datetime


path_logs = f'{Path(__file__).resolve().parent.parent.parent}/logs'

if not path.exists(path_logs):
    makedirs(name=path_logs)

format_date = '%Y-%m-%d %H:%M:%S'
date = datetime.now().strftime(format_date)
format_log = ('%(asctime)s | [%(levelname)s] | %(name)s '
            '| (%(filename)s).%(funcName)s(%(lineno)d) | %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(format_log, datefmt=format_date)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.INFO)
console_logger.setFormatter(formatter)
logger.addHandler(console_logger)

file_logger = logging.handlers.RotatingFileHandler(
    filename=f'{path_logs}/log-{date}.log',
    mode='w',
    maxBytes=10*1024*1024,
    backupCount=10
)
file_logger.setLevel(logging.INFO)
file_logger.setFormatter(formatter)
logger.addHandler(file_logger)

aiogram_logger = logging.getLogger('aiogram')
aiogram_logger.setLevel(logging.INFO)
for handler in logger.handlers:
    aiogram_logger.addHandler(handler)
