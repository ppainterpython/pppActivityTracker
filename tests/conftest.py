import logging
from atconstants import AT_LOG_FILE, AT_APP_NAME
from at_logging.at_logging import *
import at_utilities.at_utils as atu
import at_utilities.at_utils as is_running_in_pytest

def pytest_configure(config):
    """
    PPPActivityTracker/tests: Configure pytest dynamically.
    Use the app's log file and avoid duplicate logging to console as well.
    """
    me = "conftest.py:pytest_configure(): "
    # some before and after messaging
    root_logger = logging.getLogger()
    root_before_setup = f"{me}Logger('Root') ({len(root_logger.handlers)})" + \
          f" logging handlers before atlogging_setup(): {root_logger.handlers}"

    # Special handling for selected test cases
    if config.args[0].find("test_at_log_config_json") > 0 or \
        config.args[0].find("test_at_log_config") > 0 : 
        m = f"{me}running test_at_log_config_json(), "
        m += "or test_at_log_config(), "
        m += "so do not call atlogging_setup() " 
        m += "and skip the rest of the conftest.py setup."
        print(m)
        print(root_before_setup)
        return

    # Set up logging for the application
    logger = atlogging_setup(AT_APP_NAME)
    # Log the root before, current for our logger, and root after setup
    logger.debug(root_before_setup)
    logger.debug(f"Logger('{AT_APP_NAME}') ({len(logger.handlers)}) " + \
                 f" logging handlers after atlogging_setup(): {logger.handlers}")
    root_logger = logging.getLogger()
    logger.debug(f"Logger('Root') ({len(root_logger.handlers)}) " + \
                 f"logging handlers after atlogging_setup()" + \
                 f": {logger.handlers}")
    logger.debug(f"Completed pytest dynamic logging configuration.")

# if __name__ == "__main__":
#     # This block will not execute when pytest runs, only when this file is run directly
#     if atu.is_running_in_pytest():
#         print(f"This module is running in pytest.")
#     else:
#         pytest_configure(None)
#         logger = logging.getLogger(AT_APP_NAME)
#         logger.debug(f"Pytest configuration complete. Logging is set up for {AT_APP_NAME}.")
