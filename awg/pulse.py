# Data structure for one custom waveform pulse.

import numpy
from bokeh.models import Button, Toggle, TextInput
from bokeh.layouts import row
from functools import partial

class Pulse:
    """
    Each pulse makes one pulse that goes into one channel.
    """
    def __init__(self, amplitude, x_offset):
        self.amplitude = amplitude
        self.x_offset = x_offset
        self.linear_correction_coefficient = -0.3
        self.cubic_correction_coefficient = 0.005
        
    def get_pulse(self):
        """
        Make one array of 4096 floats in the range [-1, 1]. This represents one
        "pulse" that we want to send to the AWG on one channel.
        
        The AWG has multiple channels. Only one "waveform" can be sent out each channel per time.
        Each channel can have multiple "pulses" which it combines into one "waveform."
        """
        length = 4096
        start = -10
        end = start + length
        
        # We need x values in units of nanoseconds to offset
        x = numpy.arange(start, end) / 1.428 
        x = x - self.x_offset
        
        # Now squish it to make the risetime short
        x = x * 5
        w = ( (- numpy.tanh(x - 5) - numpy.tanh(-x - 5)) *
             (1 + self.linear_correction_coefficient*x + self.cubic_correction_coefficient*x**3) )
        
        # Normalize to [-1, 1], idk how to do this analytically.
        w = w * self.amplitude / 3.52
        
        return w
    
    def change_amplitude(self, channel, attr, old, new):
        self.amplitude = float(new)
        channel.plot_preview()
        
    def change_x_offset(self, channel, attr, old, new):
        self.x_offset = float(new)
        channel.plot_preview()
        
    def change_linear_coefficient(self, channel, attr, old, new):
        self.linear_correction_coefficient = float(new)
        channel.plot_preview()
        
    def change_cubic_coefficient(self, channel, attr, old, new):
        self.cubic_correction_coefficient = float(new)
        channel.plot_preview()
    
    def get_control_row(self, channel, pindex, frickin_width):
        amplitude_slider = TextInput(value = str(self.amplitude), title = "Amplitude (norm)")
        amplitude_slider.on_change('value', partial(self.change_amplitude, channel))
        
        x_offset_slider = TextInput(value = str(self.x_offset), title = "X Offset (ns)")
        x_offset_slider.on_change('value', partial(self.change_x_offset, channel))
        
        linear_coefficient_slider = TextInput(value = str(self.linear_correction_coefficient), title = 'Linear Coefficient')
        linear_coefficient_slider.on_change('value', partial(self.change_linear_coefficient, channel))
        
        cubic_coefficient_slider = TextInput(value = str(self.cubic_correction_coefficient), title = 'Cubic Coefficient')
        cubic_coefficient_slider.on_change('value', partial(self.change_cubic_coefficient, channel))
        
        remove_button = Button(label = 'Remove Pulse', align = 'end')
        remove_button.on_click(partial(channel.remove_pulse, pindex, frickin_width))
        
        therow = row(amplitude_slider, x_offset_slider, linear_coefficient_slider, cubic_coefficient_slider, remove_button)
        therow.width = frickin_width
        
        return therow
        