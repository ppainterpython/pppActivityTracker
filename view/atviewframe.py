#-----------------------------------------------------------------------------+
import tkinter as tk
from tkinter import EventType
from tkinter import ttk
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from view.constants import AT_FAINT_GRAY
class ATViewFrame(tb.Frame):
    """ Activity Tracker View class.
        The ATView class is a subclass of the tkinter.Tk class and implements 
        the entire user interface for the Activity Tracker application.
    """
    # DataContext properties
    filepath_value: tk.StringVar # file path for the activity tracker data file

    # UI widgets
    root : tb.Window = None # root window
    filepath_entry: tk.Entry = None
    quit_button: tk.Button = None

    def __init__(self, root): # self is tk.Tk root window
        # init super class (tk.Frame)
        super().__init__()
        self.grid(pady=10, padx=10, sticky="nsew") # grid layout for the frame
        style = ttk.Style()
        style.configure('TFrame', background=AT_FAINT_GRAY)

        # init properties
        self.root = root # reference to the root window
        self.filepath_value = tk.StringVar()
        # init widgets in root window
        self.create_atviewframe_widgets() # setup atviewframe widgets
        self.layout_atviewframe_widgets() # layout atviewframe widgets
        self.bind_atviewframe_widgets()   # bind atviewframe widgets to events

    def create_atviewframe_widgets(self):
        self.filepath_label = tk.Label(self, text="File Path:")
        self.filepath_value.set("") # default value
        self.filepath_entry = tk.Entry(self,textvariable=self.filepath_value)
        self.quit_button = tk.Button(self, text="Quit", command=self.root.destroy)

    def layout_atviewframe_widgets(self):
        self.filepath_label.grid(column=0, row=0)
        self.filepath_entry.grid(column=1, row=0)
        self.quit_button.grid(column=4, row=0, padx=5, pady=5, sticky="e") # quit button on right side

    def bind_atviewframe_widgets(self):
        self.filepath_entry.bind("<Return>", self.on_filepath_changed)
        self.filepath_entry.bind("<Tab>", self.on_filepath_changed)
        self.filepath_entry.bind("<FocusOut>", self.on_filepath_changed)
        # self.filepath_value.trace_add('write', self.on_filepath_changed) # bind filepath change event

    def set_datacontext(self, datacontext: object):
        self.datacontext = datacontext

    def set_filepath(self, filepath: str):
        self.filepath_value.set(filepath)

    def on_filepath_changed(self, event):
        """ Event handler for when the user presses the Enter key in the filepath entry. """
        # for <Return> key event, event.keysym = 'Return'
        # for <Tab> key event, event.keysym = 'Tab'
        # for <FocusOut> event, event.type = 'EventType.FocusOut'
        v = self.filepath_value.get()
        s = "<Return> key event" if event.keysym == 'Return' else \
            "<Tab> key event" if event.keysym == 'Tab' else \
            "<FocusOut> event" if event.type == EventType.FocusOut else "Unknown event"

        print(f"ATView.ATVFrame.filepath changed to: {v} after: {s}")

    
#-----------------------------------------------------------------------------+