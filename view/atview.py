#-----------------------------------------------------------------------------+
import tkinter as tk
from view import atviewframe as atvf
class ATView(tk.Tk):
    """ Activity Tracker View class.
        The ATView class is a subclass of the tkinter.Tk class and implements 
        the entire user interface for the Activity Tracker application.

        Properties
        ----------
        datacontext : object
            The data context for the view, typically a ViewModel object. 
            For ATView class, the datacontext should be a ATViewModel object.
    """
    datacontext: object = None
    tkview_frame: tk.Frame = None
    def __init__(self): # self is tk.Tk root window
        # init root window
        super().__init__()
        self.title("PP Python Activity Tracker")
        self.geometry("800x500")
        # init properties
        self.tkview_frame = atvf.ATViewFrame(self)

    def on_datacontext_changed(self, viewmodel):
        raise NotImplementedError("on_datacontext_change must be implemented in the subclass")
    

#-----------------------------------------------------------------------------+