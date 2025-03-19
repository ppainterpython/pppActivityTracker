#-----------------------------------------------------------------------------+
# ae.py
import at_utilities.at_utils as atu
from dataclasses import dataclass, field
from model.atmodelconstants import TE_DEFAULT_DURATION, TE_DEFAULT_DURATION_SECONDS

TE_DEFAULT_DURATION = 30 # minutes

@dataclass(kw_only=True)
class ActivityEntry:
    """
    A class to represent one entry of time spent doing some work.

    Attributes
    ----------
    start : str
        date and time an activity starts as ISO string format. 
    stop : str
        date and time an activity stops as ISO string format
    activity : str
        A unique activity identifier string, perhaps as a dictionary entry
        defining a list of activities that can be aggregated and summarized
    notes : str
        Additional descriptive text describing the particulars of this activity
    duration : float
        Calculated float difference between stop and start times in hours.
        Rationale for hours is that time tracking will use fractional hour
        amounts for line item task work.

    Data Validation at Construction
    ------------------------------
    Validate the input types for start and stop times
    and calculate the duration as a datetime.timedelta object.
    If the start or stop time are a string, it is be converted to a 
    datetime object assuming a valid ISO format datetime.
    Empty strings or 'None' values for start or stop are set to the current datetime.
    If no stop time is provided, it defaults to the start time plus 30 minutes.
    The duration is calculated as the difference between the stop and start 
    times in hours. A negative value indicates the stop time is before the start
    time. 
    """

    #-------------------------------------------------------------------------+
    #region ActivyEntery Class
    start: str = field(default=None)
    stop: str = field(default=None)
    activity: str = field(default='')
    notes: str = field(default='')
    duration: float = field(default=0.0) # duration in hours as float
    # post init function to validate start, stop and calculate duration
    def __post_init__(self):
        """Full parameters Constructor for class ActivityEntry
        
        Parameters
        ----------
        start : str
            ISO format date and time an activity starts. If none, current time is used
        stop : str
            ISO format date and time an activity stops. If none, current time is used
        activity : str
        notes : str
        """
        self.start = self.validate_start(self.start)
        self.stop = self.validate_stop(self.start, self.stop)
        self.duration = atu.calculate_duration(self.start, self.stop) # duration in hours as float
                                               
    def __str__(self):
        return f"{self.activity}"
    #endregion

    #-------------------------------------------------------------------------+
