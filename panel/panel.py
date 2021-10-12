from bokeh.models import Div, Button, ColumnDataSource
from bokeh.layouts import column
from bokeh.plotting import figure, show
from bokeh.io import curdoc
from bokeh.server.server import Server
import awg.start
import awg.stop
import scope.scope
import numpy

def start_bokeh_server():
    myapp = {'/': start_bokeh_app}
    myserver = Server(myapp)
    myserver.start()
    myserver.io_loop.add_callback(myserver.show, "/")
    myserver.io_loop.start()
    
def add_awg_controls(doc):
    # Return list of the buttons to control AWG.
    
    start_button = Button(label='Send Waveform')
    start_button.on_click(awg.start.start_waveform)
    
    stop_button = Button(label='Stop Waveform')
    stop_button.on_click(awg.stop.stop_waveform)
    
    doc.add_root(column(start_button, stop_button))
    
class Panel:
    def __init__(self):
        self.plot_figure_source = ColumnDataSource()
        self.plot_figure = figure(title='Oscilloscope')
        self.plot_figure.line(source=self.plot_figure_source)
        self.x_array = []
        self.y_array = []
        
    def plot_oscilloscope(self):
        thescope = scope.scope.get_pyvisa_scope()
        self.x_array, self.y_array = scope.scope.get_xy_lists(thescope)
        self.plot_figure_source.data = dict(x=self.x_array, y=self.y_array)
        
    def save(self):
        numpy.savetxt('x', self.x_array)
        numpy.savetxt('y', self.y_array)
        
    
def add_scope_controls(doc):
    # Return list of buttons to control scope.
    
    mypanel = Panel()
    
    plot_button = Button(label='Plot Oscilloscope')
    plot_button.on_click(mypanel.plot_oscilloscope)
    
    save_button = Button(label='Save')
    save_button.on_click(mypanel.save)
    
    doc.add_root(column(plot_button, save_button))
    doc.add_root(column(mypanel.plot_figure))

def start_bokeh_app(doc):
    add_awg_controls(doc)
    add_scope_controls(doc)