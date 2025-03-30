#------------------------------------------------------------------------------+
import logging, sys
from atconstants import AT_APP_NAME, AT_LOG_FILE
import at_utilities.at_utils as atu

#------------------------------------------------------------------------------+
#region Configure logging
def setup_logging(logger_name: str = AT_APP_NAME) -> logging.Logger:
    """Set up logging for both stdout and a log file."""
    # TODO: use custom formatter to make loglevel fixed width characters
    p = atu.pfx()
    # Create a logger
    root_logger = logging.getLogger()
    print(f"Root logger handlers before setup_logging(): {root_logger.handlers}")

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # Set the global logging level

    # Create a formatter for consistent log messages
    formatter = logging.Formatter(
        fmt="{asctime}.{msecs:03.0f}:{levelname}:[{name}] {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{"
    )

    # Create a console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)  # Set console log level
    console_handler.setFormatter(formatter)

    # Create a file handler
    file_handler = logging.FileHandler(AT_LOG_FILE, mode="a")  # Append to the log file
    file_handler.setLevel(logging.DEBUG)  # Set file log level
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.debug("============================================================")
    logger.debug(f"{p} Logging handlers initialized. First log message.")
    # Debug: List root logger handlers
    logger.debug(f"  Logger name: {logger.name}, Level: {logger.level}, " + \
                 f"Logging handlers count: {len(logging.getLogger().handlers)}")
    for handler in logger.handlers:
        logger.debug(f"    Handler: {handler}, Level: {handler.level}")
    logger.debug("setup_logging(): Complete.")
    return logger

# Initialize logging for the application
if __name__ == "__main__":
    p = atu.pfx()
    logger = setup_logging(AT_APP_NAME)
    logger.debug(f"Imported module: {__name__}")
    logger.debug(f"main.{__name__} Logging initialized.")
#endregion setup_logging()
#------------------------------------------------------------------------------+
