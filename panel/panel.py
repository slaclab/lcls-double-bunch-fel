from bokeh.models import Div, Button, ColumnDataSource, Slider
from bokeh.layouts import column, row, grid
from bokeh.plotting import figure, show
from bokeh.models import Range1d
from bokeh.server.server import Server
from functools import partial
import pulse.multipulse
import awg.awg
import scope.scope
import base64
import h5py

class Panel:
    def __init__(self, multipulse):
        self.multipulse = multipulse
        
        # Anything regarding sizing is purely cosmetic.
        # Preferably Bokeh does this for us but alas.
                
        self.preview_figure_source = ColumnDataSource()
        self.preview_figure = figure(title = 'Preview', x_axis_label = 'Nanoseconds', y_axis_label = 'Volt')
        self.preview_figure.line(source = self.preview_figure_source)
        self.preview_figure.x_range = Range1d(-20, 400)
        self.preview_figure.sizing_mode = 'stretch_both'
        
        self.oscilloscope_image = Div()
        self.oscilloscope_image.width = 640
        self.oscilloscope_image.height = 480
        
        self.oscilloscope_figure_source = ColumnDataSource()
        self.oscilloscope_figure = figure(title = 'Oscilloscope', x_axis_label = 'Nanoseconds', y_axis_label = 'Volt')
        self.oscilloscope_figure.line(source = self.oscilloscope_figure_source)
        self.oscilloscope_figure.x_range = Range1d(600, 900)
        self.oscilloscope_figure.sizing_mode = 'stretch_both'
        
    def stop_everything(self):
        awg.awg.stop()
        self.server.stop()
        self.server.unlisten()
        self.server.io_loop.stop()
        
    def get_image(self):
        scope_file_data = scope.scope_image.get_scope_image()
        data_uri = base64.b64encode(scope_file_data).decode('utf-8')
        img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        self.oscilloscope_image.text = img_tag

    def plot_oscilloscope(self):
        sec_list, volt_list = scope.scope.get_nanosec_volt_lists()
        self.oscilloscope_figure_source.data = dict(x = sec_list, y = volt_list)
        
    def plot_preview(self):
        preview_x, preview_y = self.multipulse.get_preview_waveform()
        self.preview_figure_source.data = dict(x = preview_x, y = preview_y)
        
    def save(self):
        # Save the input waveform, the parameters of the waveform, the and the 
        # nanosecond-Volt data measured from the oscilloscope.
        self.oscilloscope_figure_source.x
        self.oscilloscope_figure_source.y
        self.preview_figure_source.x
        self.preview_figure_source.y
        self.multipulse.get_awg_waveform()
        
        
    def start_controls(self, doc):
        stop_everything_button = Button(label='Stop everything')
        stop_everything_button.on_click(self.stop_everything)

        stop_button = Button(label='Stop Waveform')
        stop_button.on_click(awg.awg.stop)
        
        send_button = Button(label='Send Waveform')
        send_button.on_click(partial(awg.awg.send, self.multipulse))
        
        preview_button = Button(label='Preview Waveform')
        preview_button.on_click(self.plot_preview)
        
        plot_button = Button(label='Plot Oscilloscope')
        plot_button.on_click(self.plot_oscilloscope)

        save_button = Button(label='Save Oscilloscope')
        save_button.on_click(self.save)
        
        image_button = Button(label = 'Image')
        image_button.on_click(self.get_image)

        multipulse_column = column()
        add_pulse_button = self.multipulse.get_add_button(multipulse_column)
        self.multipulse.add_controls_to(multipulse_column)        
        left = column(stop_everything_button, multipulse_column, add_pulse_button, send_button, stop_button, preview_button, plot_button, save_button, image_button)
        
        right = column(self.preview_figure, self.oscilloscope_figure, self.oscilloscope_image)
        right.height = 600
        right.width = 500

        doc.add_root(row(left, right))
        
    def start(self):
        self.server = Server({'/': self.start_controls})
        self.server.start()
        self.server.io_loop.add_callback(self.server.show, "/")
        self.server.io_loop.start()
