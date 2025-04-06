#-----------------------------------------------------------------------------+
from abc import ABC, abstractmethod


class ATViewModel(ABC):
    '''ATViewModel is an abstract base class for the ViewModel of the 
    Activity Tracker application. It defines the interface for any concrete
    subclass with additional specialization.

    PROPERTY ATTRIBUTES
    -------------------
    activity_store_uri : str
        The URI to the JSON document containing the Activity Model data for 
        the user. This is a user-aware value from the Domain Model of the 
        application. It is meant to be independent of the ViewModel and View 
        particular bindings beyond the ViewModel but is name of where the data 
        is accessed.
    '''
    #--------------------------------------------------------------------------+
    #region ATViewModel Abstract Properties 
    #--------------------------------------------------------------------------+
    @property
    @abstractmethod
    def activity_store_uri(self) -> str:
        raise NotImplementedError
    
    @activity_store_uri.setter
    @abstractmethod
    def activity_store_uri(self, value) -> None:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def initialized(self) -> bool:
        raise NotImplementedError
    #endregion ATViewModel Abstract Properties 
    #--------------------------------------------------------------------------+
    #region ATViewModel Abstract Methods 
    @abstractmethod
    def initialize(self) -> None:
        '''
        Initialize the ViewModel, typically called after the View is set.'''
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        '''Stop and cleanup the ViewModel, stopping any background threads.'''
        raise NotImplementedError
    #endregion ATViewModel Abstract Methods 
    #--------------------------------------------------------------------------+
    

