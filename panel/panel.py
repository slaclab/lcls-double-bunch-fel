from bokeh.models import Div, Button, ColumnDataSource, Slider
from bokeh.layouts import column, row
from bokeh.plotting import figure, show
from bokeh.models import Range1d
from bokeh.io import curdoc
from bokeh.server.server import Server
from functools import partial
import pulse.multipulse
import awg.awg
import scope.scope
import numpy

class Panel:
    def __init__(self, multipulse):
        self.multipulse = multipulse
        
        self.preview_figure_source = ColumnDataSource()
        self.preview_figure = figure(title='Preview')
        self.preview_figure.line(source=self.preview_figure_source)
        
        self.oscilloscope_figure_source = ColumnDataSource()
        self.oscilloscope_figure = figure(title='Measured')
        self.oscilloscope_figure.line(source=self.oscilloscope_figure_source)
        self.oscilloscope_figure.x_range=Range1d(9e-7, 1.1e-6)
        
    def plot_oscilloscope(self):
        thescope = scope.scope.get_pyvisa_scope()
        measured_x, measured_y = scope.scope.get_xy_lists(thescope)
        self.oscilloscope_figure_source.data = dict(x=measured_x, y=measured_y)
        
    def plot_preview(self):
        preview_x = numpy.linspace(-10, 4000, 4096)
        preview_y = self.multipulse.get_multipulse()
        self.preview_figure_source.data = dict(x=preview_x, y=preview_y)
        
    def save(self):
        numpy.savetxt('x', self.measured_x)
        numpy.savetxt('y', self.measured_y)
        
    def add_awg_controls(self, doc):
        preview_button = Button(label='Preview Waveform')
        preview_button.on_click(self.plot_preview)
        doc.add_root(column(self.preview_figure))
        
        start_button = Button(label='Start Waveform')
        start_button.on_click(partial(awg.awg.start, self.multipulse))

        stop_button = Button(label='Stop Waveform')
        stop_button.on_click(awg.awg.stop)

        doc.add_root(column(preview_button, start_button, stop_button))
        self.multipulse.add_controls(doc)
        
    def add_scope_controls(self, doc):
        plot_button = Button(label='Plot Oscilloscope')
        plot_button.on_click(self.plot_oscilloscope)

        save_button = Button(label='Save')
        save_button.on_click(self.save)

        doc.add_root(column(plot_button, save_button))
        doc.add_root(column(self.oscilloscope_figure))
        
    def start_bokeh_app(self, doc):
        self.add_awg_controls(doc)
        self.add_scope_controls(doc)
        
    def start(self):
        myapp = {'/': self.start_bokeh_app}
        myserver = Server(myapp)
        myserver.start()
        myserver.io_loop.add_callback(myserver.show, "/")
        myserver.io_loop.start()
