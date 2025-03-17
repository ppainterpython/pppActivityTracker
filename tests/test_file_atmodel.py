#-----------------------------------------------------------------------------+
import datetime
import os
import getpass
from typing import List
import pytest
import json
from model.ae import ActivityEntry
from model.atmodelconstants import TE_DEFAULT_DURATION
from model.file_atmodel import FileATModel

def test_atmodel_constructor():
    an = "painterActivity"
    am = FileATModel(an)
    un = getpass.getuser()
    assert am.activityname == an
    assert am.activities == [], "activities should be empty list"
    assert isinstance(am.created_date, datetime.datetime), "created_date should be a datetime object"
    assert isinstance(am.last_modified_date, datetime.datetime), "last_modified_date should be a datetime object"
    assert am.modified_by == getpass.getuser(), "modified_by should be the current user"
    assert am.__str__() == f"ActivityEntry(activityname='{an}')", "String representation of FileATModel is incorrect"
    print(f"ActivityEntry.__str__() = {am}")

def test_atmodel_add_activity():
    an = "painterActivity"
    dur = datetime.timedelta(minutes=TE_DEFAULT_DURATION)
    onemin = datetime.timedelta(minutes=1)
    start1 = datetime.datetime.now()
    start2 = start1 + dur + onemin # duration + 1 min later
    start3 = start2 + dur + onemin # duration + 1 min later
    stop1 = start1 + dur
    stop2 = start2 + dur
    stop3 = start3 + dur
    activity1 = "ae1 activity"
    activity2 = "ae2 activity"
    activity3 = "ae3 activity"
    ae1 = ActivityEntry(start=start1, stop=stop1, activity=activity1)
    assert ae1 != None, "create activity entry start1 failed!"
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

