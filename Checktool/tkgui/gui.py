"""
Gui module to build app windows

"""

# GUI module
import tkinter as tk
import tkgui.graph as gr
import tkgui.gui_constants as gconst

class FrameGraph(tk.Frame):
    """
    Frame with canvas
    """
    def __init__(self, parent=None, interval=None):
        tk.Frame.__init__(self, parent)
        self.pack(gconst.packSettings)
        self.interval = interval
        self._make_widgets()
        
    def _make_widgets(self):
        gr.MainGraph(self, gconst.packSettings, self.interval)
                 

class FrameFunc(tk.Frame):
    """
    Frame with button for quit app.
    """
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.TOP)
        self._make_widgets()

    def _make_widgets(self):                        
        tk.Button(self, text='Quit', command=self._quit).pack(side=tk.TOP)

    def _quit(self):
        self.master.quit()
        self.master.destroy()
            
class MainWindow(tk.Frame):
    """
    Main window
    """
    def __init__(self, parent=None, interval=None):
        tk.Frame.__init__(self, parent)
        self.pack(gconst.packSettings)
        self.interval = interval
        self._make_widgets()
        
    def _make_widgets(self):   
        FrameGraph(self, self.interval).pack(gconst.packSettings) 
        FrameFunc(self).pack(side=tk.TOP) 
        