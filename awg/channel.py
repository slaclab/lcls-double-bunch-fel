# Data structure for multiple pulses, sent to the AWG, sent to the amplifiers.

from functools import partial
import base64

import numpy
from bokeh.layouts import column
from bokeh.models import Div, Button, ColumnDataSource, TextInput
from bokeh.layouts import column, row, grid
from bokeh.plotting import figure
from bokeh.models import Range1d, Spinner, TextAreaInput

import awg.pulse

class Channel:
    """
    Each channel is made of multiple pulses.
    """
    def __init__(self, awgg, trigger, channel):
        self.awg = awgg
        self.trigger = trigger
        self.channel = channel
        self.list_of_pulse = [awg.pulse.Pulse(0, 0)]
        
        self.preview_figure_source = ColumnDataSource()
        self.preview_figure_source.data = dict(x = [], y = [])
        self.preview_figure = figure(title = 'Preview', x_axis_label = 'Nanoseconds', y_axis_label = 'Volt')
        self.preview_figure.line(source = self.preview_figure_source)
        self.preview_figure.x_range = Range1d(0, 400)
        self.preview_figure.height = 300
        
        self.column = column()
        
    def get_awg_waveform(self):
        """
        Get the waveform to send to the AWG. The x axis should match the time difference 
        between each waveform data point. The waveform is 4096 floats in the range  [0, 2^16].
        The range [0, 2^16] maps to [-0.25 Volt, 0.25 Volt]. The waveform is sampled at 1.428 GHz. 
        """
        
        w = self.list_of_pulse[0].get_pulse()
        
        for pulse in self.list_of_pulse[1:]:
            next_w = pulse.get_pulse()
            w += next_w
            
        # Make the waveform compatible with the AWG input parameters.
        # Basically, a big array of integers with range from 0 to 2^16.
        # 0 is -0.25 V and 2^16 is 0.25 V. Amperage unknown.
            
        max_dac = 2 ** 16
        half_dac = 2 ** 15
        quarter_dac = 2 ** 14

        # Move the "0 Volt" value to 2^15.
        w = w * quarter_dac + half_dac
        # Round the double to the nearest digit.
        w = numpy.round(w)
        # These values should be from 0 to 2^16. Clip for safety.
        w = numpy.clip(w, 0, max_dac)
        # Convert from double to int.
        w = w.astype(numpy.uint16)
        
        # Time between data points is NOT 1 nanosecond, and the units of each value is NOT Volts.
        return w
    
    def get_preview_waveform(self):
        # Preview what the AWG will output to the amplifier.
        # Units of nanosecond - Volt.
        
        # Scale the waveform to units of nanosecond and Volt to preview 
        # what the output waveform should look like in theory.
        w = self.get_awg_waveform()
        
        # x is the time axis of the waveform
        x = numpy.arange(0, len(w)) / 1.428
                
        # The range [0, 2^16] maps to the range [-0.25 Volt, 0.25 Volt].
        w = (w / 2 ** 17) - 0.25
        
        # x is the time axis in nanoseconds, and w is volt axis in units of volts.
        return x, w
    
    def plot_preview(self):
        preview_x, preview_y = self.get_preview_waveform()
        self.preview_figure_source.data = dict(x = preview_x, y = preview_y)
        
    def add_default_pulse(self, frickin_width):  
        default_pulse = awg.pulse.Pulse(0, 0)
        pindex = len(self.list_of_pulse)
        self.list_of_pulse.append(default_pulse)
        control_row = default_pulse.get_control_row(pindex, frickin_width)
        self.column.children.append(control_row)
    
    def change_trigger(self, attr, old, new):
        self.trigger = new
        
    def change_channel(self, attr, old, new):
        self.channel = new
        
    def get_control_column(self, frickin_width):
        channel_input = TextInput(title = 'Channel', align = 'end', value = self.channel)
        channel_input.on_change('value', self.change_channel)
        
        trigger_input = TextInput(title = 'Trigger', align = 'end', value = self.trigger)
        trigger_input.on_change('value', self.change_trigger)

        stop_button = Button(label='Stop Channel', align = 'end')
        stop_button.on_click(partial(self.awg.stop, self))

        start_button = Button(label='Start Channel', align = 'end')
        start_button.on_click(partial(self.awg.start, self))
        
        add_pulse_button = Button(label = 'Add pulse', align = 'end')
        add_pulse_button.on_click(partial(self.add_default_pulse, frickin_width))
        
        control_row = row(channel_input, trigger_input, stop_button, start_button, add_pulse_button)
        control_row.width = frickin_width
        
        self.column.children.append(control_row)

        for pindex, pulse in enumerate(self.list_of_pulse):
            control_row = pulse.get_control_row(self, pindex, frickin_width)
            self.column.children.append(control_row)
            
        self.plot_preview()
        
        return row(self.column, self.preview_figure)
    
    def remove_pulse(self, pindex, frickin_width):
        if len(self.list_of_pulse) > 1:
            del self.list_of_pulse[pindex]
            self.column.children.clear()
            self.get_control_column(frickin_width)
            self.plot_preview()