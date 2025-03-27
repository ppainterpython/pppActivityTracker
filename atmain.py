#------------------------------------------------------------------------------+
import logging, sys
from atconstants import AT_APP_NAME, AT_LOG_FILE


#------------------------------------------------------------------------------+
#region Configure logging
def setup_logging(logger_name: str = AT_APP_NAME) -> logging.Logger:
    """Set up logging for both stdout and a log file."""
    # TODO: use custom formatter to make loglevel fixed width characters
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
    logger.debug("setup_logging(): Logging handlers initialized. First log message.")
    # Debug: List root logger handlers
    logger.debug(f"  Logger name: {logger.name}, Level: {logger.level}, " + \
                 f"Logging handlers count: {len(logging.getLogger().handlers)}")
    for handler in logger.handlers:
        logger.debug(f"    Handler: {handler}, Level: {handler.level}")
    logger.debug("setup_logging(): Complete.")
    return logger

# Initialize logging for the application
if __name__ == "__main__":
    logger = setup_logging(AT_APP_NAME)
    logger.debug(f"Imported module: {__name__}")
    logger.debug(f"main.{__name__} Logging initialized.")
#endregion
#------------------------------------------------------------------------------+

from view import atview 
from viewmodel import mainatviewmodel as MainATViewModel

class Application:
    """Activity Tracker Main Application"""
    atv: atview.ATView = None
    atvm: MainATViewModel.MainATModel = None

    def __init__(self):
        logger.info("Initializing Application")
        # Load the configuration file
        # TODO: Implement configuration file loading logic
        # config = atconfig.ATConfig(AT_DEFAULT_CONFIG_FILE)

        # Create the ATView for a UX
        self.atv = atview.ATView()
        logger.debug("ATView created")

        # If configured, create an MainATModel
        self.atvm = MainATViewModel.MainATModel(self.atv)
        logger.debug("MainATModel created")

        # Which subclass(es) of ATModel are used is determined by the
        # configuration file. The MainATModel is responsible to load the
        # configuration file and create the appropriate ATModel subclass.

    def run(self):
        """Run the ATView application loop"""
        logger.info("Running the application")
        self.atv.mainloop()

if __name__ == "__main__":
    logger.info("Starting the application")
    app = Application()
    app.run()
    logger.info("Application exited")

#------------------------------------------------------------------------------+