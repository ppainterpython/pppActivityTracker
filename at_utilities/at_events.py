#-----------------------------------------------------------------------------+
import threading, queue

#-----------------------------------------------------------------------------+
#region claa ATEvent
class ATEvent (threading.Event):
    ''' ATEvent is a subclass of threading.Event. ATEvents are published to
    notify the owning module about an event in their scope.'''
    _event_name = None
    _event_data = None

    def __init__(self, event_name:str=None, event_data:dict=None):
        super().__init__()
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

    def set(self):
        super().set()

    def clear(self):
        super().clear()

    def wait(self, timeout=None):
        return super().wait(timeout)
#endregion class ATEvent
#-----------------------------------------------------------------------------+
    

#-----------------------------------------------------------------------------+
#region class ATEventQueue
class ATEventQueue (queue.Queue):
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()

    def put(self, event):
        self.queue.put(event)

    def get(self):
        return self.queue.get()

    def empty(self):
        return self.queue.empty()

    def qsize(self):
        return self.queue.qsize()
#endregion class ATEventQueue
#-----------------------------------------------------------------------------+

# for local debugging
if __name__ == "__main__":
    myEQ = ATEventQueue()
    ev1 = ATEvent("Event1", {"data1": "data1"})
    ev2 = ATEvent("Event2", {"data2": "data2"})
    ev3 = ATEvent("Event3", {"data3": "data3"})

    myEQ.put(ev1)
    myEQ.put(ev2)
    myEQ.put(ev3)

    
