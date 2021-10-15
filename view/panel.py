from bokeh.models import Div, Button, ColumnDataSource, Slider
from bokeh.layouts import column, row
from bokeh.plotting import figure, show
from bokeh.io import curdoc
from bokeh.server.server import Server
from functools import partial
import controller.awg.start
import controller.awg.stop
import controller.scope.scope
import numpy

def start_bokeh_server():
    myapp = {'/': start_bokeh_app}
    myserver = Server(myapp)
    myserver.start()
    myserver.io_loop.add_callback(myserver.show, "/")
    myserver.io_loop.start()

class Multipulse:
    def __init__(self):
        self.list_of_pulseinfo = []
        self.list_of_pulseview = []
        self.multipulsecolumn = column()
        
        default_pulses = [controller.awg.pulse.PulseInfo(1, 0),
                          controller.awg.pulse.PulseInfo(-0.7, -50),
                          controller.awg.pulse.PulseInfo(-0.4, -100),
                          controller.awg.pulse.PulseInfo(-0.9, -150)]
        
        for pulseinfo in default_pulses:
            self.add_pulse(pulseinfo)
            
    def add_default_pulse(self):
        self.add_pulse(controller.awg.pulse.PulseInfo(1, 0))
        
    def add_pulse(self, pulseinfo):
        index = len(self.list_of_pulseinfo)
        self.list_of_pulseinfo.append(pulseinfo)
        pulseview = PulseView(index, self)
        self.list_of_pulseview.append(pulseview)
        self.multipulsecolumn.children.append(pulseview.get_control_row())
        
    def remove_pulse(self, index):
        del self.list_of_pulseview[index]
        del self.multipulsecolumn.children[index]
    
class PulseView:
    def __init__(self, index, multipulse):
        # index: index of this PulseView within some list of pulses
        # pulseinfo: the PulseInfo that this view represents
        self.index = index
        self.multipulse = multipulse
        
    def change_amplitude(self, on_change_name, old_value, new_value):
        self.multipulse.list_of_pulseinfo[self.index].amplitude = new_value
        
    def change_x_offset(self, on_change_name, old_value, new_value):
        self.multipulse.list_of_pulseinfo[self.index].x_offset = new_value
        
    def remove_this_pulse(self):
        self.multipulse.remove_pulse(self.index)
        
    def get_control_row(self):
        # Get the controls related to this PulseView
        
        amplitude_value = self.multipulse.list_of_pulseinfo[self.index].amplitude
        amplitude_slider = Slider(start = -1, end = 1, value=amplitude_value, step=0.01, title="Amplitude")
        amplitude_slider.on_change('value', self.change_amplitude)
        
        x_offset_value = self.multipulse.list_of_pulseinfo[self.index].x_offset
        x_offset_slider = Slider(start = -200, end = 0, value=x_offset_value, step=1, title="X Offset")
        x_offset_slider.on_change('value', self.change_x_offset)
        
        remove_button = Button(label='Remove')
        remove_button.on_click(self.remove_this_pulse)
        
        return row(amplitude_slider, x_offset_slider, remove_button)
    
def add_awg_controls(doc):
    # Return list of the buttons to control AWG.
    
    multipulse = Multipulse()
    
    start_button = Button(label='Send Waveform')
    start_button.on_click(partial(controller.awg.start.start_waveform, multipulse.list_of_pulseinfo))
    
    stop_button = Button(label='Stop Waveform')
    stop_button.on_click(controller.awg.stop.stop_waveform)
    
    add_pulse_button = Button(label='Add pulse')
    add_pulse_button.on_click(partial(multipulse.add_default_pulse))
    
    doc.add_root(column(start_button, stop_button, add_pulse_button))
    doc.add_root(multipulse.multipulsecolumn)
    
class Panel:
    def __init__(self):
        self.plot_figure_source = ColumnDataSource()
        self.plot_figure = figure(title='Oscilloscope')
        self.plot_figure.line(source=self.plot_figure_source)
        self.x_array = []
        self.y_array = []
        
    def plot_oscilloscope(self):
        thescope = controller.scope.scope.get_pyvisa_scope()
        self.x_array, self.y_array = controller.scope.scope.get_xy_lists(thescope)
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