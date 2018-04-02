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

#--------------------------------------------------
############################################################
class MainGraph(FigureCanvasTkAgg):
    """

    """
    
    def __init__(self, parent, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.line = None
        
        self._initialize_figure()    
            
        FigureCanvasTkAgg.__init__(self, figure=self.fig, master=parent)
        self.show()       
        self.get_tk_widget().pack(gc.packSettings)
        self._tkcanvas.pack(gc.packSettings)     
 
    def _initialize_figure(self):
        self.line, = self.axes.plot(np.zeros(100))
        self.axes.set_xlim(-0.1, 1.1)
        self.axes.set_ylim(-1.1, 1.1)
        self.axes.grid()
        
    def update_figure(self, data):
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

