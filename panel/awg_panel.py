from bokeh.models import Div, Button, ColumnDataSource, Slider
from bokeh.layouts import column, row, grid
from bokeh.plotting import figure
import base64
from functools import partial

from bokeh.models import Range1d, Spinner, TextAreaInput
import scope.awgscope
import awg.awg

class AWGPanel:
    def __init__(self, multipulse):
        self.multipulse = multipulse
        
        self.preview_figure_source = ColumnDataSource()
        self.preview_figure_source.data = dict(x=[], y=[])
        self.preview_figure = figure(title = 'Preview', x_axis_label = 'Nanoseconds', y_axis_label = 'Volt')
        self.preview_figure.line(source = self.preview_figure_source)
        self.preview_figure.x_range = Range1d(-20, 400)
        self.preview_figure.height = 300
    
        self.awgscope_figure_source = ColumnDataSource()
        self.awgscope_figure_source.data = dict(x=[], y=[])
        self.awgscope_figure = figure(title = 'AWG Scope', x_axis_label = 'Nanoseconds', y_axis_label = 'Volt')
        self.awgscope_figure.line(source = self.awgscope_figure_source)
        #self.awgscope_figure.x_range = Range1d(600, 900)
        self.awgscope_figure.height = 300
        
        self.awgscope_image = Div(height = 480)
        
    def plot_preview(self):
        preview_x, preview_y = self.multipulse.get_preview_waveform()
        self.preview_figure_source.data = dict(x = preview_x, y = preview_y)
        
    def get_awgscope_image(self):
        png = scope.awgscope_image.get()
        data_uri = base64.b64encode(png).decode('utf-8')
        img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        self.awgscope_image.text = img_tag
        
    def plot_awgscope(self):
        sec_list, volt_list = scope.awgscope.get_nanosec_volt_lists()
        self.awgscope_figure_source.data = dict(x = sec_list, y = volt_list)
        
    def get_controls(self):
        stop_button = Button(label='Stop Waveform')
        stop_button.on_click(awg.awg.stop)
        
        send_button = Button(label='Send Waveform')
        send_button.on_click(partial(awg.awg.send, self.multipulse))
        
        preview_button = Button(label='Preview Waveform')
        preview_button.on_click(self.plot_preview)
        
        plot_awgscope_button = Button(label='Plot AWG Scope')
        plot_awgscope_button.on_click(self.plot_awgscope)
        
        awgscope_image_button = Button(label = 'Get AWG Scope Image')
        awgscope_image_button.on_click(self.get_awgscope_image)
        
        multipulse_column = column()
        add_pulse_button = self.multipulse.get_add_button(multipulse_column)
        self.multipulse.add_controls_to(multipulse_column)  
        
        return self.preview_figure, self.awgscope_figure, self.awgscope_image, stop_button, send_button, preview_button, plot_awgscope_button, awgscope_image_button, multipulse_column, add_pulse_button
        
    def addto(self, savefile, number_of_traces):
        
        preview_x, preview_y = self.multipulse.get_preview_waveform()
        savefile.create_dataset('preview_x', (len(preview_x),), data = preview_x)
        savefile.create_dataset('preview_y', (len(preview_y),), data = preview_y)
        waveform_x, waveform_y = self.multipulse.get_awg_waveform()
        savefile.create_dataset('awgscope_x', (len(waveform_x),), data = waveform_x)
        savefile.create_dataset('awgscope_y', (len(waveform_y),), data = waveform_y)

        awgscope_traces_x = list()
        awgscope_traces_y = list()
        awgscope_x, awgscope_y = scope.awgscope.get_nanosec_volt_lists()
        
        for index in range(number_of_traces):
            awgscope_x, awgscope_y = scope.awgscope.get_nanosec_volt_lists()
            awgscope_traces_x.append(awgscope_x)
            awgscope_traces_y.append(awgscope_y)

        savefile.create_dataset('awgscope_traces_x', (number_of_traces,len(awgscope_x)), data = awgscope_traces_x)
        savefile.create_dataset('awgscope_traces_y', (number_of_traces,len(awgscope_y)), data = awgscope_traces_y)