"""
Gui module to build app windows

"""

# GUI module
import tkinter as tk
import tkgui.graph as gr
import tkgui.gui_constants as gconst
import numpy as np

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
        self.mainGraph = gr.MainGraph(self, gconst.packSettings, self.interval)
                 

class FrameFunc(tk.Frame):
    """
    Frame with button for quit app.
    """
    def __init__(self, parent, graph):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.TOP)
        self.graph = graph
        self.generationID = None
        self._make_widgets()

    def _make_widgets(self):  
        #Button starts data produsing                      
        tk.Button(self, text='Start', command=self.start_generation).pack(side=tk.LEFT)
        
        # Button to quits application
        tk.Button(self, text='Quit', command=self._quit).pack(side=tk.LEFT)

    def _quit(self):
        self.master.quit()
        self.master.destroy()

    def start_generation(self):
        self.graph.view_handling()
        self._generation_handling()
        
        
    def _generation_handling(self):
        if self.generationID:
            self.after_cancel(self.generationID)
            self.generationID = None
        else:
            self._data_func()          
            

    def _data_func(self):
        """
        Generate data.
        """
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        l = np.random.rand(t.shape[0]) - 0.5
        self.graph.put_data((t, l+s))
        self.generationID = self.after(1000, self._data_func)
            
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
        graph = FrameGraph(self, self.interval)
        graph.pack(gconst.packSettings) 
        FrameFunc(self, graph.mainGraph).pack(side=tk.TOP) 
        
        
        