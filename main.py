from src.logs import *
from src.utils import *

def main():
    l = TpLogger('INFO', 'log.txt', 'branch', 'leaf')
    dotl = l._freeze()
    print(l)
    l.logger.warning('Hello, World!')
    print(f'{dotl} has {len(l.logger.handlers)} handlers and {len(l.logger.manager.loggerDict)} loggers and type {type(l.logger)}')
    l.stop()

if __name__ == '__main__':
    main()
