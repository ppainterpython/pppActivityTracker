#-----------------------------------------------------------------------------+
import tkinter as tk
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PP Python Activity Tracker")
        self.geometry("800x500")
        self.create_widgets()

    def create_widgets(self):
        frm = tk.Frame(self)
        frm.grid()
        tk.Label(frm, text="Hello World!").grid(column=0, row=0)
        tk.Button(frm, text="Quit", command=self.destroy).grid(column=1, row=0)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
#-----------------------------------------------------------------------------+