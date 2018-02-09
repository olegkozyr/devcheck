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
        """
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
            print('thread working')
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
        self.interval = interval
        self._make_widgets(dataQueue)
        
    def _make_widgets(self, dataQueue):
        self.mainGraph = gr.MainGraph(self, dataQueue, self.interval)
                 

class FrameFunc(tk.Frame):
    """
    Frame with button for quit app.
    """
    def __init__(self, parent, graph, dataQueue):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.TOP)
        self.graph = graph
        self.dataQueue = dataQueue
        self.dataThread = None
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
        if self.dataThread:
            self.dataThread.stop()
            self.dataThread.join()
            self.dataThread = None
            print(self.dataQueue._qsize())
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
        self.dataQueue.put(np.zeros(100))
        self._make_widgets(interval)
        
    def _make_widgets(self, interval):   
        frameGraph = FrameGraph(self, self.dataQueue, interval)
        frameGraph.pack(gc.packSettings) 
        FrameFunc(self, frameGraph.mainGraph, self.dataQueue).pack(side=tk.TOP) 
        
        
        