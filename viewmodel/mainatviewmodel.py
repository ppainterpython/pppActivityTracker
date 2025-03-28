#-----------------------------------------------------------------------------+
from viewmodel.base_atviewmodel.atviewmodel import ATViewModel
from view import atview


class MainATModel(ATViewModel):
    '''    MainATModel is a concrete subclass of ATModel, representing the
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
    #region MainATModel Class
    #-------------------------------------------------------------------------+
    activity_store_uri: str = "activities.json"
    atv: atview.ATView = None # Reference to the View object for AT.
    
    def __init__(self, atv: atview.ATView = None):
        self.atv = atv # Associate ViewModel with View

    @property
    def activity_store_uri(self):
        return self.activity_store_uri
    
    @activity_store_uri.setter
    def activity_store_uri(self, value):
        self.activity_store_uri = value

    #endregion MainATModel Class
    #-------------------------------------------------------------------------+
