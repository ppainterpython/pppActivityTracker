#-----------------------------------------------------------------------------+
import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from view import atviewframe as atvf
from view.constants import AT_FAINT_GRAY

ATV_WINDOW_TITLE = "PP Python Activity Tracker"
class ATView(tb.Window):
    """ Activity Tracker View class.
        The ATView class is a subclass of the tkinter.Tk class and implements 
        the entire user interface for the Activity Tracker application.

        Properties
        ----------
        datacontext : object
            The data context for the view, typically a ViewModel object. 
            For ATView class, the datacontext should be a ATViewModel object.
    """
    # Property attributes
    datacontext: object = None    # ATViewModel object used as datacontext
    tkview_frame: tk.Frame = None

    # Class constructor
    def __init__(self, title=ATV_WINDOW_TITLE, themename='cosmo'): # self is tk.Tk root window
        # init root window
        super().__init__(title,themename)
        # self.title("PP Python Activity Tracker")
        self.configure(bg=AT_FAINT_GRAY)
        self.geometry("800x500")
        # init properties
        self.tkview_frame = atvf.ATViewFrame(self)

    def on_datacontext_changed(self, viewmodel):
        raise NotImplementedError("on_datacontext_change must be implemented in the subclass")
    

#-----------------------------------------------------------------------------+