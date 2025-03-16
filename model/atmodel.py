#-----------------------------------------------------------------------------+
# ae.py
import datetime
import getpass
from dataclasses import dataclass, field
from typing import List
from model.ae import ActivityEntry

@dataclass(kw_only=True)
class ATModel:
    """
    A class to represent the complete Activity Tracking model for a user.

    Attributes
    ----------
    activityname : str
        A string identifying a set of activity data for a the user

    """
    activityname: str = ""
    activities: List[ActivityEntry]
    created_date: datetime = None
    last_modified_date: datetime = None
    modified_by: str = ""
    def __init__(self, an: str):
        """Constructor for class ATModel
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

