#-----------------------------------------------------------------------------+
# test_at_logging.py
#-----------------------------------------------------------------------------+
import logging, sys
from atconstants import AT_APP_NAME
from at_utilities.at_logging import atlogging_setup
import at_utilities.at_utils as atu
import atmain
from atmain import Application as App

# Setup logging for AT compaitble with pytest and other modules
p = atu.pfx(mn=__name__)
logger = atlogging_setup(AT_APP_NAME)
if logger is None:
    logger = logging.getLogger(AT_APP_NAME)  # fallback to default logger if setup failed
    if logger is None:
        logger = logging.getLogger()  # fallback to the root logger if all else fails
if logger is not None:
    logger.debug(f"{p}Imported module: {__name__}")
    logger.debug(f"{p} Logging initialized.")

#-----------------------------------------------------------------------------+
#region test_application_class()
def test_application_class():
    """Test the Application class in atmain.py"""
    # Create an instance of the Application class
    app = App()
    assert app is not None, "Failed to create an instance of the Application class"
    
    # Test the attributes of the Application class
    assert isinstance(app.atv, atmain.atview.ATView), \
        "ATView instance is not created or is of incorrect type"
    assert isinstance(app.atvm, atmain.MainATModel.MainATModel), \
        "MainATModel instance is not created or is of incorrect type"

    # Test the run() method
    # app.run()
    # assert app.atv.mainloop_called, "The mainloop() method was not called"
#endregion test_application_class()