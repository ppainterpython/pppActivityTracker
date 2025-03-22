#-----------------------------------------------------------------------------+
import getpass, pathlib, logging
import at_utilities.at_utils as atu
from model.atmodelconstants import TE_DEFAULT_DURATION, TE_DEFAULT_DURATION_SECONDS
from model.ae import ActivityEntry
from model.base_atmodel.atmodel import ATModel
from model.file_atmodel import FileATModel
from model.file_atmodel import FATM_DEFAULT_FILENAME

FATM_TEMPDATA_DIR = "tests/tempdata"
FATM_FILENAME = "activity.json"  # default filename for saving

# Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


#region test_atmodel_constructor()
def test_atmodel_constructor():
    """Test the constructor for FileATModel class"""
    an = "painterActivity"
    am = FileATModel(an)
    un = getpass.getuser()
    assert am.activityname == an
    assert am.activities == [], "activities should be empty list"
    assert atu.validate_iso_date_string(am.created_date), \
        f"created_date is not a valid ISO date string:{am.created_date}"
    assert atu.validate_iso_date_string(am.last_modified_date), \
        f"last_modified_date is not a valid ISO date string:{am.last_modified_date}"
    assert am.modified_by == getpass.getuser(), "modified_by should be the current user"
    assert am.__str__() == f"ActivityEntry(activityname='{an}')", "String representation of FileATModel is incorrect"
#endregion

#region test_atmodel_default_filename()
def test_atmodel_add_activity():
    """Test the add_activity method for FileATModel class"""
    """This test creates three ActivityEntry objects, adds them to the 
    FileATModel instance, saves to a temp data file, and then reads
    the file back for comparison. Temporary files are placed in the 
    folder tests/tempdata"""
    logging.debug("Starting test_atmodel_add_activity()")
    un = getpass.getuser()
    an = un + "_activity"
    # TODO: ae1.duration is float hours, but dur is minutes.
    default_dur_hours : float = atu.default_duration() # hours
    int_dur_minutes : int = int(default_dur_hours * 60) # convert to minutes
    start1 = atu.now_iso_date_string()
    start2 = atu.increase_time(start1, minutes=(int_dur_minutes + 1)) # duration + 1 min later
    start3 = atu.increase_time(start2, minutes=(int_dur_minutes + 1)) # duration + 1 min later
    stop1 = atu.increase_time(start1, minutes=int_dur_minutes)
    stop2 = atu.increase_time(start2, minutes=int_dur_minutes)
    stop3 = atu.increase_time(start3, minutes=int_dur_minutes)
    activity1 = "ae1 activity"
    activity2 = "ae2 activity"
    activity3 = "ae3 activity"

    ae1 = ActivityEntry(start=start1, stop=stop1, activity=activity1)
    assert ae1 is not None, "create activity ae1 __init__ failed!"
    assert ae1.start == start1, "ae1.start value is incorrect"
    assert ae1.duration == default_dur_hours, "ae1 duration is incorrect"
    assert str(ae1) == activity1, "String representation of ActivityEntry ae1 is not correct"

    ae2 = ActivityEntry(start=start2, stop=stop2, activity=activity2)
    assert ae2 != None, "create activity entry start2 failed!"
    assert ae2.start == start2, "ae2.start value is incorrect"
    assert ae2.duration == default_dur_hours, "ae2 duration is incorrect"
    assert str(ae2) == activity2, "String representation of ActivityEntry ae2 is not correct"

    ae3 = ActivityEntry(start=start3, stop=stop3, activity=activity3)
    assert ae3 != None, "create activity entry start3 failed!"
    assert ae3.start == start3, "ae3.start value is incorrect"
    assert ae3.duration == default_dur_hours, "ae3 duration is incorrect"
    assert str(ae3) == activity3, "String representation of ActivityEntry ae3 is not correct"

    assert (atm := FileATModel(an)) is not None, "creating FileATModel instance failed"
    assert isinstance(atm, FileATModel), \
        f"FileATModel() returned type:'{type(atm).__name__}' "
    assert isinstance(atm, ATModel), \
        f"FileATModel() returned type:'{type(atm).__name__}' "

    assert atm.add_activity(ae1) is not None
    assert len(atm.activities) == 1, \
        "add_activity() failed to add 1st ActivityEntry instance to activites"
    assert atm.add_activity(ae2) is not None
    assert len(atm.activities) == 2, \
        "add_activity() failed to add 2nd ActivityEntry instance to activites"
    assert atm.add_activity(ae3) is not None
    assert len(atm.activities) == 3, \
        "add_activity() failed to add 3rd ActivityEntry instance to activites"

    # Save the created FATM object with 3 activities to a file using FileATModel.
    folder_path = pathlib.Path(FATM_TEMPDATA_DIR)
    file_name = FATM_FILENAME
    full_path = folder_path / file_name
    full_path.parent.mkdir(parents=True, exist_ok=True)
    assert atm.put_atmodel(full_path) is True, \
        f"put_atmodel failed to save to file {full_path}"

    # Read the file back into a new FileATModel instance
    new_atm = FileATModel(an)
    assert new_atm is not None, "creating FileATModel instance failed"
    assert new_atm.get_atmodel(full_path) is None, \
        f"get_atmodel failed to load from file {full_path}"
    
    # Validate the new_atm object
    assert new_atm.activityname == an, \
        f"get_atmodel activityname is incorrect: {new_atm.activityname}"
    assert len(new_atm.activities) == 3, \
        f"get_atmodel activities length is incorrect: {len(new_atm.activities)}"
    assert new_atm.activities[0].activity == ae1.activity, \
        f"get_atmodel activities[0] activity is incorrect: {new_atm.activities[0].activity}"
    assert new_atm.activities[1].activity == ae2.activity, \
        f"get_atmodel activities[1] activity is incorrect: {new_atm.activities[1].activity}"
    assert new_atm.activities[2].activity == ae3.activity, \
        f"get_atmodel activities[2] activity is incorrect: {new_atm.activities[2].activity}"
    assert new_atm.activities[0].start == ae1.start, \
        f"get_atmodel activities[0] start time is incorrect: {new_atm.activities[0].start}" 
    assert new_atm.activities[1].start == ae2.start, \
        f"get_atmodel activities[1] start time is incorrect: {new_atm.activities[1].start}"
    assert new_atm.activities[2].start == ae3.start, \
        f"get_atmodel activities[2] start time is incorrect: {new_atm.activities[2].start}"
    assert new_atm.activities[0].stop == ae1.stop, \
        f"get_atmodel activities[0] stop time is incorrect: {new_atm.activities[0].stop}"
    assert new_atm.activities[1].stop == ae2.stop, \
        f"get_atmodel activities[1] stop time is incorrect: {new_atm.activities[1].stop}"
    assert new_atm.activities[2].stop == ae3.stop, \
        f"get_atmodel activities[2] stop time is incorrect: {new_atm.activities[2].stop}"
    assert new_atm.activities[0].duration == ae1.duration, \
        f"get_atmodel activities[0] duration is incorrect: {new_atm.activities[0].duration}"
    assert new_atm.activities[1].duration == ae2.duration, \
        f"get_atmodel activities[1] duration is incorrect: {new_atm.activities[1].duration}"
    assert new_atm.activities[2].duration == ae3.duration, \
        f"get_atmodel activities[2] duration is incorrect: {new_atm.activities[2].duration}"
    assert new_atm.created_date == atm.created_date, \
        f"get_atmodel created_date is incorrect: {new_atm.created_date}"
    assert new_atm.last_modified_date == atm.last_modified_date, \
        f"get_atmodel last_modified_date is incorrect: {new_atm.last_modified_date}"
    assert new_atm.modified_by == atm.modified_by, \
        f"get_atmodel modified_by is incorrect: {new_atm.modified_by}"
    assert new_atm.modified_by == un, \
        f"get_atmodel modified_by is incorrect: {new_atm.modified_by}"
    assert new_atm.__str__() == atm.__str__(), \
        f"get_atmodel string representation is incorrect: {new_atm.__str__()}"
    assert new_atm.__str__() == f"ActivityEntry(activityname='{an}')", \
        "String representation of FileATModel is incorrect"
    # Clean up the temporary file
    try:
        full_path.unlink()
    except Exception as e:
        logging.error(f"Failed to delete file {full_path}: {e}")
        raise
    logging.debug("Completed test_atmodel_add_activity()")
#endregion
#-----------------------------------------------------------------------------+
