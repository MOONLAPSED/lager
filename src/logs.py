import logging
from logging import handlers, config, getLogger, Logger, LogRecord
from logging.handlers import QueueListener
from logging.config import dictConfig
import queue
from queue import Queue
import datetime
from datetime import datetime
import dataclasses
from dataclasses import dataclass, field, fields, make_dataclass

class TpLogger:
    def tp_config(self, log_level: str, log_file_path: str, branch_name: str, leaf_name: str, queue: Queue):
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': '[%(levelname)s] %(asctime)s || %(name)s: %(message)s',
                    'datefmt': '%Y-%m-%d~%H:%M:%S%z'
                },
            },
            'handlers': {
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                },
                'file': {
                    'level': log_level,
                    'formatter': 'default',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': log_file_path,
                    'maxBytes': 10485760,
                    'backupCount': 10
                },
                'queue': {
                    'class': 'logging.handlers.QueueHandler',
                    'queue': queue,
                }
            },
            'loggers': {
                '': {
                    'level': log_level,
                    'handlers': ['queue'],
                    'propagate': True
                },
                branch_name: {
                    'level': 'DEBUG',
                    'handlers': [],
                    'propagate': True
                },
                f'{branch_name}.{leaf_name}': {
                    'level': 'DEBUG',
                    'handlers': [],
                    'propagate': True
                }
            },
            'root': {
                'level': log_level,
                'handlers': ['console', 'file']
            }
        }

        dictConfig(logging_config)

    def get_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(name)  # this is the object that you will use to log messages.

    def stop(self):
        self.queue_listener.stop()

    def __init__(self, log_level: str, log_file_path: str, branch_name: str, leaf_name:str):
        self.log_level = log_level
        self.log_file_path = log_file_path
        self.branch_name = branch_name
        self.leaf_name = leaf_name

        self.queue = Queue(-1)
        self.tp_config(log_level, log_file_path, branch_name, leaf_name, self.queue)
        self.queue_listener = logging.handlers.QueueListener(self.queue)
        self.queue_listener.start()
        self.logger = self.get_logger(f'{self.branch_name}.{self.leaf_name}')


def __post_init__(self):
    object.__setattr__(self, 'exception_type', type(self.exception).__name__)
    object.__setattr__(self, 'exception_message', str(self.exception))
    return make_dataclass('FrozenBroadcastReporter', [(field.name, field.type) for field in fields(self)], frozen=True)(*self.serialize())

def main():
    logger = TpLogger('INFO', 'log.txt', 'branch', 'leaf')
    logger.logger.warning('Hello, World!')
    logger.stop()

if __name__ == '__main__':
    main()
