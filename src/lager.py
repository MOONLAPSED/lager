from dataclasses import dataclass, field
import datetime
import xml.etree.ElementTree as ET
import logging
from logging.handlers import RotatingFileHandler 
from logging.config import dictConfig
import os
import sys
from queue import Queue
from abc import ABC, abstractmethod

class TpLogger():

    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,   
        'formatters': {
            'default': {
                'format': '[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
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
                'queue': Queue(-1)
            }
        },
        'root': {  
            'level': logging.INFO,
            'propagate': True,
            'handlers': ['console', 'file']
        }
    }
    @staticmethod
    def __static__init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        dictConfig(self.LOGGING_CONFIG)
        # self.logger.root.setLevel(logging.WARNING)  # comment this out to show [INFO] and [DEBUG] logs
        self.logger.info(f"Logger {self.__class__.__name__} initialized")

    def __init__(self, **kwargs):
        self.__static__init__(self)
        try:
            self.branch = kwargs['branch']
            self.logger.info(f"Successfully assigned 'branch' value: {self.branch}")
        except KeyError:
            self.logger.error("Failed to assign 'branch' value. Key not found in kwargs.")
        except Exception as e:
            self.logger.error(f"An error occurred while assigning 'branch' value: {str(e)}")
        finally:
            self.leaf = None
    def __post_init__(self, **kwargs):
        self.logger.info(f"Runtime achieved, all logging handlers initialized")
        try:
            if self.leaf is not None or 'leaf' in kwargs:
                self.leaf = kwargs.get('leaf')
                self.logger.info(f"Successfully assigned 'leaf' value: {self.leaf}")
            else:
                self.logger.info("'leaf' value is not provided in kwargs and remains None.")
        except Exception as e:
            self.logger.error(f"An error occurred while assigning 'leaf' value: {str(e)}")
        finally:
            self.logger.info(f"Branch: {self.branch}\nLeaf: {self.leaf} fully runtime initialized")
    def login(self, leaf):
        self.leaf = leaf
        self.logger.info(f"Successfully logged in with leaf: {self.leaf}")
        """
        self.logger.addHandler(logging.getLogger('broadcast'))
        self.logger.addHandler(logging.getLogger('queue'))
        self.logger.addHandler(logging.getLogger('file'))
        self.logger.addHandler(logging.getLogger('console'))
        """
        return self
    def logout(self):
        self.leaf = None
        # self.logger.info(f"Successfully logged out")  # comment this out for per-handler logout messages
        """
        self.logger.removeHandler(logging.getLogger('broadcast'))
        self.logger.removeHandler(logging.getLogger('queue'))
        self.logger.removeHandler(logging.getLogger('file'))
        self.logger.removeHandler(logging.getLogger('console'))
        """
        return self

