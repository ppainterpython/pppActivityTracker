#-----------------------------------------------------------------------------+
import datetime
from abc import ABC, abstractmethod
from typing import List
from model.ae import ActivityEntry

class ATModel(ABC):
    """
    A class to represent the complete Activity Tracking model for a user.
    ATModel is a base abstract class, representing the Interface for any 
    concrete subclass with additional specialization.

    Properties
    ----------
    activityname : str
        A string identifying a set of activity data for a the user
    activities : List[ActivityEntry]
        A List of ActivityEntry instances, one for each activity sorted in
        sequential order by start time.
    created_date : datetime
        The timestamp the activity model was created
    last_modified_date : datetime
        The timestamp of the last modification
    modified_by : str
        The username to last modify the content

    Methods
    -------
    add_activity(ae : ActivityEntry) -> ActivityEntry
        adds the provided ActivityEntry instance to the activities List,
        returns ae upon success, None otherwise
    """

    @property
    @abstractmethod
    def activityname(self) -> str:
        raise NotImplementedError
    
    @activityname.setter
    @abstractmethod
    def activityname(self, value: str) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def activities(self) -> List[ActivityEntry]:
        raise NotImplementedError
    
    @activities.setter
    @abstractmethod
    def activities(self, value: List[ActivityEntry]) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def created_date(self) -> datetime:
        raise NotImplementedError
    
    @created_date.setter
    @abstractmethod
    def created_date(self, value: datetime) -> None:
        raise NotImplementedError

    @created_date.setter
    @abstractmethod
    def created_date(self, value: datetime) -> datetime:
        raise NotImplementedError

    @property
    @abstractmethod
    def last_modified_date(self) -> datetime:
        raise NotImplementedError
    
    @last_modified_date.setter
    @abstractmethod
    def last_modified_date(self, value: datetime) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def modified_by(self) -> str:
        raise NotImplementedError
    
    @modified_by.setter
    @abstractmethod
    def modified_by(self, value: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_activity(self, ae: ActivityEntry) -> ActivityEntry:
        raise NotImplementedError

