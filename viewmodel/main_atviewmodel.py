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
from at_utilities.at_events import ATEventManager, ATEvent
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
    #--------------------------------------------------------------------------+
    #region MainATViewModel Class
    #--------------------------------------------------------------------------+
    #region __init__() method
    def __init__(self, atv: atview.ATView = None):
        self._activity_store_uri: str = AT_DEFAULT_ACTIVITY_STORE_URI 
        self._atview: atview.ATView = atv # Reference to the View object for AT.
        self._atem: ATEventManager = None # Event manager for this ViewModel.
        self._initialized: bool = False # Track if initialize() has been called.
        logger.debug(f"{p} MainATViewModel initialized with atv: {self._atview}")
    #endregion __init__() method
    #--------------------------------------------------------------------------+
    #region MainATViewModel Properties (from ATViewModel abstract base class)
    #--------------------------------------------------------------------------+
    @property
    def activity_store_uri(self):
        return self._activity_store_uri
    
    @activity_store_uri.setter
    def activity_store_uri(self, value):
        self._activity_store_uri = value

    @property
    def initialized(self) -> bool:
        return self._initialized
    
    #endregion MainATViewModel Properties (from ATViewModel abstract base class)
    #--------------------------------------------------------------------------+
    #region MainATViewModel Properties (specific to MainATViewModel class)
    #--------------------------------------------------------------------------+
    @property
    def atview(self):
        return self._atview
    
    @atview.setter
    def atview(self, value):
        self._atview = value

    #endregion MainATViewModel Properties (specific to MainATViewModel class)
    #--------------------------------------------------------------------------+
    #region MainATViewModel Methods (from ATViewModel abstract base class)

    #region initialize() method
    def initialize(self):
        """
        Initialize the MainATViewModel, typically called after the View is set.
        This can be used to initialize the event manager or other properties.
        """
        if self._atem is None:
            self._atem = ATEventManager()
            self._atem.start()
        self._initialized = True
    #endregion initialize() method
    
    #region stop() method
    def stop(self) -> None:
        """
        Stop and cleanup the ViewModel, stopping any background threads.
        This method should be called when the ViewModel is no longer needed.
        """
        p = atu.pfx(mn=__name__)
        logger.debug(f"{p}Stopping MainATViewModel")
        if self._atem:
            self._atem.stop()
            self._atem = None
        self._initialized = False
        logger.debug(f"{p}MainATViewModel stopped")
    #endregion stop() method

    #region publish(self, event: ATEvent) method
    def publish(self, event: ATEvent) -> None:
        """
        Publish an event to the event manager if initialized.
        This allows the ViewModel to raise events to subscribers.
        """
        if self._atem and self._initialized:
            self._atem.publish(event)
        else:
            logger.warning(f"{p}Cannot publish event, ATEventManager not initialized.")
    #endregion MainATViewModel Methods (from ATViewModel abstract base class)
    #--------------------------------------------------------------------------+
    #endregion MainATViewModel Class
    #-------------------------------------------------------------------------+
