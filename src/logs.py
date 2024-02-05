import logging
import logging.handlers
from logging.config import dictConfig
from queue import Queue
import datetime
from dataclasses import dataclass, field


class TpLogger:
    """
    TpLogger is a class that configures and handles the logging mechanism, separating logs into different files and
    providing a mechanism to log into a queue for inter-process communication or similar purposes.

    Attributes:
        log_file_path (str): The path to the log file.
        branch_name (str): The branch name in the logger hierarchy.
        leaf_name (str): The leaf name in the logger hierarchy.
        queue (Queue): A queue object used for logging messages.
        queue_listener (logging.handlers.QueueListener): A queue listener to process logged events.
        logger (logging.Logger): The logger instance with a specific name.
    """

    def __init__(self, log_file_path: str, branch_name: str, leaf_name: str):
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
        self.logger = self.get_logger(f'{self.branch_name}.{self.leaf_name}')
    
    def tp_config(self, log_file_path: str, branch_name: str, leaf_name: str, queue: Queue):
        """
        Configures the logging system using a dictionary-based configuration.

        Args:
            log_file_path (str): The path to the log file.
            branch_name (str): The base name for the logger hierarchy.
            leaf_name (str): The leaf name for the logger hierarchy.
            queue (Queue): A queue for handling logging messages.
        """
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': '[%(levelname)s]-%(asctime)s|-%(name)s: %(message)s',
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
                    'level': 'INFO',
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

        dictConfig(logging_config)

    def get_logger(self, name: str) -> logging.Logger:
        """
        Retrieves a logger with the specified name.

        Args:
            name (str): The name of the logger to retrieve.
        
        Returns:
            logging.Logger: The logger instance with the specified name.
        """
        return logging.getLogger(name)

    def stop(self):
        """
        Stops the queue listener and waits for it to finish processing messages.
        """
        self.queue_listener.stop()
        self.queue_listener.join()


@dataclass
class BroadcastReporter(TpLogger):
    """
    BroadcastReporter is a subclass of TpLogger, which adds functionality to report logging messages
    with associated metadata such as error codes, exception information, and timestamps.

    Attributes:
        error_message (str): The error message to be logged.
        error_code (int): An error code associated with the message.
        exception (Exception): The exception object associated with the error.
        level (int): The logging level for the message (default: logging.ERROR).
        timestamp (datetime.datetime): The timestamp at which the error was logged.
        exception_type (str): The type of the exception.
        exception_message (str): The message associated with the exception.
    """
    error_message: str
    error_code: int
    exception: Exception
    level: int = logging.ERROR
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    exception_type: str = field(init=False)
    exception_message: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'exception_type', type(self.exception).__name__)
        object.__setattr__(self, 'exception_message', str(self.exception))

    def log_message(self, logger: logging.Logger, level: int, message: str):
        """
        Logs a message with the specified level using the provided logger.

        Args:
            logger (logging.Logger): The logger to use for logging the message.
            level (int): The logging level at which the message should be logged.
            message (str): The message to be logged.
        """
        if level == logging.ERROR:
            logger.error(message, exc_info=self.exception)
        elif level == logging.WARNING:
            logger.warning(message)
        elif level == logging.CRITICAL:
            logger.critical(message)
        elif level == logging.INFO:
            logger.info(message)
        elif level == logging.DEBUG:
            logger.debug(message)
    """
    # Method definitions for log_error, log_warning, log_critical, log_info, and log_debug -
    # Each of these methods call log_message with the corresponding logging level and message.
    """
    def log_error(self, logger: logging.Logger):
        self.log_message(logger, logging.ERROR, self.error_message)

    def log_warning(self, logger: logging.Logger):
        self.log_message(logger, logging.WARNING, self.error_message)

    def log_critical(self, logger: logging.Logger):
        self.log_message(logger, logging.CRITICAL, self.error_message)

    def log_info(self, logger: logging.Logger):
        self.log_message(logger, logging.INFO, self.error_message)

    def log_debug(self, logger: logging.Logger):
        self.log_message(logger, logging.DEBUG, self.error_message)

    def set_level(self, level: int):
        """
        Sets the reporting level of the BroadcastReporter.

        Args:
            level (int): The logging level to be set.
        """
        object.__setattr__(self, 'level', level)

    def get_level(self) -> int:
        """
        Retrieves the current reporting level of the BroadcastReporter.

        Returns:
            int: The current logging level.
        """
        return self.level