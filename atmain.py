#------------------------------------------------------------------------------+
import logging, sys
from atconstants import AT_APP_NAME, AT_LOG_FILE
from at_utilities.at_logging import atlogging_setup
#------------------------------------------------------------------------------+

# When running under the VSCode Python Debugger, the argv[0] is the full path to the
# and will look something like this:
# 'c:\\Users\\ppain\\.vscode\\extensions\\ms-python.python-2025.2.0-win32-x64\\python_files\\vscode_pytest\\run_pytest_script.py'
#region atlogging_setup()

argv = sys.argv
app_full_path = argv[0] if len(argv) > 1 else "unknown"

if __name__ == "__main__":
    logger = atlogging_setup(AT_APP_NAME)
    logger.debug(f"Imported module: {__name__}")
    logger.debug(f"main.{__name__} Logging initialized.")
#endregion atlogging_setup()
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