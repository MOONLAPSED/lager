from src.lager import TpLogger

ll = TpLogger()
ll.logger.warning(f"Runtime warning per instance of {ll.__class__.__name__} class\n\n|repr|: {ll.__repr__()}\n")
try:
    ll.login('runtime_leaf')
    # insert test for root.branch.leaf runtime sub-logger
    ll.logger.info(f"Testing sub-logger for root.branch.leaf: {ll.__class__.__name__} class\n\n|repr|: {ll.__repr__()}\n")
    # insert test for root.branch.leaf runtime sub-logger
    ll.logout()
except Exception as e:
    ll.logger.error(f"An error occurred while logging in and out: {str(e)}")
finally:
    ll.logger.info(f"Runtime concluded, all logging handlers removed\n")