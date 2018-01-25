"""
Modules for graphs
"""
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas, \
                                              TimerTk                             
# implement the default mpl key bindings
from matplotlib.figure import Figure

# module to form signals
import numpy as np

#--------------------------------------------------
############################################################
class MplGraph(FigureCanvas):
    """
    Prepare graph canvas
    """
    
    def __init__(self, parent, packSettings, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        
        self._initialize_figure()
        
        FigureCanvas.__init__(self, figure=fig, master=parent)
        self.show()       
        self.get_tk_widget().pack(packSettings)
        
    def _initialize_figure(self):
        """
        Virtual method to be overwritten.
        Initialize plot to default value.
        """
        pass

class MainGraph(MplGraph):
    """
    Create dynamic figure that display.
    """
    
    def __init__(self, parent, packSettings, interval=None, **kwargs):
        MplGraph.__init__(self, parent, packSettings, **kwargs)
        self.update_figure()
        self._tkcanvas.pack(packSettings)
        timer = TimerTk(parent)
        timer.add_callback(self.update_figure)
        timer.start(interval)
    
    def _initialize_figure(self):
        self.axes.plot([0], [0], 'r')

    def update_figure(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        l = np.random.rand(t.shape[0]) - 0.5
        self.axes.cla()
        self.axes.plot(t, s+l, 'r')
        self.draw()
        
#######################################################################
#--------------------------------------------------
