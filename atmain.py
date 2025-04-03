#------------------------------------------------------------------------------+
import sys, os
from atconstants import AT_APP_NAME, AT_LOG_FILE
import at_utilities.at_utils as atu
from at_utilities.at_logging import atlogging_setup 
#------------------------------------------------------------------------------+
#region atlogging_setup()
# Configur logging before importing the primary application modules
#if __name__ in  ("__main__", "atmain"):
p=atu.pfx(mn=__name__)
logger = atlogging_setup(AT_APP_NAME)
logger.debug(f"{p}Imported module: {__name__}")
logger.debug(f"{p}{__name__} Logging initialized.")
#endregion atlogging_setup()
#------------------------------------------------------------------------------+
from view import atview 
from viewmodel import mainatviewmodel as MainATViewModel

class Application:
    """Activity Tracker Main Application"""
    atv: atview.ATView = None
    atvm: MainATViewModel.MainATViewModel = None

    def __init__(self):
        p=atu.pfx(mn=__name__)
        logger.info(f"{p}Initializing Application")
        # Load the configuration file
        # TODO: Implement configuration file loading logic
        # config = atconfig.ATConfig(AT_DEFAULT_CONFIG_FILE)

        # Create the ATView for a UX
        self.atv = atview.ATView()
        logger.debug(f"{p}ATView created")

        # If configured, create an MainATViewModel
        self.atvm = MainATViewModel.MainATViewModel(self.atv)
        logger.debug(f"{p}MainATViewModel created")

        # Which subclass(es) of ATModel are used is determined by the
        # configuration file. The MainATViewModel is responsible to load the
        # configuration file and create the appropriate ATModel subclass.

    def run(self):
        """Run the ATView application loop"""
        p=atu.pfx(mn=__name__)
        atenv = atu.at_env_info(__name__,True,logger)
        run_mode = atenv[3]
        logger.debug(f"{p}Running in {run_mode} mode")
        if run_mode == "direct":
            logger.debug(f"{p}Running application atv.mainloop()")
            # Start the ATView main loop only in direct mode
            self.atv.mainloop() if "direct" in atenv else None
            logger.debug(f"{p}Finished application atv.mainloop()")

logger.info(f"{p}Starting the application")
app = Application()
app.run()
logger.info(f"{p}Application exited")

#------------------------------------------------------------------------------+