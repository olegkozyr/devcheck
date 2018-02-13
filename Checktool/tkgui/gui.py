"""
Gui module to build app windows

"""

# GUI module
import tkinter as tk
import tkgui.graph as gr
import tkgui.gui_constants as gc
import numpy as np

import threading, queue, time

class ProducerThread(threading.Thread):
    def __init__(self, dataQueue):
        self.running = True
        self.dataQueue = dataQueue
        threading.Thread.__init__(self)

    def run(self):
        """
        Override threading.Thread.run(self)
        Generate data.
        """

        f = 250
        n = 100 
        dt = 1.0/(f*n)
        t = np.arange(0.0, 0.004, dt)
        s = np.sin(2*np.pi*250*t) 
        while self.running:
            l = np.random.rand(t.shape[0]) - 0.5 + s
            self.dataQueue.put(l)
            time.sleep(0.2)
    
    def stop(self):
        self.running = False

class FrameGraph(tk.Frame):
    """
    Frame with canvas
    """
    def __init__(self, parent, dataQueue, interval):
        tk.Frame.__init__(self, parent)
        self.pack(gc.packSettings)
        self.dataQueue = dataQueue
        self.interval = interval
        self.isPlotting = False
        self._make_widgets()
        
    def _make_widgets(self):
        self.mainGraph = gr.MainGraph(self, self.interval)

    def start_plotting(self):
        if self.isPlotting:
            self.isPlotting = False
            while self.dataQueue.qsize() != 0:
                self.dataQueue.get()
        else:
            self.isPlotting = True
            self.plot()
        
    def plot(self):
        try:
            data = self.dataQueue.get(block=False)
        except queue.Empty:
            pass
        else:   
            self.mainGraph.update_figure(data)
        if self.isPlotting:
            self.after(self.interval, self.plot)

class FrameFunc(tk.Frame):
    """
    Frame with button for quit app.
    """
    def __init__(self, parent, frameGraph, dataQueue):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.TOP)
        self.frameGraph = frameGraph
        self.dataQueue = dataQueue
        self.dataThread = None
        self._make_widgets()

    def _make_widgets(self):  
        #Button starts data produsing                      
        tk.Button(self, text='Start', command=self.start_generation).pack(side=tk.LEFT)
        
        # Button to quits application
        tk.Button(self, text='Quit', command=self._quit).pack(side=tk.LEFT)

    def _quit(self):
        if self.dataThread:
            self.stop_thread()
        self.master.quit()
        self.master.destroy()

    def start_generation(self):
        self.frameGraph.start_plotting() 
        self._generation_handling()

    def stop_thread(self):
        self.dataThread.stop()
        self.dataThread.join()
        self.dataThread = None        
                
    def _generation_handling(self):
        if self.dataThread:
            self.stop_thread()
        else:         
            self.dataThread = ProducerThread(self.dataQueue)
            self.dataThread.start()       
            
class MainWindow(tk.Frame):
    """
    Main window
    """
    def __init__(self, parent, interval):
        tk.Frame.__init__(self, parent)
        self.pack(gc.packSettings)
        
        self.dataQueue = queue.Queue() 
        self._make_widgets(interval)
        
    def _make_widgets(self, interval):   
        frameGraph = FrameGraph(self, self.dataQueue, interval)
        frameGraph.pack(gc.packSettings) 
        FrameFunc(self, frameGraph, self.dataQueue).pack(side=tk.TOP) 
        
        
        