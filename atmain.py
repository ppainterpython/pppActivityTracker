#------------------------------------------------------------------------------+
import logging, sys
from atconstants import AT_APP_NAME, AT_LOG_FILE
from at_utilities.at_logging import setup_logging
#------------------------------------------------------------------------------+
#region setup_logging()

# Initialize logging for the application
if __name__ == "__main__":
    logger = setup_logging(AT_APP_NAME)
    logger.debug(f"Imported module: {__name__}")
    logger.debug(f"main.{__name__} Logging initialized.")
#endregion setup_logging()
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