#-----------------------------------------------------------------------------+
# file_atmodel.py
import getpass, json, pathlib
from abc import ABC, abstractmethod
from typing import List
import at_utilities.at_utils as atu
from model.ae import ActivityEntry
from model.base_atmodel.atmodel import ATModel
from model.atmodelconstants import TE_DEFAULT_DURATION, \
    TE_DEFAULT_DURATION_SECONDS, FATM_DEFAULT_ACTIVITY_STORE_URI

class FileATModel(ATModel):
    #region FileATModel Class doc string
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
    #endregion FileATModel Class doc string
    #region FileATModel attributes
    # Note: Using ATModel as an abstract base class ATModel, requires
    # the abstract property method implementation. Hence, each attribute
    # is defined as a @property and @property.setter method using the
    # private underscore convention.
    #--------------------------------------------------------------------------+
    # FileATModel class constructor __init__() method
    #--------------------------------------------------------------------------+
    def __init__(self,  activityname: str = None, 
                        activities: List[ActivityEntry] = None,
                        created_date: str = None,
                        last_modified_date: str = None,
                        modified_by: str = None,
                        activity_store_uri: str = None) -> None:
        # Private Property attributes initialization
        # Do some validation of the input parameters with defaults assigned
        self._activityname = atu.str_or_none(activityname)
        self._activities = FileATModel.valid_activities_list(activities)
        self._created_date = atu.timestamp_str_or_default(created_date)
        self._last_modified_date = \
            atu.stop_str_or_default(last_modified_date,self.created_date)
        self._modified_by = modified_by \
            if atu.str_notempty(modified_by) else getpass.getuser()
        self._activity_store_uri = activity_store_uri \
            if atu.str_notempty(activity_store_uri) else FATM_DEFAULT_ACTIVITY_STORE_URI
        # Public Property attributes initialization
    #--------------------------------------------------------------------------+

    def to_dict(self):
        '''Return self FileATModel object as a dictionary, with the activities
        list converted to a list of dictionaries for each ActivityEntry obj.'''
        ret = {
            "activityname": self.activityname,
            "activities": [ae.to_dict() for ae in self.activities],
            "created_date": self.created_date,
            "last_modified_date": self.last_modified_date,
            "modified_by": self.modified_by,
            "activity_store_uri": self.activity_store_uri
        }
        return ret

    def __repr__(self) -> str:
        ''' Return a string representation of the FileATModel object '''
        ret = f"FileATModel(activityname='{self.activityname}', "
        ret += f"activities=[{', '.join([repr(ae) for ae in self.activities])}], "
        ret += f"created_date='{self.created_date}', "
        ret += f"last_modified_date='{self.last_modified_date}', "
        ret += f"modified_by='{self.modified_by}', "
        ret += f"activity_store_uri='{self.activity_store_uri}')"
        return ret
    
    def __str__(self) -> str:
        """ Return a string representation of the FileATModel object """
        ret = f"FileATModel(activityname='{self.activityname}', "
        ret += f"activities=[{', '.join([str(ae) for ae in self.activities])}], "
        ret += f"created_date='{self.created_date}', "
        ret += f"last_modified_date='{self.last_modified_date}', "
        ret += f"modified_by='{self.modified_by}', "
        ret += f"activity_store_uri='{self.activity_store_uri}')"
        return ret
    #endregion FileATModel Class  

    #--------------------------------------------------------------------------+
    #region ATModel Properties (from ATModel abstract base class)
    #--------------------------------------------------------------------------+
    @property
    def activityname(self) -> str:
        return self._activityname
    
    @activityname.setter
    def activityname(self, value: str) -> None:
        self._activityname = value

    @property
    def activities(self) -> List[ActivityEntry]:
        return self._activities
    
    @activities.setter
    def activities(self, value: List[ActivityEntry]) -> None:
        self._activities = value

    @property
    def created_date(self) -> str:
        return self._created_date
    
    @created_date.setter
    def created_date(self, value: str) -> None:
        self._created_date = value

    @property
    def last_modified_date(self) -> str:
        return self._last_modified_date
    
    @last_modified_date.setter
    def last_modified_date(self, value: str) -> None:
        self._last_modified_date = value

    @property
    def modified_by(self) -> str:
        return self._modified_by
    
    @modified_by.setter
    def modified_by(self, value: str) -> None:
        self._modified_by = value

    @property
    def activity_store_uri(self) -> str:
        return self._activity_store_uri
    
    @activity_store_uri.setter
    def activity_store_uri(self, value: str) -> None:
        self._activity_store_uri = value
    #endregion

    #--------------------------------------------------------------------------+
    #region FileATModel Properties (specific to FileATModel class)
    #--------------------------------------------------------------------------+
    # tbd
    #endregion

    #--------------------------------------------------------------------------+
    #region ATModel Methods (from ATModel abstract base class)
    #--------------------------------------------------------------------------+
    def add_activity(self, ae: ActivityEntry) -> ActivityEntry:
        """ FileATModel.add_activity() - concrete impl for ABC method, 
            add an ActivityEntry to the activities list"""
        self.activities.append(ae)
        self.modified_by = getpass.getuser()
        self.last_modified_date = atu.current_timestamp()
        return ae

    def put_atmodel(self, activity_store_uri:str = None) -> bool:
        """ Save the current activity model to a .json file """
        # activity_store_uri is the pathname to a file and must be a str.
        # If activity_store_uri is None or "", the default filename is used.
        # Raises TypeError as appropriate.
        with open(self.validate_activity_store_uri(activity_store_uri), 'w') as file:
            json.dump(self.to_dict(), file, indent=4)
        return True

    def get_atmodel(self, activity_store_uri:str) -> None:
        """ Gets and populates values from a .json file store.
            For FileATModel, activity_store_uri is a pathname to a file. 
            Input activity_store_uri is first validated. Raises TypeError.
        """
        # activity_store_uri is the pathname to a file and must be a str.
        # If activity_store_uri is None or "", the default filename is used.
        # Raises ValueError or TypeError as appropriate.
        with open(self.validate_activity_store_uri(activity_store_uri), 'r') as file:
            data = json.load(file)
            self.activityname = data['activityname']
            self.activities = [ActivityEntry(**ae) for ae in data['activities']]
            self.created_date = data['created_date']
            self.last_modified_date = data['last_modified_date']
            self.modified_by = data['modified_by']
            self.activity_store_uri = data['activity_store_uri'] 

    def validate_activity_store_uri(self, activity_store_uri:str) -> pathlib.Path:
        """ Validate the provided activity activity_store_uri.
            Input of None, or "" are convereted to default uri.
            Input str values are converted to a pathlib.Path object.
            Raises TypeError for other types of input.
        """
        my_fp = activity_store_uri
        if my_fp is None:
            my_fp = pathlib.Path(FATM_DEFAULT_ACTIVITY_STORE_URI)
        if isinstance(my_fp, str) and len(my_fp) == 0 : 
            my_fp = pathlib.Path(FATM_DEFAULT_ACTIVITY_STORE_URI)
        if isinstance(my_fp, str):
            my_fp = pathlib.Path(my_fp)
        if isinstance(my_fp, pathlib.Path): return my_fp
        # Must be some other type
        t = type(my_fp).__name__
        rt = type(pathlib.Path).__name__
        m = f"activity_store_uri must be type:'{rt}', not type:'{t}'"
        raise TypeError(m)
    #endregion

    #--------------------------------------------------------------------------+
    #region FileATModel Methods (specific to FileATModel class)
    #--------------------------------------------------------------------------+
    @staticmethod
    def default_creation_date() -> str:
        """ Return the current date and time as a ISO format string """
        return atu.now_iso_date_string()
    #endregion

    @staticmethod
    def valid_activities_list(al : List[ActivityEntry]) -> List[ActivityEntry]:
        """
        Validate the input activities list, ensuring each entry is an 
        ActivityEntry instance or the list is empty.
        Returns the validated list or raises TypeError or ValueError 
        if validation fails.
        """
        if al is None: return []
        if not isinstance(al, list):
            raise TypeError("activities must be a list of ActivityEntry instances")
        if len(al) == 0:
            # Allow empty list, return it as valid
            return al
        for ae in al:
            if not isinstance(ae, ActivityEntry):
                raise ValueError(f"Expected ActivityEntry instance, got {type(ae).__name__}")
        return al
    #--------------------------------------------------------------------------+

