#------------------------------------------------------------------------------+
import logging, sys

AT_APP_NAME ="PPPActivityTracker"
AT_DEFAULT_CONFIG_FILE = "atconfig.ini" # default config file for the application
AT_LOG_FILE = AT_APP_NAME + ".log"

#------------------------------------------------------------------------------+
#region Configure logging
def setup_logging():
    """Set up logging for both stdout and a log file."""
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the global logging level

    # Create a formatter for consistent log messages
    formatter = logging.Formatter(
        fmt="{asctime} - {name} - {levelname} - {message}",
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
    logger.debug("Logging handlers initialized.")
    # Debug: Check root logger handlers
    root_logger = logging.getLogger()
    print(f"Root logger handlers: {root_logger.handlers}")

    return logger

# Initialize logging
logger = setup_logging()
logger.debug(f"{__name__} Logging initialized.")
logger.debug(f"{__name__} Logger name: {logger.name}, Level: {logger.level}")
for handler in logger.handlers:
    logger.debug(f"    Handler: {handler}, Level: {handler.level}")
#endregion
#------------------------------------------------------------------------------+

from view import atview 
from viewmodel import atviewmodel

class Application:
    """Activity Tracker Main Application"""
    atv: atview.ATView = None
    atvm: atviewmodel.ATViewModel = None

    def __init__(self):
        logger.info("Initializing Application")
        # Load the configuration file
        # TODO: Implement configuration file loading logic
        # config = atconfig.ATConfig(AT_DEFAULT_CONFIG_FILE)

        # Create the ATView for a UX
        self.atv = atview.ATView()
        logger.debug("ATView created")

        # If configured, create an ATViewModel
        self.atvm = atviewmodel.ATViewModel(self.atv)
        logger.debug("ATViewModel created")

        # Which subclass(es) of ATModel are used is determined by the
        # configuration file. The ATViewModel is responsible to load the
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