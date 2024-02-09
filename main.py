from src.lager import TpLogger
import unittest

class TestMain(unittest.TestCase):
    def test_main(self):
        # Test the main function here
        # self.assertEqual(main(), 0)  # Check if main returns 0
        self.assertEqual(main(), 0)


def main():
    ll = TpLogger()
    ll.logger.warning(f"Runtime warning per instance of {ll.__class__.__name__} class\n\n|repr|: {ll.__repr__()}\n")
    try:
        ll = ll.__class__(branch='root', leaf='runtime_leaf')  # Assign new instance to ll
        ll.login('runtime_leaf')
    except Exception as e:
        ll.logger.error(f"An error occurred while logging in and out: {str(e)}")
    finally:
        ll.logger.info(f"Runtime concluded, all logging handlers removed\n")
    return 0; ll.logout()


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


