from logging import config as logging_config, getLogger
from logging import Logger
from os.path import join, dirname

from news_service_lib.log_utils import check_log_dir, get_base_log_config

LOG_FILE = join(check_log_dir(join(dirname(__file__), 'var', 'logs')), "news-discovery-app.log")
LOG_CONFIG = get_base_log_config(LOG_FILE)


def get_logger() -> Logger:
    logging_config.dictConfig(LOG_CONFIG)
    return getLogger('main_logger')
