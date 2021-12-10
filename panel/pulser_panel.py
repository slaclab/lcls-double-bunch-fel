from bokeh.models import Div, Button, ColumnDataSource
from bokeh.layouts import column, row, grid
from bokeh.plotting import figure
from functools import partial
import base64
from bokeh.models import Range1d, Spinner, TextAreaInput
import scope.pulserscope

class PulserPanel:
    def __init__(self):
        self.pulserscope_figure_source = ColumnDataSource()
        self.pulserscope_figure_source.data = dict(x=[], y=[])
        self.pulserscope_figure = figure(title = 'Pulser Scope', x_axis_label = 'Nanoseconds', y_axis_label = 'Volt')
        self.pulserscope_figure.line(source = self.pulserscope_figure_source)
        self.pulserscope_figure.height = 300
        
        self.pulserscope_image = Div(height = 480)
        
    def get_pulserscope_image(self):
        png = scope.pulserscope_image.get()
        data_uri = base64.b64encode(png).decode('ascii')
        img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        self.pulserscope_image.text = img_tag
        
    def plot_pulserscope(self):
        sec_list, volt_list = scope.pulserscope.get_nanosec_volt_lists()
        self.pulserscope_figure_source.data = dict(x = sec_list, y = volt_list)
        
    def get_controls(self):
        plot_pulserscope_button = Button(label='Plot Pulser Scope')
        plot_pulserscope_button.on_click(self.plot_pulserscope)
        
        pulserscope_image_button = Button(label = 'Get Pulser Scope Image')
        pulserscope_image_button.on_click(self.get_pulserscope_image)
        
        return self.pulserscope_figure, self.pulserscope_image, plot_pulserscope_button, pulserscope_image_button
        
    def addto(self, savefile, number_of_traces):
        pulserscope_traces_x = list()
        pulserscope_traces_y = list()
        pulserscope_x, pulserscope_y = scope.pulserscope.get_nanosec_volt_lists()
        
        for index in range(number_of_traces):
            pulserscope_x, pulserscope_y = scope.pulserscope.get_nanosec_volt_lists()
            pulserscope_traces_x.append(pulserscope_x)
            pulserscope_traces_y.append(pulserscope_y)

        savefile.create_dataset('pulserscope_traces_x', (number_of_traces,len(pulserscope_x)), data = pulserscope_traces_x)
        savefile.create_dataset('pulserscope_traces_y', (number_of_traces,len(pulserscope_y)), data = pulserscope_traces_y)