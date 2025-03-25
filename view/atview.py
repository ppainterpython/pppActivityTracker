#-----------------------------------------------------------------------------+
import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tb  # tb.Window used for root window only
from view import atviewframe as atvf
from view.constants import ATV_FAINT_GRAY

ATV_WINDOW_TITLE = "PP Python Activity Tracker"
ATV_MIN_WINDOW_WIDTH = 800
ATV_MIN_WINDOW_HEIGHT = 450
ATV_MAX_WINDOW_WIDTH = 1600
ATV_MAX_WINDOW_HEIGHT = 1000

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
    #region ATView class
    #--------------------------------------------------------------------------+
    # Public Property attributes
    datacontext: object = None    # ATViewModel object used as datacontext
    tkview_frame: tk.Frame = None

    # Private attributes
    __width: int = ATV_MIN_WINDOW_WIDTH
    __height: int = ATV_MIN_WINDOW_HEIGHT
    __geometry: str = f"{__width}x{__height}"
    # Class constructor
    def __init__(self, title=ATV_WINDOW_TITLE, themename='cosmo'):
        # init root window
        super().__init__(title,themename)
        self.configure(bg=ATV_FAINT_GRAY)
        self.geometry(self.__geometry)
        self.minsize(ATV_MIN_WINDOW_WIDTH, ATV_MIN_WINDOW_HEIGHT)
        self.maxsize(ATV_MAX_WINDOW_WIDTH, ATV_MAX_WINDOW_HEIGHT)
        # init properties
        self.tkview_frame = atvf.ATViewFrame(self) # create the view frame

    #--------------------------------------------------------------------------+
    # Property attributes

    #--------------------------------------------------------------------------+
    # Event Handler Methods

    def on_datacontext_changed(self, viewmodel):
        raise NotImplementedError("on_datacontext_change must be implemented in the subclass")
    

#------------------------------------------------------------------------------+