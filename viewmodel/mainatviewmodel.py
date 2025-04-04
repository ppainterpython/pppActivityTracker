#-----------------------------------------------------------------------------+
from atconstants import *
import at_utilities.at_utils as atu
from at_utilities.at_logging import atlogging_setup 
#------------------------------------------------------------------------------+
#region atlogging_setup()
# Configur logging before importing the primary application modules
p=atu.pfx(mn=__name__)
logger = atlogging_setup(AT_APP_NAME)
logger.debug(f"{p}Imported module: {__name__}")
logger.debug(f"{p}{__name__} Logging initialized.")
#endregion atlogging_setup()
#------------------------------------------------------------------------------+
from viewmodel.base_atviewmodel.atviewmodel import ATViewModel
from view import atview

class MainATViewModel(ATViewModel):
    '''    MainATViewModel is a concrete subclass of ATModel, representing the
    ViewModel for the Activity Tracker application. Optionally, it associates 
    a View object.
    
    The ViewModel is responsible to present data properties and methods to the 
    View sufficient to support the View's functionality. The ViewModel is also
    responsible to update the View when the underlying data model changes.
    
    View - handles property change notifcations from ViewModel, raises UI events
    for view elements bound to ViewModel properties and methods. Accesses
    Viewmodel properties to update the view.

    ViewModel - handles property change notifications from the Model, raises
    PropertyChanged events for view elements bound to ViewModel properties and 
    Provides Properties accessible by the view. Handles PropertyChanged events
    from the Model, writes, saves and reads the Model.

    Model - provides properties and methods to manage the underlying data for 
    the model domain, independent of the ViewModel. Provides read, write, and 
    save methods to persist the model.
    '''
    #region MainATViewModel Class
    #-------------------------------------------------------------------------+
    def __init__(self, atv: atview.ATView = None):
        self._activity_store_uri: str = AT_DEFAULT_ACTIVITY_STORE_URI 
        self._atview: atview.ATView = atv # Reference to the View object for AT.
        logger.debug(f"{p} MainATViewModel initialized with atv: {self._atview}")

    @property
    def activity_store_uri(self):
        return self._activity_store_uri
    
    @activity_store_uri.setter
    def activity_store_uri(self, value):
        self._activity_store_uri = value

    @property
    def atview(self):
        return self._atview
    
    @atview.setter
    def atview(self, value):
        self._atview = value

    #endregion MainATViewModel Class
    #-------------------------------------------------------------------------+
