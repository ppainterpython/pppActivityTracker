#------------------------------------------------------------------------------+
# at_logging.py - Setup logging for the Activity Tracker application.
#------------------------------------------------------------------------------+
'''
at_logging.py - Setup logging for the Activity Tracker application. 
Do it is such a way that it is a singleton logger for the application.
Take care to configure both console (stdout) and file logging.
Take care to ensure that the logging setup is idempotent, meaning that if
the atlogging_setup function is called multiple times, it does not add multiple 
console and file handlers either under actual operation, pytext or single file
debugging. This is important to avoid duplicate log messages in the output.
'''
#------------------------------------------------------------------------------+
import logging, logging.config, sys, json, threading, pathlib, logging.handlers
from atconstants import *

#------------------------------------------------------------------------------+
# Globals for singleton use
at_logging_initialized : bool = False
at_log_config : dict = None
_logging_lock = threading.Lock()
#------------------------------------------------------------------------------+
#region get_at_log_config()
def get_at_log_config(config_file:str=AT_LOG_CONFIG_FILE,
                      refresh:bool=False) -> dict:
    """Get the logging configuration from the JSON file.
    If refresh is True, reload the configuration file.
    Get the logging configuration from the specified JSON file."""
    global at_logging_initialized
    global at_log_config
    try:
        config_file = pathlib.Path(config_file)
        if not config_file.exists():
            raise FileNotFoundError(f"Logging configuration file not found: {config_file}")
        with open(config_file, "r") as f:
            at_log_config = json.load(f)
        logging.config.dictConfig(at_log_config)
        print(at_log_config)
        return at_log_config
    except Exception as e:
        m1 = f"Error in get_at_log_config(): {str(e)}"
        print(m1)
        raise
#endregion get_at_log_config()
#------------------------------------------------------------------------------+
#region atlogging_setup()
def atlogging_setup(logger_name: str = AT_APP_NAME) -> logging.Logger:
    """Set up logging for both stdout and a log file (thread-safe singleton)."""
    try:
        global at_logging_initialized
        if logger_name == AT_TEST_EXCEPTION_LOGGER_NAME:
            logger = logging.getLogger(AT_APP_NAME)
            _ = 1/0 # Force an exception to test the exception logger

        with _logging_lock:  # Ensure thread-safe access to the logger setup
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)  # Set the global logging level
            if at_logging_initialized:
                logger = logging.getLogger(logger_name)
                logger.debug(f" Logging handlers previously initialized.")
                return logging.getLogger(logger_name)

            # config_file = pathlib.Path("at_logging/at_log_config.json")
            # with open(config_file, "r") as f:
            #     at_log_config = f.read()
            # logging.config.dictConfig(at_log_config) 

            # debug to learn
            root_logger = logging.getLogger()
            lc = len(root_logger.handlers)  
            msg_before = f"Root logger handlers before atlogging_setup({lc}): {root_logger.handlers}"

            # Create a formatter for consistent log messages
            # Note: not using {name} of the logger, since there is only one
            fmtstr="{asctime}.{msecs:03.0f}:{levelname}:[{process}:{thread}]:" + \
                "{module}.{funcName}() {message}"
            formatter = logging.Formatter(
                fmt=fmtstr,
                datefmt="%Y-%m-%d %H:%M:%S",
                style="{"
            )

            # Create a console handler (stdout)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)  # Set console log level
            console_handler.setFormatter(formatter)

            # Create a file handler
            # file_handler = logging.FileHandler(AT_LOG_FILE, mode="a")  # Append to the log file
            # file_handler.setLevel(logging.DEBUG)  # Set file log level
            # file_handler.setFormatter(formatter)
            file_handler = logging.handlers.RotatingFileHandler(AT_LOG_FILE, mode="a")  # Append to the log file
            file_handler.setLevel(logging.DEBUG)  # Set file log level
            file_handler.setFormatter(formatter)

            # Add handlers to the logger
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
            hdr = "========================================================="
            hdr += "[" + hdr + hdr + "]"
            logger.debug(f"{hdr}")
            logger.debug(f" 1st log message, initialized Logging handlers.")
            # Debug: List root logger handlers
            logger.debug(f"  Logger name: {logger.name}, Level: {logger.level}, " + \
                        f"Logging handlers count: {len(logger.handlers)}")
            for handler in logger.handlers:
                logger.debug(f"    Handler: {handler}, Level: {handler.level}")
            logger.debug(f"atlogging_setup(): Complete.")
            logger.debug(msg_before)
            root_logger = logging.getLogger()
            lc = len(root_logger.handlers)
            lnc = len(logger.handlers)
            logger.debug(f"Root logger handlers after atlogging_setup({lc}): {root_logger.handlers}")
            logger.debug(f"{logger_name} logger handlers after atlogging_setup({lnc}): {logger.handlers}")
            at_logging_initialized = True
            return logger
    except Exception as e:
        m1 = f"Error in atlogging_setup for requested logger: '{logger}'"
        m2 = f"Exception: {e}"
        _ = logger.debug(m1) if logger is not None else print(m1)
        _ = logger.debug(m2) if logger is not None else print(m2)
        raise
#endregion atlogging_setup()
#------------------------------------------------------------------------------+
#region ATLogger CLass - A LoggerAdapter
class ATLogger(logging.LoggerAdapter):
    """
    A custom LoggerAdapter that adds a prefix info to log messages.
    PARAMETERS
    ----------
    logger : logging.Logger
        The logger instance to be used for logging.
    container : object, optional
        An optional name of container class or module making logging calls.
    """
    def __init__(self, logger: logging.Logger, container = None):
        super().__init__(logger, {'cn': container or 'noContainerName'})

    def process(self, msg: str, kwargs):
        """Process the log message by adding the cn parameter to kwargs."""
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        self.extra['extra']['cn'] = self.extra.get('cn', 'noContainerName')
        return msg, kwargs
#endregion ATLogger CLass - A LoggerAdapter
#------------------------------------------------------------------------------+
#region atlogging_header()
#endregion atlogging_header()
#------------------------------------------------------------------------------+
class ClassLogger:
    """A class to provide a logger with a specific class name."""

    def __init__(self):
        cn = self.__class__.__name__
        self.logger = ATLogger(logger, {'cn': self.__class__.__name__})

    def some_method(self) -> None:
        """Get the logger instance."""
        self.logger.debug("This is a debug message from some_method.")

# Initialize logging for running/debugging this script directly
if __name__ == "__main__":
    logger = atlogging_setup(AT_APP_NAME)
    logger.debug(f"Running in direct mode: {__name__}")
    example_instance = ClassLogger()
    example_instance.some_method()
    logger.debug(f"Imported module: {__name__}")
    logger.debug(f"{__name__} Logging initialized.")
    # cwd = os.getcwd(); sys.path.append(cwd)
    # argv = sys.argv; app_full_path = argv[0] if len(argv) >= 1 else "unknown"
    # # Add the current working directory to the path
    # print(f"argv: {argv}, len='{len(argv)}'")
    # print(f"argv[0]: {argv[0]}")
    # app_full_path = argv[0] if len(argv) >= 1 else "unknown"
    # cwd = os.getcwd()
    # sys.path.append(cwd)  # Add the current working directory to the path
    # print(f"Current working directory: {cwd}")
    # print(f"App full path: {app_full_path}")
    # print(f"sys.path: {sys.path}")
#endregion atlogging_setup()
#------------------------------------------------------------------------------+

#------------------------------------------------------------------------------+
