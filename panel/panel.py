from bokeh.models import Div, Button, ColumnDataSource, Slider
from bokeh.layouts import column, row, layout
from bokeh.plotting import figure, show
from bokeh.models import Range1d
from bokeh.io import curdoc
from bokeh.server.server import Server
from functools import partial
import pulse.multipulse
import awg.awg
import scope.scope
import numpy
import signal
import time

class Controls:
    def __init__(self, multipulse):
        self.multipulse = multipulse
        
        self.preview_figure_source = ColumnDataSource()
        self.preview_figure = figure(title = 'Preview')
        self.preview_figure.line(source = self.preview_figure_source)
        
        self.oscilloscope_figure_source = ColumnDataSource()
        self.oscilloscope_figure = figure(title = 'Oscilloscope')
        self.oscilloscope_figure.line(source = self.oscilloscope_figure_source)
        self.oscilloscope_figure.x_range = Range1d(9e-7, 1.1e-6)
        
    def stop_server(self):
        self.server.stop()
        self.server.unlisten()
        self.server.io_loop.stop()
        
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
        
    def start_controls(self, doc):
        stop_server_button = Button(label='Stop server')
        stop_server_button.on_click(self.stop_server) 

        stop_button = Button(label='Stop Waveform')
        stop_button.on_click(awg.awg.stop)
        
        start_button = Button(label='Start Waveform')
        start_button.on_click(partial(awg.awg.start, self.multipulse))
        
        preview_button = Button(label='Preview Waveform')
        preview_button.on_click(self.plot_preview)
        
        plot_button = Button(label='Plot Oscilloscope')
        plot_button.on_click(self.plot_oscilloscope)

        save_button = Button(label='Save Oscilloscope')
        save_button.on_click(self.save)

        add_pulse_button, multipulse_column = self.multipulse.get_controls()
        controls = column(stop_server_button, multipulse_column, start_button, stop_button, preview_button, plot_button, save_button, add_pulse_button)
        
        left = controls
        right = column(self.preview_figure, self.oscilloscope_figure)

        doc.add_root(row(left, right))
        
    def start(self):
        self.server = Server({'/': self.start_controls})
        self.server.start()
        self.server.io_loop.add_callback(self.server.show, "/")
        self.server.io_loop.start()
