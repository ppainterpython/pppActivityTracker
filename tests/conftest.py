import logging
from atconstants import AT_LOG_FILE, AT_APP_NAME
from at_utilities.at_logging import setup_logging
import at_utilities.at_utils as atu

def pytest_configure(config):
    """
    PPPActivityTracker/tests: Configure pytest dynamically.
    Use the apps log file and avoid duplicate logging to console as well.
    """
    p = atu.pfx(mn=__name__)  # Use the module name for the prefix
    # Disable pytest's default logging handlers
    root_logger = logging.getLogger()
    print(f"{p}Root logger handlers before setup_logging({len(root_logger.handlers)}): {root_logger.handlers}")
    root_logger.handlers.clear()
    print(f"{p}Root logger handlers after clear({len(root_logger.handlers)}): {root_logger.handlers}")

    # Set up logging
    # logger = logging.getLogger(AT_APP_NAME)
    logger = setup_logging(AT_APP_NAME)
    # logger.setLevel(logging.DEBUG)
    print(f"{p}Root logger handlers after setup_logging({len(root_logger.handlers)}): {root_logger.handlers}")
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    print(f"{p}Root logger handlers after clear({len(root_logger.handlers)}): {root_logger.handlers}")
    print(f"{p}{AT_APP_NAME} logger handlers ({len(logger.handlers)}): {logger.handlers}")

    # # Create a file handler for pytest logs
    # file_handler = logging.FileHandler(AT_LOG_FILE, mode="a")
    # file_handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(
    #     fmt="%(asctime)s - %(levelname)s - %(message)s",
    #     datefmt="%Y-%m-%d %H:%M:%S"
    # )
    # file_handler.setFormatter(formatter)

    # # Add the file handler to the logger
    # logger.addHandler(file_handler)

    # # Optionally, disable propagation to avoid duplicate logs
    # logger.propagate = False

    logger.debug(f"{p}Pytest logging configured dynamically.")

if __name__ == "__main__":
    # This block will not execute when pytest runs, only when this file is run directly
    
    print(f"{p}Pytest configuration complete. Logging is set up for {AT_APP_NAME}.")