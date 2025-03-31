'''
at_logging.py - Setup logging for the Activity Tracker application. 
Do it is such a way that it is a singleton logger for the application.
Take care to configure both console (stdout) and file logging.
Take care to ensure that the logging setup is idempotent, meaning that if
the setup_logging function is called multiple times, it does not add multiple 
console and file handlers either under actual operation, pytext or single file
debugging. This is important to avoid duplicate log messages in the output.
'''
#------------------------------------------------------------------------------+
import logging, sys, threading
from atconstants import AT_APP_NAME, AT_LOG_FILE
import at_utilities.at_utils as atu

#------------------------------------------------------------------------------+
#region Configure logging
at_logging_initialized = False
_logging_lock = threading.Lock()
def setup_logging(logger_name: str = AT_APP_NAME) -> logging.Logger:
    """Set up logging for both stdout and a log file (thread-safe singleton)."""
    p = atu.pfx()
    global at_logging_initialized

    with _logging_lock:  # Ensure thread-safe access to the logger setup
        if at_logging_initialized:
            logger.debug(f"{p} Logging handlers initialized. First log message.")
            return logging.getLogger(logger_name)
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)  # Set the global logging level

        at_logging_initialized = True

        # debug to learn
        root_logger = logging.getLogger()
        lc = len(root_logger.handlers)  
        print(f"Root logger handlers before setup_logging({lc}): {root_logger.handlers}")

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
        p = atu.pfx()
        logger.debug("============================================================")
        logger.debug(f"{p} Logging handlers initialized. First log message.")
        # Debug: List root logger handlers
        logger.debug(f"  Logger name: {logger.name}, Level: {logger.level}, " + \
                    f"Logging handlers count: {len(logging.getLogger().handlers)}")
        for handler in logger.handlers:
            logger.debug(f"    Handler: {handler}, Level: {handler.level}")
        logger.debug("setup_logging(): Complete.")
        root_logger = logging.getLogger()
        lc = len(root_logger.handlers)
        lnc = len(logger.handlers)
        print(f"Root logger handlers after setup_logging({lc}): {root_logger.handlers}")
        print(f"{logger_name} logger handlers after setup_logging({lnc}): {logger.handlers}")
        return logger

# Initialize logging for the application
if __name__ == "__main__":
    p = atu.pfx()
    logger = setup_logging(AT_APP_NAME)
    logger.debug(f"Imported module: {__name__}")
    logger.debug(f"main.{__name__} Logging initialized.")
#endregion setup_logging()
#------------------------------------------------------------------------------+

#------------------------------------------------------------------------------+
