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

    #--------------------------------------------------------------------------+
    #region ActivyEntery Class
    # constructor for ActivityEntry class
    def __init__(self, start:str=None, stop:str=None, activity:str=None,
                 notes:str=None):
        """Constructor for class ActivityEntry
        
        Parameters
        ----------
        start : str
            ISO format date and time an activity starts. If none, current time is used
        stop : str
            ISO format date and time an activity stops. If none, current time is used
        activity : str
        notes : str
        """
        self._start: str = atu.validate_start(start)
        self._stop: str = atu.validate_stop(self.start, stop)
        self._activity: str = activity
        self._notes: str = notes
        self._duration: float = atu.calculate_duration(self.start, self.stop)

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
        self.start: str = atu.validate_start(self.start)
        self.stop: str = atu.validate_stop(self.start, self.stop)
        activity: str = ''
        notes: str = ''
        self.duration: float = atu.calculate_duration(self.start, self.stop) # duration in hours as float
                                               
    def __str__(self):
        return f"{self.activity}"
    #endregion
    #--------------------------------------------------------------------------+
    #region ActivityEntry Properties
    @property
    def start(self) -> str:
        return self._start
    @start.setter
    def start(self, value: str) -> None:
        self._start = atu.validate_start(value)
    @property
    def stop(self) -> str:
        return self._stop
    @stop.setter
    def stop(self, value: str) -> None:
        self._stop = atu.validate_stop(self.start, value)
    @property
    def activity(self) -> str:
        return self._activity
    @activity.setter
    def activity(self, value: str) -> None:
        self._activity = value
    @property
    def notes(self) -> str:
        return self._notes
    @notes.setter
    def notes(self, value: str) -> None:
        self._notes = value
    @property
    def duration(self) -> float:
        return self._duration
    @duration.setter
    def duration(self, value: float) -> None:
        self._duration = atu.calculate_duration(self.start, self.stop)
    #endregion
    #--------------------------------------------------------------------------+
