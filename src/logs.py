import logging
import logging.handlers
from logging.config import dictConfig
from queue import Queue
import datetime
from dataclasses import dataclass, field
import logging
import logging.handlers
from logging.config import dictConfig
import os
import sys
from queue import Queue

def main():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # is there adequate permission to expand the path?
    except Exception as e:
        print(e)
    finally:
        sys.path.extend([
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')),
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'),
            os.path.abspath(os.path.dirname(__file__))
        ])
        return TpLogger(), BroadcastReporter('app.log', 'my_branch', 'my_leaf')

class TpLogger:
    """
    TpLogger is a class that configures and handles the logging mechanism for the application.
    Houses queue-related funcs, logger-related matters are for subclasses with TpLogger serving as a base class and root logger
    providing a mechanism to 'login' to a queue for inter-process communication or similar purposes.

    Attributes:
        log_file_path (str): The path to the log file.
        branch_name (str): The branch name in the logger hierarchy.
        leaf_name (str): The leaf name in the logger hierarchy.
        queue (Queue): A queue object used for logging messages.
        queue_listener (logging.handlers.QueueListener): A queue listener to process logged events.
        logger (logging.Logger): The logger instance with a specific name.
    
    Class methods:
        tp_config: Configures the logging system using a dictionary-based configuration.
        login: Retrieves a logger with the specified name, attached to the TpLogger instance queue.
        logout: Stops the queue listener and waits for it to finish processing messages. TODO: more logic to 'finish processing messages'
    """
    def __init__(self, log_file_path: str, branch_name: str, leaf_name: str):  # root is always the base logger(this TpLogger instance and its children and queue etc.)
        """
        Initializes the TpLogger instance.

        Args:
            log_file_path (str): The path to the log file.
            branch_name (str): The branch name in the logger hierarchy.
            leaf_name (str): The leaf name in the logger hierarchy.
        """
        self.log_file_path = log_file_path
        self.branch_name = branch_name
        self.leaf_name = leaf_name

        self.queue = Queue(-1)
        self.tp_config(log_file_path, branch_name, leaf_name, self.queue)
        self.queue_listener = logging.handlers.QueueListener(self.queue)
        self.queue_listener.start()
        self.logger = logging.getLogger(f'{branch_name}.{leaf_name}')
        self.logger.warning('This is a runtime warning')
        self.logger.info('This is a runtime info message')

    @staticmethod  # static method called on class via TpLogger.tp_config()
    def tp_config(log_file_path: str, branch_name: str, leaf_name: str, queue: Queue):
        """Static method to configure logging"""
        
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': '[%(levelname)s]-%(asctime)s|-%(name)s: %(message)s',
                    'datefmt': '%Y-%m-%d~%H:%M:%S%z'
                }
            },
            'handlers': {
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'default'
                },
                'file': {
                    'level': 'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': log_file_path,
                    'maxBytes': 10485760,
                    'backupCount': 10,
                    'formatter': 'default'
                },
                'queue': {
                    'class': 'logging.handlers.QueueHandler',
                    'queue': queue
                }
            },
            'loggers': {
                '': {
                    'level': 'DEBUG',
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
                'level': 'INFO',
                'handlers': ['console', 'file']
            }
        }

        dictConfig(config)



@dataclass
class BroadcastReporter(TpLogger):
    """
    The BroadcastReporter class is a specialized subclass of TpLogger designed for enriched logging. It extends the base logging functionality with additional metadata—such as error codes, exception information, and hierarchical context—associated with the log messages.

    By using a BroadcastReporter instance, messages are logged with this augmented information, which is especially useful for error reporting and diagnostic purposes in a production environment. For example:

        br_instance = BroadcastReporter('/path/to/logfile', 'branch', 'leaf', ...)
        br_instance.log_error()    # Logs an error message with additional context

    The class methods log_error, log_warning, log_info, log_debug, and log_critical are tailored to handle varying levels of logging severity. Each method encapsulates the process of adding detailed metadata and then delegates the actual logging to the underlying logging.Logger instance accessible through self.logger. This design adheres to object-oriented principles and provides a structured approach to logging throughout an application.

    Attributes:
        error_message (str): The error message to be logged.
        error_code (int): An error code associated with the message.
        exception (Exception): The exception object associated with an error (if any).
        level (int): The logging level for the message. Defaults to logging.ERROR.
        timestamp (datetime.datetime): The timestamp when the log entry is created.
        exception_type (str): The type of the exception. Automatically derived from the exception attribute.
        exception_message (str): The message associated with the exception. Also derived from the exception attribute.

    The instantiation of BroadcastReporter initializes TpLogger with a given hierarchy and starts a QueueListener for asynchronous logging if required for multi-threaded or multi-process scenarios. This sets up a robust logging system capable of handling complex logging needs.

    Methods such as serialize_log provide a way to convert log entries to a structured format for serialization or transmission to external systems, which may be essential for logging analysis and monitoring.
    """
    error_code: int
    level: int = logging.ERROR
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def log_message(self, logger: logging.Logger, level: int, message: str):
        """
        Logs a message with the specified level using the provided logger.

        Args:
            logger (logging.Logger): The logger to use for logging the message.
            level (int): The logging level at which the message should be logged.
            message (str): The message to be logged.
        """
        extra_info = {'exc_info': self.exception} if level == logging.ERROR else {}
        logger.log(level, message, **extra_info)
    
    def getset_level(self, level: int):
        """
        Sets the reporting level of the BroadcastReporter.

        Args:
            level (int): The logging level to be set.
        """
        object.__setattr__(self, 'level', level)
        return self.level

    def log_error(self):
        self.logger.error(self.error_message, exc_info=self.exception)

    def serialize_log(self) -> dict:
        """
        Serializes the log data into a dictionary.

        Returns:
            dict: A dictionary containing the log data.
        """
        return {
            'error_message': self.error_message,
            'error_code': self.error_code,
            'exception_type': self.exception_type,
            'exception_message': self.exception_message,
            'level': self.level,
            'timestamp': self.timestamp
        }
    def __str__(self) -> str:
        return super().__str__()

    def login(self, name: str) -> logging.Logger:  # renamed from getlogger to differentiate from the built-in getLogger
        """
        Retrieves a logger with the specified name.

        Args:
            name (str): The name of the logger to retrieve.
        
        Returns:
            logging.Logger: The logger instance with the specified name.
        """
        # TODO 'login' functionality to handle queue-related matters (see 'logout' method for queue_listener.stop to end the app)
        """
        def __repr__(self) -> str:
            for attr in dir(self):
                if not attr.startswith('__'):
                    print(f'{attr}: {getattr(self, attr)}')
            return super().__repr__()
        """
        
        return logging.getLogger(name)

    def logout(self):
        """
        Stops the queue listener and waits for it to finish processing messages.
        """
        for item in dir(self.queue_listener):
            print(f'{item}: {getattr(self.queue_listener, item)}')
        self.queue_listener.stop()
        self.queue_listener.join()




if __name__ == '__main__':
    main()