#------------------------------------------------------------------------------+
import threading, queue
'''
ATEvents is a module that contains classes for managing events in the
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

#------------------------------------------------------------------------------+
#region class ATEventSignal
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
#endregion class ATEvent
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

#------------------------------------------------------------------------------+
#region class ATViewEvent
class ATViewEvent(ATEvent):
    '''Event class for events published by the AT View.'''
    def __init__(self, event_name = None, event_data = None):
        super().__init__(event_name, event_data)
##endregion class ATViewEvent        
#------------------------------------------------------------------------------+
        

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

#------------------------------------------------------------------------------+
#region class ATEVentManager
#------------------------------------------------------------------------------+
class ATEventManager():
    '''
    ATEventManager is a singleton class that manages the event queues for 
    the Activity Tracker ViewMOdel application. This Event Manager is 
    responsible for for subscribing to events from the ATView.
    TODO: Expand to multiple signal events for various event types with their
    own event queues.
    TODO: Expand to multiple worker threads for each event type with its own.
    '''
    def __init__(self):
        self.event_queues = {}
        self.signal_event = threading.Event()
        self.running = False
        self.event_thread = threading.Thread(target=self.process_events, daemon=True)

    def process_events(self):
        '''Process the events in the event queue'''
        while self.running:
            if self.signal_event.is_set():
                for event_type in self.event_queues:
                    event_queue = self.event_queues[event_type]
                    if not event_queue.empty():
                        # Get an event from the queue
                        event = event_queue.get()
                        self.signal_event.clear()
                        self.process_event(event)
            else:
                self.signal_event.wait()

    def start(self):
        '''Start the event manager thread'''
        self.running = True
        if not self.event_thread.is_alive():
            self.event_thread.start()

    def get_event_queue(self, event_type : str, create : bool = True) -> ATEventQueue:
        '''Get the event queue for the event type if it exists.
        If create is True, create the event queue if it does not exist.'''
        if event_type in self.event_queues:
            return self.event_queues[event_type]
        elif create:
            return self.add_event_queue(event_type)
        else:
            return
        
    def add_event_queue(self, event_type : str):
        '''Add an event_queue to the EventManager for event_type if not
        already added.'''
        if isinstance(event_type, str) and not event_type in self.event_queues :
            # Add the event queue for event type if not already there.
            self.event_queues[event_type] = ATEventQueue()
            # True when new queue is added
            return True
        else:
            return False

    def publish(self, event: ATEvent):
        '''Publish an event to the event queue based on the event type'''

        # Add the event to the indicated event queue.
        if self.get_event_queue(event.event_name):
            self.event_queues[event.event_name].put(event)

        # Signal the event queue to process the event
        if not self.signal_event.is_set():
            self.signal_event.set()

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
    myEM = ATEventManager()



#endregion local debugging code

