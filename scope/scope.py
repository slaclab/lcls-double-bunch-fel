"""
Get Bokeh elements to grab scope data, or scope image.
"""

from functools import partial
import base64

from bokeh.models import Button, Div, TextInput
from bokeh.models.sources import ColumnDataSource
from bokeh.layouts import column, row
from bokeh.plotting import figure
import h5py

import scope.smallscope_data
import scope.smallscope_image

def get_plot(data_function, channel, figure_source):
    sec_list, volt_list = data_function(channel.value)
    figure_source.data = dict(x = sec_list, y = volt_list)

def get_image(image_function, scope_image_element):
    png = image_function()
    data_uri = base64.b64encode(png).decode('ascii')
    img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
    scope_image_element.text = img_tag
    
def change_channel_value(channel_input, attr, old, new):
    channel_input.value = new

def get_controls(frickin_width):
    data_function = scope.smallscope_data.get
    image_function = scope.smallscope_image.get
    
    title = Div(text = '<h3>Oscilloscope</h3>')
    
    figure_source = ColumnDataSource()
    figure_source.data = dict(x = [], y = [])
    figure_element = figure(title = 'Scope', x_axis_label = 'Nanoseconds', y_axis_label = 'Volt')
    figure_element.line(source = figure_source)
    figure_element.height = 300
    scope_image_element = Div(height = 480)
    
    channel_input = TextInput(value = 'CH1', title = 'Channel')
    channel_input.on_change('value', partial(change_channel_value, channel_input))

    get_plot_button = Button(label = 'Plot Scope', align = 'end')
    get_plot_button.on_click(partial(get_plot, data_function, channel_input, figure_source))

    get_image_button = Button(label = 'Get Scope Image', align = 'end')
    get_image_button.on_click(partial(get_image, image_function, scope_image_element))
    
    control_row = row(channel_input, get_plot_button, get_image_button)
    control_row.width = frickin_width
    
    viz_column = column(figure_element, scope_image_element)
                              
    controls = column(title, row(control_row, viz_column))
                              
    return controls
                                             
# def addto(self, savefile, number_of_traces):        
#         channels = ['CH1']
        
#         for c in channels:
#             print('Measuring channel', c)
            
#             scope_traces_x = list()
#             scope_traces_y = list()
        
#             scope_x, scope_y = scope.smallscope.get_nanosec_volt_lists(c)

#             for index in range(number_of_traces):
#                 scope_x, scope_y = scope.smallscope.get_nanosec_volt_lists(c)
#                 scope_traces_x.append(scope_x)
#                 scope_traces_y.append(scope_y)

#             savefile.create_dataset(f'scope_traces_x_{c}', (number_of_traces,len(scope_x)), data = scope_traces_x)
#             savefile.create_dataset(f'scope_traces_y_{c}', (number_of_traces,len(scope_y)), data = scope_traces_y)