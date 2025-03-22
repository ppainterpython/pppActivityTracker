#-----------------------------------------------------------------------------+
# file_atmodel.py
import getpass, json, pathlib
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
from typing import List
import at_utilities.at_utils as atu
from model.ae import ActivityEntry
from model.base_atmodel.atmodel import ATModel
from model.atmodelconstants import TE_DEFAULT_DURATION, TE_DEFAULT_DURATION_SECONDS

FATM_DEFAULT_FILENAME = "activity.json"  # default filename for saving

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
    activityname: str = ""
    activities: List[ActivityEntry]
    created_date: str = None
    last_modified_date: str = None
    modified_by: str = ""
    # For FileATModel sub-class property values
    filepath: str = "activity-tracking.json"  # default filepath for saving
    #-------------------------------------------------------------------------+
    # class constructor
    #-------------------------------------------------------------------------+
    def __init__(self, activityname, activities=None, created_date=None, \
                 last_modified_date=None, modified_by=None, filepath=None):
        self.activityname = activityname
        self.activities = activities if activities is not None else []
        self.created_date = created_date if created_date is not None else "2025-03-22T14:42:49.300051"
        self.last_modified_date = last_modified_date if last_modified_date is not None else "2025-03-22T14:42:49.301397"
        self.modified_by = modified_by if modified_by is not None else "ppain"
        self.filepath = filepath if filepath is not None else "activity-tracking.json"

    def to_dict(self):
        return {
            "activityname": self.activityname,
            "activities": self.activities,
            "created_date": self.created_date,
            "last_modified_date": self.last_modified_date,
            "modified_by": self.modified_by,
            "filename": self.filename,
            "folderpath": self.folderpath
        }

    def __str__(self):
        return f"ActivityEntry(activityname='{self.activityname}')"
    #endregion FileATModel Class  

    #-------------------------------------------------------------------------+
    #region ATModel Properties (from ATModel abstract base class)
    #-------------------------------------------------------------------------+
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
    #endregion

    #-------------------------------------------------------------------------+
    #region FileATModel Properties (specific to FileATModel class)
    #-------------------------------------------------------------------------+
    @property
    def filepath(self) -> str:
        return self._filepath
    
    @filepath.setter
    def filepath(self, value: str) -> None:
        self._filepath = value
    #endregion

    #-------------------------------------------------------------------------+
    #region ATModel Methods (from ATModel abstract base class)
    #-------------------------------------------------------------------------+
    def add_activity(self, ae: ActivityEntry) -> ActivityEntry:
        """ FileATModel.add_activity() - concrete impl for ABC method, 
            add an ActivityEntry to the activities list"""
        self.activities.append(ae)
        self.modified_by = getpass.getuser()
        self.last_modified_date = atu.current_timestamp()
        return ae

    def put_atmodel(self, filepath:str = None) -> bool:
        """ Save the current activity model to a .json file """
        # filepath is the pathname to a file and must be a str.
        # If filepath is None or "", the default filename is used.
        # Raises TypeError as appropriate.
        with open(self.validate_filepath(filepath), 'w') as file:
            data = asdict(self)
            data['activities'] = [asdict(ae) for ae in self.activities]
            json.dump(data, file, indent=4)
        return True

    def get_atmodel(self, filepath:str) -> None:
        """ Load the activity model from a .json file """
        # filepath is the pathname to a file and must be a str.
        # If filepath is None or "", the default filename is used.
        # Raises ValueError or TypeError as appropriate.
        with open(self.validate_filepath(filepath), 'r') as file:
            data = json.load(file)
            self.__activityname = data['activityname']
            self.activities = [ActivityEntry(**ae) for ae in data['activities']]
            self.created_date = data['created_date']
            self.last_modified_date = data['last_modified_date']
            self.modified_by = data['modified_by']

    def validate_filepath(self, filepath:str) -> pathlib.Path:
        """ Validate the provided activity filepath """
        my_fp = filepath
        if my_fp is None:
            my_fp = pathlib.Path(FileATModel.default_activity_filename())
        if isinstance(my_fp, str) and len(my_fp) == 0 : 
            my_fp = pathlib.Path(FileATModel.default_activity_filename())
        else:
            my_fp = pathlib.Path(my_fp)
        if not isinstance(my_fp, pathlib.Path):
            t = type(my_fp).__name__
            rt = type(pathlib.Path).__name__
            m = f"filepath must be type:'{rt}', not type:'{t}'"
            raise TypeError(m)
        return my_fp
    #endregion

    #-------------------------------------------------------------------------+
    #region FileATModel Methods (specific to FileATModel class)
    #-------------------------------------------------------------------------+
    @staticmethod
    def default_creation_date() -> str:
        """ Return the current date and time as a ISO format string """
        return atu.now_iso_date_string()

    #endregion

