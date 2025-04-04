import logging
from atconstants import AT_LOG_FILE, AT_APP_NAME
from at_utilities.at_logging import atlogging_setup
import at_utilities.at_utils as atu
import at_utilities.at_utils as is_running_in_pytest

def pytest_configure(config):
    """
    PPPActivityTracker/tests: Configure pytest dynamically.
    Use the apps log file and avoid duplicate logging to console as well.
    """
    p = atu.pfx(mn=__name__)  # Use the module name for the prefix
    # Disable pytest's default logging handlers
    root_logger = logging.getLogger()
    print(f"{p}Root logger handlers before atlogging_setup({len(root_logger.handlers)}): {root_logger.handlers}")
    root_logger.handlers.clear()
    print(f"{p}Root logger handlers after clear({len(root_logger.handlers)}): {root_logger.handlers}")

    # Set up logging
    # logger = logging.getLogger(AT_APP_NAME)
    logger = atlogging_setup(AT_APP_NAME)
    # logger.setLevel(logging.DEBUG)
    logger.debug(f"{p}Root logger handlers after atlogging_setup({len(root_logger.handlers)}): {root_logger.handlers}")
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    logger.debug(f"{p}Root logger handlers after clear({len(root_logger.handlers)}): {root_logger.handlers}")
    logger.debug(f"{p}{AT_APP_NAME} logger handlers ({len(logger.handlers)}): {logger.handlers}")
    logger.debug(f"{p}Pytest logging configured dynamically.")

# if __name__ == "__main__":
#     # This block will not execute when pytest runs, only when this file is run directly
#     p = atu.pfx(mn=__name__)  # Use the module name for the prefix
#     if atu.is_running_in_pytest():
#         print(f"{p}This module is running in pytest.")
#     else:
#         pytest_configure(None)
#         logger = logging.getLogger(AT_APP_NAME)
#         logger.debug(f"{p}Pytest configuration complete. Logging is set up for {AT_APP_NAME}.")
