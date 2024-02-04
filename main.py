from src.logs import *
from src.utils import *

def main():
    l = TpLogger('INFO', 'app.log', 'my_branch', 'my_leaf')
    dotl = l._freeze()
    print(l)
    l.logger.warning('Hello, World!')
    print(f'dataclass {dotl} has been frozen with attributes: {fields(dotl)}')
    l.stop()

if __name__ == '__main__':
    main()
