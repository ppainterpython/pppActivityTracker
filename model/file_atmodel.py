#-----------------------------------------------------------------------------+
# file_atmodel.py
import getpass, json
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
from typing import List
import at_utilities.at_utils as atu
from model.ae import ActivityEntry
from model.base_atmodel.atmodel import ATModel
from model.atmodelconstants import TE_DEFAULT_DURATION, TE_DEFAULT_DURATION_SECONDS

@dataclass(kw_only=True)
class FileATModel(ATModel):
    """
    A class to represent the complete Activity Tracking model for a user.
    FileATModel is a concrete implementation of base abstract class ATModel.
    A simple file system .json file is used to persist the activity model
    data. Additional Properties and Methods are included to support the
    local File System functions.

    ATModel Properties (from ATModel abstract base class)
    -----------------------------------------------------
    activityname : str
        A string identifying a set of activity data for a the user
    activities : List[ActivityEntry]
        A List of ActivityEntry instances, one for each activity sorted in
        sequential order by start time.
    created_date : str
        ISO format timestamp string for the activity model was created
    last_modified_date : str
        ISO format timestamp string for the last modification
    modified_by : str
        The username to last modify the content

    FileATModel Properties (specific to FileATModel class)
    ------------------------------------------------------

    ATModel Methods (from ATModel abstract base class)
    --------------------------------------------------
    add_activity(ae : ActivityEntry) -> ActivityEntry
        adds the provided ActivityEntry instance to the activities List,
        returns ae upon success, None otherwise

    FileATModel Methods (specific to FileATModel class)
    ---------------------------------------------------

    """
    #region FileATModel Class
    #-------------------------------------------------------------------------+
    # Private Property attributes
    #-------------------------------------------------------------------------+
    # For ATModel abstract base class property values
    __activityname: str = ""
    __activities: List[ActivityEntry]
    __created_date: str = None
    __last_modified_date: str = None
    __modified_by: str = ""
    # For FileATModel sub-class property values
    __filename: str = "activity-tracking.json"  # default filename for saving
    __folderpath: str = "."  # default folder path for saving
    #-------------------------------------------------------------------------+
    # class constructor
    #-------------------------------------------------------------------------+
    def __init__(self, an: str):
        """Constructor for class FileATModel"""
        self.__activityname = an
        self.__activities = []
        self.__created_date = FileATModel.default_creation_date()
        self.__last_modified_date = self.__created_date
        self.__modified_by = getpass.getuser()        

    def __str__(self):
        return f"ActivityEntry(activityname='{self.__activityname}')"
    #endregion FileATModel Class  

    #-------------------------------------------------------------------------+
    #region ATModel Properties (from ATModel abstract base class)
    #-------------------------------------------------------------------------+
    @property
    def activityname(self) -> str:
        return self.__activityname
    
    @activityname.setter
    def activityname(self, value: str) -> None:
        self.__activityname = value

    @property
    def activities(self) -> List[ActivityEntry]:
        return self.__activities
    
    @activities.setter
    def activities(self, value: List[ActivityEntry]) -> None:
        self.__activities = value

    @property
    def created_date(self) -> str:
        return self.__created_date
    
    @created_date.setter
    def created_date(self, value: str) -> None:
        self.__created_date = value

    @created_date.setter
    def created_date(self, value: str) -> str:
        return self.__created_date

    @property
    def last_modified_date(self) -> str:
        return self.__last_modified_date
    
    @last_modified_date.setter
    def last_modified_date(self, value: str) -> None:
        self.__last_modified_date = value

    @property
    def modified_by(self) -> str:
        return self.__modified_by
    
    @modified_by.setter
    def modified_by(self, value: str) -> None:
        self.__modified_by = value
    #endregion

    #-------------------------------------------------------------------------+
    #region FileATModel Properties (specific to FileATModel class)
    #-------------------------------------------------------------------------+
    @property
    def filename(self) -> str:
        return self.__filename
    
    @filename.setter
    def filename(self, value: str) -> None:
        self.__filename = value

    @property
    def folderpath(self) -> str:
        return self.__folderpath
    
    @folderpath.setter
    def folderpath(self, value: str) -> None:
        self.__folderpath = value
    #endregion

    #-------------------------------------------------------------------------+
    #region ATModel Methods (from ATModel abstract base class)
    #-------------------------------------------------------------------------+
    def add_activity(self, ae: ActivityEntry) -> ActivityEntry:
        """ FileATModel.add_activity() - concrete impl for ABC method, 
            add an ActivityEntry to the activities list"""
        self.__activities.append(ae)
        self.__modified_by = getpass.getuser()
        self.__last_modified_date = atu.current_timestamp()
        return ae
    #endregion

    #-------------------------------------------------------------------------+
    #region FileATModel Methods (specific to FileATModel class)
    #-------------------------------------------------------------------------+
    def save_atmodel(self, fp:str,fn:str) -> None:
        """ Save the current activity model to a .json file """
        with open(fp, 'w') as f:
            data = asdict(self)
            json.dump(data, f, indent=4)

    @staticmethod
    def default_creation_date() -> str:
        """ Return the current date and time as a ISO format string """
        return atu.now_iso_date_string()

    #endregion

