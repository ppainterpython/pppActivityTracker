#-----------------------------------------------------------------------------+
# ae.py
import datetime
import getpass
from dataclasses import dataclass, field
from typing import List
from model.ae import ActivityEntry

@dataclass(kw_only=True)
class FileATModel:
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
    created_date : datetime
        The timestamp the activity model was created
    last_modified_date : datetime
        The timestamp of the last modification
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
    activityname: str = ""
    activities: List[ActivityEntry]
    created_date: datetime = None
    last_modified_date: datetime = None
    modified_by: str = ""
    def __init__(self, an: str):
        """Constructor for class FileATModel
        """
        self.activityname = an
        self.activities = []
        self.created_date = datetime.datetime.now()
        self.modified_by = self.created_date
        self.modified_by = getpass.getuser()        

    def __str__(self):
        return f"Activity: {self.activityname}"
    
    def add_activity(self, ae: ActivityEntry) -> ActivityEntry:
        self.activities.append(ae)
        self.modified_by = getpass.getuser()
        self.last_modified_date = datetime.datetime.now()
        return ae

