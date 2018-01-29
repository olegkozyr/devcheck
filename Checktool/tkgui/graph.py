"""
Modules for graphs
"""
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
                                              TimerTk                             
# implement the default mpl key bindings
from matplotlib.figure import Figure

# module to form signals
import numpy as np

import tkgui.gui_constants as gc

import queue

#--------------------------------------------------
############################################################
class MainGraph(FigureCanvasTkAgg):
    """

    """
    
    def __init__(self, parent, dataQueue, interval, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.dataQueue = dataQueue
        self.line = None
        
        self._initialize_figure()    
            
        FigureCanvasTkAgg.__init__(self, figure=self.fig, master=parent)
        self.show()       
        self.get_tk_widget().pack(gc.packSettings)
        self._tkcanvas.pack(gc.packSettings)
        self.interval = interval        
        self._update_figure()
        self.timer = TimerTk(parent)
        self.timer.add_callback(self._update_figure)
        self.timerOn = False
 
    def _initialize_figure(self):
        try:
            data = self.dataQueue.get(block=False)
        except queue.Empty:
            pass
        else:
            self.line, = self.axes.plot(data)
        
        self.axes.set_ylim(-1.1, 1.1)
        self.axes.set_xlim(-0.1, 100.1)

    def view_handling(self):
        if self.timerOn:
            self.timer.stop()
            self.timerOn = False
        else:
            self.timer.start(self.interval)
            self.timerOn = True
        
    def _update_figure(self):
        try:
            data = self.dataQueue.get(block=False)
        except queue.Empty:
            pass
        else:
            #self.axes.cla()
            #self.axes.plot(self.data, 'r')
            #self.draw()
            self.line.set_ydata(data)
            #self.axes.draw_artist(self.axes.patch)
            #self.axes.draw_artist(self.line)
            #self.fig.canvas.update()
            self.draw()
            self.fig.canvas.flush_events()
        
#######################################################################
#--------------------------------------------------

