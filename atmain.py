#------------------------------------------------------------------------------+
from atconstants import *
import at_utilities.at_utils as atu
from at_logging.at_logging import atlogging_setup 
#------------------------------------------------------------------------------+
#region atlogging_setup()
# Configur logging before importing the primary application modules
logger = atlogging_setup(AT_APP_NAME)
logger.debug(f"Imported module: {__name__}")
logger.debug(f"{__name__} Logging initialized.")
#endregion atlogging_setup()
#------------------------------------------------------------------------------+
from view.atview import ATView 
from viewmodel.main_atviewmodel import MainATViewModel

class Application:
    """Activity Tracker Main Application"""
    def __init__(self):
        atv: ATView = None
        atvm: MainATViewModel = None
        logger.info(f"Initializing Application")
        # Load the configuration file
        # TODO: Implement configuration file loading logic
        # config = atconfig.ATConfig(AT_DEFAULT_CONFIG_FILE)

        # Create the ATView for a UX
        self.atv = ATView()
        logger.debug(f"ATView created")

        # Create an MainATViewModel
        self.atvm = MainATViewModel(self.atv)
        logger.debug(f"MainATViewModel created")

        # Which subclass(es) of ATModel are used is determined by the
        # configuration file. The MainATViewModel is responsible to load the
        # configuration file and create the appropriate ATModel subclass.

    def run(self) -> None:
        """Run the ATView application loop"""
        atenv = atu.at_env_info(__name__,logger)
        run_mode = atenv[3]
        logger.debug(f"Running in {run_mode} mode")
        if run_mode == "direct":
            logger.debug(f"Running application atv.mainloop()")#  pragma: no cover
            # Start the ATView main loop only in direct mode
            self.atv.mainloop() if "direct" in atenv else None # pragma: no cover
            logger.debug(f"Finished application atv.mainloop()") # pragma: no cover
        return None

logger.info(f"Starting the application")
app = Application()
app.run()
logger.info(f"Application exited")

#------------------------------------------------------------------------------+