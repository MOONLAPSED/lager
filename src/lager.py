import datetime
import logging
import multiprocessing
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from logging.handlers import RotatingFileHandler 
from logging.config import dictConfig
from abc import ABC, abstractmethod


@dataclass
class LogConfig:
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(levelname)s]%(asctime)s|[%(name)s]: %(message)s',
                'datefmt': '%Y-%m-%d~%H:%M:%S%z'
            },
        },
        'handlers': {
            'console': {
                'level': logging.INFO,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': logging.INFO,
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'app.log',
                'maxBytes': 10485760,
                'backupCount': 10
            },
            'broadcast': {
                'level': logging.INFO,
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'broadcast.log',
                'maxBytes': 10485760,
                'backupCount': 10
            },
            'queue': {
                'level': logging.INFO,
                'formatter': 'default',
                'class': 'logging.handlers.QueueHandler',
                'queue': multiprocessing.Queue(-1)
            }
        },
        'root': {
            'level': logging.INFO,
            'propagate': True,
            'handlers': ['console', 'file']
        }
    }

    logger: logging.Logger = field(init=False)

    def __static_init__(self) -> 'LogConfig':
        """
        Performs run-once initialization of logging configuration and queue handler.
        """
        logging.config.dictConfig(self.LOGGING_CONFIG)
        self.logger = logging.getLogger(__name__)
        return self

    def __init__(self):
        self.__static_init__()

    def __post_init__(self):
        self.logger.info(f"Runtime achieved, root handlers [file, console] initialized\n")
        # ...

if __name__ == "__main__":
    config_instance = LogConfig()
    logger_instance = config_instance.logger

    logger_instance.debug('This is a debug message')
    logger_instance.info('This is an info message')
    logger_instance.warning('This is a warning message')
    logger_instance.error('This is an error message')
    logger_instance.critical('This is a critical message')






