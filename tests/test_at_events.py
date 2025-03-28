import pytest, threading
from at_utilities import at_events as atev

#region test_iso_date_string()
def test_at_event_manager():
    """Test the ATEventManager."""
    myEM = atev.ATEventManager()
    # Assert that there are no queues in the new event manager
    assert len(myEM.event_queues) == 0, \
        "New ATEventManager object not created."
    # Assert that the signal event is created
    assert  isinstance(myEM.signal_event,threading.Event), \
        "Signal event not created."
    # Test adding event queues for two different event types
    assert myEM.add_event_queue("test_event_type"), \
        "Event queue not added to event manager."
    assert not myEM.add_event_queue("test_event_type"), \
        "Second add_event_queue() returned True."
    assert myEM.add_event_queue(atev.ATViewEvent.__name__), \
        "Event queue not added to event manager."
    assert not myEM.add_event_queue(atev.ATViewEvent.__name__), \
        "Second add_event_queue() returned True."
    
    # Test creating some ATEvnet objects
    assert (e1 := atev.ATViewEvent("test_event_type", "test_event_data")), \
        "ATEvnet(\"test_event_type\") object not created."
    assert (e2 := atev.ATViewEvent(atev.ATViewEvent.__name__, "test_event_data")), \
        f"ATEvnet()\"{atev.ATViewEvent.__name__}\" object not created."
    
    # Test publishing events to the event manager
    myEM.publish_event(e1)
    myEM.destroy()

    # Test with invalid type of input
    # with pytest.raises(TypeError) : atu.iso_date_string(None)
#endregion

