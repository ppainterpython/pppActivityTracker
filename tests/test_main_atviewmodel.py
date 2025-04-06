#------------------------------------------------------------------------------+
import time
from typing import List
from pytest import approx
from atconstants import *
import at_utilities.at_utils as atu
from at_utilities.at_logging import atlogging_setup 
#region atlogging_setup()
# Configur logging before importing the primary application modules
logger = atlogging_setup(AT_APP_NAME)
logger.debug(f"Imported module: {__name__}")
logger.debug(f"{__name__} Logging initialized.")
#endregion atlogging_setup()
from at_utilities.at_events import ATEvent
from viewmodel.base_atviewmodel.atviewmodel import ATViewModel
from viewmodel.main_atviewmodel import MainATViewModel

#------------------------------------------------------------------------------+
#region test_viewmodel_constructor()
def test_viewmodel_constructor():
    logger.debug(f"Starting test_viewmodel_constructor()")
    matvm = MainATViewModel()
    assert matvm is not None, \
        f"Failed to create an instance of MainATViewModel."
    assert isinstance(matvm, MainATViewModel), \
        f"Created instance is not of type MainATViewModel, " \
        f"but instead is of type {type(matvm)}."
    assert matvm.activity_store_uri == AT_DEFAULT_ACTIVITY_STORE_URI, \
        f"Expected activity_store_uri to be '{AT_DEFAULT_ACTIVITY_STORE_URI}', " \
        f"but got '{matvm.activity_store_uri}'"
    assert not matvm.initialized
    matvm.initialize()  # Call initialize to set the internal state
    assert matvm.initialized, \
        f"Failed to initialize the MainATViewModel instance properly."
    matvm.stop()
    assert not matvm.initialized, \
        f"Expected MainATViewModel to be uninitialized after stop(), " \
        f"but it is still initialized."
    del matvm
    logger.debug(f"Completed test_viewmodel_constructor()")
#endregion test_viewmodel_constructor()
#------------------------------------------------------------------------------+
#region test_viewmodel_eventing()
def test_viewmodel_eventing():
    logger.debug(f"Starting test_viewmodel_eventing()")
    
    # Create an instance of MainATViewModel
    matvm = MainATViewModel()
    assert matvm is not None, \
        f"Failed to create an instance of MainATViewModel."
    
    # Initialize the viewmodel to setup the event manager
    matvm.initialize()
    time.sleep(2)
    # Create and publish events
    event1 = ATEvent("EventType1", {"key1": "value1"})
    matvm.publish(event1)  # Publish the first event
    time.sleep(2)
        
    # Stop the viewmodel and ensure it can be stopped without issues
    matvm.stop()
    
    del matvm
    logger.debug(f"Completed test_viewmodel_eventing()")
    #endregion test_viewmodel_eventing()