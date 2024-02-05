from src.logs import TpLogger, BroadcastReporter
from src.utils import *
from src.ut import *
class TestMain(unittest.TestCase):
    def test_main(self):
        # Test the main function here
        # You can use assert statements to check the expected behavior
        # For example:
        # self.assertEqual(main(), 0)  # Check if main returns 0
        self.assertEqual(main(), 0)


def main():
    l = BroadcastReporter('app.log', 'my_branch', 'my_leaf')
    print(f"logger name {l}\n level: {l.level}\n |repr|: {l.__repr__()}\n")
    ll = l.get_logger('my_branch.my_leaf')
    ll.warning('runtime warning message')
    print(f"logger name: {ll.name}\n level: {ll.level}\n |repr|: {ll.__repr__()}")
    return 0

if __name__ == '__main__':
    main()

    for attr in dir(main):  # no non-public functions should appear in the output
        if not attr.startswith('__'):
            print(f'{attr}: {getattr(main, attr)}')

