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
        self._tkcanvas.pack(packSettings)
        self.interval = interval
        self.data = (np.linspace(0, 1, 100), np.linspace(0, 1, 100))
        self._update_figure()
        self.timer = TimerTk(parent)
        self.timer.add_callback(self._update_figure)
        self.timerOn = False
        
    def put_data(self, data):
        self.data = data
        #print(self.data)

    def view_handling(self):
        if self.timerOn:
            self.timer.stop()
            self.timerOn = False
        else:
            self.timer.start(self.interval)
            self.timerOn = True
        
    def _update_figure(self):
        self.axes.cla()
        self.axes.plot(*self.data, 'r')
        self.draw()
        
#######################################################################
#--------------------------------------------------
