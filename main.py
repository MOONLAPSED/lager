from src.logs import *
from src.utils import *

def main():
    logger = TpLogger('INFO', 'log.txt', 'branch', 'leaf')
    logger.logger.warning('Hello, World!')
    logger.stop()

if __name__ == '__main__':
    main()
