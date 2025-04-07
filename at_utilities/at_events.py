#------------------------------------------------------------------------------+
'''
Module at_atevents contains classes for managing events in the
Activity Tracker application. The module contains classes for managing a 
queue of events, the events themselves, and a signal event to signal the
processing of the queue of events. The module also contains a singleton class 
for managing the event queues for the Activity Tracker application.

One background thread is used to process the event queue. The event queue is
a queue of ATEvent objects. The event queue is used to store events that 
are published from actors outside the queue owner. The event queue is
processed by the background thread. The background thread waits for an event 
to be published to the queue. When an event is published to the queue, the
background thread processes the event by calling the event's callback method.

This version uses a singleton event as a signal to process the event queue. The 
callback method for the event is called by the background thread when the event
is processed. The callback method is passed the event data as a parameter. The 
callback method is responsible for dispathching the call to appropriate
event handler functions.
TODO: Expand to multiple worker threads for each event type with its own queue 
and signal event callback method.
'''
import logging
from atconstants import *
from at_utilities.at_logging import atlogging_setup
import at_utilities.at_utils as atu
#------------------------------------------------------------------------------+
#region atlogging_setup()
# Setup logging for AT prior to importing the main application modules
logger = atlogging_setup(AT_APP_NAME)
logger.debug(f"Imported module: {__name__}")
logger.debug(f" Logging initialized.")
#endregion atlogging_setup()
#------------------------------------------------------------------------------+
import threading, queue
import at_utilities.at_utils as atu
from at_utilities import at_events as atev
 
#------------------------------------------------------------------------------+
#region class ATSignalEvent
class ATSignalEvent (threading.Event):
    '''
    ATEventSignal is a subclass of threading.Event. A ATSignalEvent is 
    is to signal processing of a queue of EventData objects.
    '''
    def __init__(self, event_type:str=None, event_name:str=None, signal_data:dict=None):
        super().__init__()
        self._event_type = event_type
        self._event_name = event_name
        self._signal_data : dict = signal_data

    @property
    def event_type(self):
        return self._event_type
    
    @event_type.setter
    def event_type(self, value):
        self._event_type = value

    @property
    def event_name(self):
        return self._event_name
    
    @event_name.setter
    def event_name(self, value):
        self._event_name = value

    @property
    def event_data(self):
        return self._event_data
    
    @event_data.setter
    def event_data(self, value):
        self._event_data = value

    def set(self):
        super().set()

    def clear(self):
        super().clear()

    def wait(self, timeout=None):
        return super().wait(timeout)
#endregion class ATSignalEvent
#------------------------------------------------------------------------------+
        
#------------------------------------------------------------------------------+
#region class ATEvent
class ATEvent ():
    '''
    ATEvent is a simple object used to contain data of a published event.
    '''
    def __init__(self, event_name:str=None, event_data:dict=None):
        # super().__init__()

        # Instance variables
        self._event_name = event_name
        self._event_data : dict = event_data

    @property
    def event_name(self):
        return self._event_name
    
    @event_name.setter
    def event_name(self, value):
        self._event_name = value

    @property
    def event_data(self):
        return self._event_data
    
    @event_data.setter
    def event_data(self, value):
        self._event_data = value

    #region future
    # def set(self):
    #     super().set()

    # def clear(self):
    #     super().clear()

    # def wait(self, timeout=None):
    #     return super().wait(timeout)
    #endregion future
#endregion class ATEvent
#------------------------------------------------------------------------------+
#region class ATViewEvent
class ATViewEvent(ATEvent):
    '''Event class for events published by the AT View.'''
    def __init__(self, event_name = None, event_data = None):
        super().__init__(event_name, event_data)
#endregion class ATViewEvent        
#------------------------------------------------------------------------------+
#region class ATViewModelEvent
class ATViewModelEvent(ATEvent):
    '''Event class for events published by the AT View.'''
    def __init__(self, event_name = None, event_data = None):
        super().__init__(event_name, event_data)
#endregion class ATViewEvent        
#------------------------------------------------------------------------------+
#region class ATModelEvent
class ATModelEvent(ATEvent):
    '''Event class for events published by the AT View.'''
    def __init__(self, event_name = None, event_data = None):
        super().__init__(event_name, event_data)
#endregion class ATModelEvent        
#------------------------------------------------------------------------------+
#region class ATEventQueue
class ATEventQueue (queue.Queue):
    '''
    ATEventQueue is a subclass of queue.Queue. ATEventQueue is a queue of
    ATEvent objects. The queue is used to store events that are published 
    from actors outside the queue owner.
    '''
    _queue_name = None
    _queue_data = None

    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()

    @property
    def queue_name(self):
        return self._event_name
    
    @queue_name.setter
    def queue_name(self, value):
        self._queue_name = value

    @property
    def queue_data(self):
        return self._queue_data
    
    @queue_data.setter
    def queue_data(self, value):
        self._queue_data = value

    def put(self, event):
        self.queue.put(event)

    def get(self):
        return self.queue.get()

    def empty(self):
        return self.queue.empty()

    def qsize(self):
        return self.queue.qsize()
#endregion class ATEventQueue
#------------------------------------------------------------------------------+
#region class ATEVentManager
#------------------------------------------------------------------------------+
class ATEventManager():
    '''
    ATEventManager is a singleton class that manages the event queues for 
    the Activity Tracker ViewMOdel application. This Event Manager is 
    responsible for for subscribing to events from the ATView.

    A single background thread processes the event queues. The thread waits for
    events to be published to the queues. When an event is published, the 
    a threading.Event is used to signal the background thread to process the
    event queue. A threading.RLock is used to ensure thread-safe access to the
    event queues in self.event_queues.
    TODO: Expand to multiple signal events for various event types with their
    own event queues.
    TODO: Expand to multiple worker threads for each event type with its own.
    '''
    def __init__(self):
        self.event_queues = {}
        self.signal_event = threading.Event()
        self.stop_event = threading.Event()  # To stop event manager threads
        self.running = False
        self.event_thread = threading.Thread(name="ATEventManagerThread", 
                            daemon=True, target=self.process_events_loop)
        self.lock = threading.RLock()  # For thread-safe access to event queues

    def start(self):
        '''Start the event manager thread'''
        logger.debug(f" starting event manager.")
        if not self.event_thread.is_alive():
            self.running = True
            self.event_thread.start()
            t = self.event_thread.native_id
            logger.debug(f" started worker thread {t}.")

    def stopped(self) -> bool:
        '''Check if the event manager stop event is set'''
        return self.stop_event.is_set()
    
    def total_events(self) -> int:
        '''Returns the total number of events in all event queues'''
        ecount = 0
        for eq in self.event_queues.values(): ecount += eq.qsize()
        return ecount

    def stop(self):
        '''Stop the event manager threads'''
        logger.debug(f" stopping event manager.")
        self.stop_event.set()  # Set stop_event to signal worker threads to stop

    def process_events_loop(self):
        '''Main loop to Process events from event queues'''
        m = f" Entry: self.stopped() = {self.stopped()}."
        logger.debug(m); print(m)
        # Runs until the self.stopped() method returns True, 
        # indicating that the self.stop_signal has been set.
        while not self.stopped():  # Loop until stop_event is set
            logger.debug(f" wait next event.")
            if self.signal_event.is_set():
                logger.debug(f" signal_event.is_set()={self.signal_event.is_set()}.")
                all_queues_empty = True
                eqount = len(self.event_queues)
                ecount = self.total_events()
                logger.debug(f" process '{ecount}' events in {eqount} queues.")
                for et in self.event_queues:
                    eq = self.event_queues[et]
                    while not eq.empty():
                        logger.debug(f" process queue {et}" + \
                              f".count={eq.qsize()} ")
                        # Get an event from the queue until none are left
                        event = eq.get()
                        self.process_an_event(event)
                        all_queues_empty = False 
                    logger.debug(f" finished queue {et}" + \
                          f".count={eq.qsize()}")
                # clear signal event when queues are empty
                if all_queues_empty:  
                    self.signal_event.clear()
                    logger.debug(f" signal_event.clear().")
            else:
                to = 2.0
                # print(f" signal_event.is_set():False.")
                # print(f" signal_event.wait({to}).")
                self.signal_event.wait(to)
                m = f" signal_event.wait({to}) expired."
                logger.debug(m); logger.debug(m)
        logger.debug(f" Exit: self.Stopped = {self.stopped}.")
 
    def process_an_event(self, event):
        '''Process an event by calling the event's callback method'''
        et = type(event).__name__; en = event.event_name; ed = event.event_data 
        logger.debug(f"process_an_event(): {et}[event_name='{en}', event_data='{ed}']")
        match type(event):
            case atev.ATViewEvent:
                logger.debug(f"{et} event processing")
            case atev.ATEvent:
                logger.debug(f"{et} event processing")
            case _:
                pass
        return

    def get_event_queue(self, event_type : str, create : bool = True) -> ATEventQueue:
        '''Get the event queue for the event type.
        If the queue already exists, return it.
        If the queue does not exist and create is True, create the event queue. 
        If the queue does not exist and create is False, return None.'''
        logger.debug(f" event_type='{event_type}', create={create}, " \
              f"event_queues({len(self.event_queues)})=" \
                f"{list(self.event_queues.keys())}")
        with self.lock:  # Ensure thread-safe access to event queues
            logger.debug(f" Returning existing event queue for event type: " \
                      f"{event_type}.")
            if event_type in self.event_queues:
                eq = self.event_queues[event_type]
                logger.debug(f" Returning existing event queue for event type: " \
                      f"{event_type}.")
                return eq
            elif create:
                if self.add_event_queue(event_type):
                    return self.event_queues[event_type]
                else:
                    return None
            else:
                return None
        
    def add_event_queue(self, event_type : str):
        '''Add an event_queue to the EventManager for event_type if not
        already added.'''
        logger.debug(f" Entry: event_type='{event_type}' " + \
              f"event_queues({len(self.event_queues)})=" + \
              f"{list(self.event_queues.keys())}")
        with self.lock: # Lock for one thread modifies event_queues at a time
            # Check if the event type already exists in the event queues
            if isinstance(event_type, str) and not event_type in self.event_queues :
                # Add the event queue for event type if not already there.
                #TODO: bug here
                self.event_queues[event_type] = ATEventQueue()
                logger.debug(f" Added event queue for event type: {event_type}" + \
                      f"event_queues({len(self.event_queues)})=" + \
                      f"{list(self.event_queues.keys())}")
                # True when new queue is added
                return True
            else:
                logger.debug(f" NOT Added event queue for event type: " + \
                      f"{event_type}" + \
                      f"event_queues({len(self.event_queues)})=" + \
                      f"{list(self.event_queues.keys())}")
                return False

    def publish(self, event: ATEvent):
        '''Publish an event to the event queue based on the event type'''
        et = type(event).__name__; en = event.event_name
        logger.debug(f":Entry event=[{et}.{en}]")
        # Add the event to the appropriate event queue based on event type.
        if self.get_event_queue(et):
            with self.lock:
                self.event_queues[et].put(event)
            logger.debug(f":Published Event[{et}.{en}] to queue: ")

        # Signal the event queue to process the event
        if not self.signal_event.is_set():
            self.signal_event.set()
            logger.debug(f":Signal event set.")

    def subscribe(self, event_name, callback):
        while not self.event_queue.empty():
            event = self.event_queue.get()
            if event.event_name == event_name:
                callback(event)
#endregion
#------------------------------------------------------------------------------+


#------------------------------------------------------------------------------+
#region local debugging code
if __name__ == "__main__":

    # Debug tests for the ATEventManager and related classes
    myEM = ATEventManager()
    myEM.start()  # Start the event manager thread

    import time
    time.sleep(2)

    # Create and publish events
    event1 = ATModelEvent("ATModelEvent1", {"key1": "value1"})
    event2 = ATViewModelEvent("ATViewModelEvent1", {"key2": "value2"})
    event3 = ATViewEvent("ATViewEvent1", {"key3": "value3"})
    event4 = ATEvent("ATEvent1", {"key4": "value4"})
    # Allow some time for events to be processed
    time.sleep(2)

    myEM.publish(event1)
    time.sleep(2)  # Allow some time for events to be processed
    myEM.publish(event2)
    time.sleep(2)  # Allow some time for events to be processed
    myEM.publish(event3)

    time.sleep(2)  # Allow some time for events to be processed

    # Stop the event manager
    myEM.stop()
#endregion local debugging code

