#-----------------------------------------------------------------------------+
# test_at_logging.py
#-----------------------------------------------------------------------------+
import logging, pytest
from atconstants import *
from at_logging.at_logging import atlogging_setup
import at_utilities.at_utils as atu
from view.atview import ATView
from viewmodel.main_atviewmodel import MainATViewModel
import atmain
from atmain import Application as App

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown(autouse=True):
    """
    Setup and teardown for the module.
    This is used to initialize logging and clean up after tests.
    """
    # Setup logging for the module
    logger = atlogging_setup(AT_APP_NAME)
    if logger:
        logger.debug(f"Setup for test module: {__name__}")
    
    yield

    if logger:
        logger.debug(f"Teardown for test module: {__name__}")

# Setup logging for AT compaitble with pytest and other modules
logger = atlogging_setup(AT_APP_NAME)
if logger is None:
    logger = logging.getLogger(AT_APP_NAME)  # fallback to default logger if setup failed
    if logger is None:
        logger = logging.getLogger()  # fallback to the root logger if all else fails
if logger is not None:
    logger.debug(f"Imported module: {__name__}")
    logger.debug(f" Logging initialized.")

#-----------------------------------------------------------------------------+
#region test_application_class()
def test_application_class():
    """Test the Application class in atmain.py"""
    # Create an instance of the Application class
    app = App()
    assert app is not None, "Failed to create an instance of the Application class"
    
    # Test the attributes of the Application class
    assert isinstance(app.atv, ATView), \
        "ATView instance is not created or is of incorrect type"
    assert isinstance(app.atvm, MainATViewModel), \
        "MainATViewModel instance is not created or is of incorrect type"
    assert app.atvm.activity_store_uri == AT_DEFAULT_ACTIVITY_STORE_URI, \
        f"Expected atvm.activity_store_uri: '{AT_DEFAULT_ACTIVITY_STORE_URI}' " \
        + F"but received '{app.atvm.activity_store_uri}'"
    # Test the app.activity_store_uri property setter and getter
    newval = "test.json"; app.atvm.activity_store_uri = newval
    assert app.atvm.activity_store_uri == newval, \
        f"Expected atvm.activity_store_uri: '{newval}' " + \
            f"but received '{app.atvm.activity_store_uri}'"
    # Test the app.atvm.atview property setter and getter
    assert (newview := ATView()) is not None, \
        "Failed to create a new instance of ATView for testing the atview property"
    assert (oldview := app.atvm.atview) is not None, \
        f"Failed to get the initial atview property from MainATViewModel"
    app.atvm.atview = newview  # Set a new view to the atvm
    assert app.atvm.atview == newview, \
        f"Expected app.atvm.atview: {newview} but received: '{newview}'"
    assert app.atvm.atview == newview, \
        f"Expected app.atvm.atview to change from {oldview} to {newview}"
    # Test the run() method to ensure it returns None and does not call
    #  mainloop except in direct mode.
    assert app.run() is None, "The run() method did not return None as expected"

    # Test the run() method
    # app.run()
    # assert app.atv.mainloop_called, "The mainloop() method was not called"
#endregion test_application_class()