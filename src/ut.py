import unittest
from unittest.mock import patch, ANY

from src.logs import TpLogger

class TestLoggerManager(unittest.TestCase):

    def setUp(self):
        # Setup a LoggerManager with test values
        self.log_file_path = 'test.log'
        self.branch_name = 'test_branch'
        self.leaf_name = 'test_leaf'
        self.logger_manager = TpLogger('DEBUG', self.log_file_path, self.branch_name, self.leaf_name)
        return super().setUp()
    
    def __repr__(self) -> str:
        for attr in dir(self):
            if not attr.startswith('__'):
                print(f'{attr}: {getattr(self, attr)}')
        return super().__repr__()

if __name__ == '__main__':
    unittest.main()
