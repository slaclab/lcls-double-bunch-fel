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
import os
import base64

class Controls:
    def __init__(self, multipulse):
        self.multipulse = multipulse
        
        self.preview_figure_source = ColumnDataSource()
        self.preview_figure = figure(title = 'Preview')
        self.preview_figure.sizing_mode = 'scale_both'
        self.preview_figure.line(source = self.preview_figure_source)
        self.preview_figure.x_range = Range1d(-50 , 300)
        
        self.oscilloscope_image = Div()
        
        self.oscilloscope_figure_source = ColumnDataSource()
        self.oscilloscope_figure = figure(title = 'Oscilloscope', x_axis_label = 'Second', y_axis_label = 'Volt')
        self.oscilloscope_figure.sizing_mode = 'scale_both'
        self.oscilloscope_figure.line(source = self.oscilloscope_figure_source)
        self.oscilloscope_figure.x_range = Range1d(9e-7, 1.4e-6)
        
    def stop_everything(self):
        awg.awg.stop()
        self.server.stop()
        self.server.unlisten()
        self.server.io_loop.stop()
        
    def get_image(self):
        scope_file_data = scope.scope_image.get_scope_image('192.168.1.123')
        data_uri = base64.b64encode(scope_file_data).decode('utf-8')
        img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        self.oscilloscope_image.text = img_tag

    def plot_oscilloscope(self):
        sec_list, volt_list = scope.scope.get_sec_volt_lists()
        self.oscilloscope_figure_source.data = dict(x=sec_list, y=volt_list)
        
    def plot_preview(self):
        preview_x = numpy.linspace(-10, 4000, 4096)
        preview_y = self.multipulse.get_multipulse()
        self.preview_figure_source.data = dict(x=preview_x, y=preview_y)
        
    def save(self):
        sec_list, volt_list = scope.scope.get_sec_volt_lists()
        numpy.savetxt('x', sec_list)
        numpy.savetxt('y', volt_list)
        
    def start_controls(self, doc):
        stop_everything_button = Button(label='Stop everything')
        stop_everything_button.on_click(self.stop_everything) 

        stop_button = Button(label='Stop Waveform')
        stop_button.on_click(awg.awg.stop)
        
        send_button = Button(label='Send Waveform')
        send_button.on_click(partial(awg.awg.send, self.multipulse))
        
        preview_button = Button(label='Preview Waveform')
        preview_button.on_click(self.plot_preview)
        
        image_button = Button(label = 'Image')
        image_button.on_click(self.get_image)
        
        plot_button = Button(label='Plot Oscilloscope')
        plot_button.on_click(self.plot_oscilloscope)

        save_button = Button(label='Save Oscilloscope')
        save_button.on_click(self.save)

        add_pulse_button, multipulse_column = self.multipulse.get_controls()
        controls = column(stop_everything_button, multipulse_column, send_button, stop_button, preview_button, image_button, plot_button, save_button, add_pulse_button)
        
        left = controls
        right = column(self.preview_figure, self.oscilloscope_figure, self.oscilloscope_image)

        doc.add_root(row(left, right))
        
    def start(self):
        self.server = Server({'/': self.start_controls})
        self.server.start()
        self.server.io_loop.add_callback(self.server.show, "/")
        self.server.io_loop.start()
