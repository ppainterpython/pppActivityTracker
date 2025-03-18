#-----------------------------------------------------------------------------+
import getpass, pytest
import at_utilities.at_utils as atu
from model.atmodelconstants import TE_DEFAULT_DURATION, TE_DEFAULT_DURATION_SECONDS
from model.ae import ActivityEntry
from model.file_atmodel import FileATModel

#region test_atmodel_constructor()
def test_atmodel_constructor():
    """Test the constructor for FileATModel class"""
    an = "painterActivity"
    am = FileATModel(an)
    un = getpass.getuser()
    assert am.activityname == an
    assert am.activities == [], "activities should be empty list"
    assert ActivityEntry.validate_iso_date_string(am.created_date), \
        f"created_date is not a valid ISO date string:{am.created_date}"
    assert ActivityEntry.validate_iso_date_string(am.last_modified_date), \
        f"last_modified_date is not a valid ISO date string:{am.last_modified_date}"
    assert am.modified_by == getpass.getuser(), "modified_by should be the current user"
    assert am.__str__() == f"ActivityEntry(activityname='{an}')", "String representation of FileATModel is incorrect"
    print(f"ActivityEntry.__str__() = {am}")
#endregion

def test_atmodel_add_activity():
    """Test the add_activity method for FileATModel class"""
    """This test creates three ActivityEntry objects and adds them to the FileATModel instance."""
    an = "painterActivity"
    # TODO: ae1.duration is float hours, but dur is minutes.
    dur : int = FileATModel.default_duration() # minutes
    start1 = atu.iso_date_now_string()
    start2 = atu.increase_time(start1, minutes=(dur + 1)) # duration + 1 min later
    start3 = atu.increase_time(start2, minutes=(dur + 1)) # duration + 1 min later
    stop1 = atu.increase_time(start1, minutes=dur)
    stop2 = atu.increase_time(start2, minutes=dur)
    stop3 = atu.increase_time(start3, minutes=dur)
    activity1 = "ae1 activity"
    activity2 = "ae2 activity"
    activity3 = "ae3 activity"

    ae1 = ActivityEntry(start=start1, stop=stop1, activity=activity1)
    assert ae1 is not None, "create activity ae1 __init__ failed!"
    assert ae1.start == start1, "ae1.start value is incorrect"
    assert ae1.duration == dur, "ae1 duration is incorrect"
    assert str(ae1) == activity1, "String representation of ActivityEntry ae1 is not correct"

    ae2 = ActivityEntry(start=start2, stop=stop2, activity=activity2)
    assert ae2 != None, "create activity entry start2 failed!"
    assert ae2.start == start2, "ae2.start value is incorrect"
    assert ae2.duration == dur, "ae2 duration is incorrect"
    assert str(ae2) == activity2, "String representation of ActivityEntry ae2 is not correct"

    ae3 = ActivityEntry(start=start3, stop=stop3, activity=activity3)
    assert ae3 != None, "create activity entry start3 failed!"
    assert ae3.start == start3, "ae3.start value is incorrect"
    assert ae3.duration == dur, "ae3 duration is incorrect"
    assert str(ae3) == activity3, "String representation of ActivityEntry ae3 is not correct"

    atm = FileATModel(an)
    assert atm != None, "creating ATModel instance faile"

    atm.add_activity(ae1)
    assert len(atm.activities) == 1, "add_activity failed to add ae1 object to activites"
    atm.add_activity(ae2)
    assert len(atm.activities) == 2, "add_activity failed to add ae2 object to activites"
    atm.add_activity(ae3)
    assert len(atm.activities) == 3, "add_activity failed to add ae3 object to activites"

    atm.save_atmodel("test.json", "test.json")
