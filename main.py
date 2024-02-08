from src.logs import TpLogger, BroadcastReporter
from src.utils import *
from src.ut import *
class TestMain(unittest.TestCase):
    def test_main(self):
        # Test the main function here
        # self.assertEqual(main(), 0)  # Check if main returns 0
        self.assertEqual(main(), 0)


def main():
    l = BroadcastReporter('app.log', 'my_branch', 'my_leaf')
    ll = l.login('my_branch.my_leaf')
    ll.warning('runtime warning message')
    print(f"logger name: {ll.name}\n|repr|: {ll.__repr__()}")
    return 0; l.logout()

def run_main_and_handle_result():
    result = main()
    if result == 0:
        print("main() returned 0")
        # ...
    else:
        print("main() did not return 0")
        # ...

if __name__ == '__main__':
    run_main_and_handle_result()  # TODO: replace with pytest or A/B testing - see: 'TestMain' above for implementation
    # TestMain.test_main()
    # unittest.main()
