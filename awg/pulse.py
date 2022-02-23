# Data structure for one custom waveform pulse.

import numpy
from bokeh.models import Button, Toggle, TextInput
from bokeh.layouts import row
from functools import partial

class Pulse:
    def __init__(self, amplitude, x_offset):
        self.amplitude = amplitude
        self.x_offset = x_offset
        self.linear_correction_coefficient = -0.3
        self.cubic_correction_coefficient = 0.005
        
    def get_pulse(self):
        length = 4096
        start = -10
        end = start + length
        x = numpy.arange(start, end) / 1.428
        x = x - self.x_offset
        # x is not the time axis of the waveform. It is whatever necessary to make the waveform.
        
        w = ( (- numpy.tanh(x - 5) - numpy.tanh(-x - 5)) *
             (1 + self.linear_correction_coefficient*x + self.cubic_correction_coefficient*x**3) )
            
        w = w * self.amplitude / 1.8
        
        # Each data point of this waveform will be sampled by the AWG at some frequency,
        # so the time different between each data point is not necessarily 1 nanosecond,
        # 1.428 nanoseconds, etc. You should experimentally verify the sampling rate of
        # the AWG if you ever significantly change its configuration.
    
        return w
    
    def change_amplitude(self, plot_preview, attr, old, new):
        self.amplitude = float(new)
        plot_preview()
        
    def change_x_offset(self, plot_preview, attr, old, new):
        self.x_offset = float(new)
        plot_preview()
        
    def change_linear_correction_coefficient(self, plot_preview, attr, old, new):
        self.linear_correction_coefficient = float(new)
        plot_preview()
        
    def change_cubic_correction_coefficient(self, plot_preview, attr, old, new):
        self.cubic_correction_coefficient = float(new)
        plot_preview()
    
    def get_control_row(self, multipulse, index, plot_preview):
        amplitude_slider = TextInput(value = str(self.amplitude), title = "Amplitude (norm)")
        amplitude_slider.on_change('value', partial(self.change_amplitude, plot_preview))
        
        x_offset_slider = TextInput(value = str(self.x_offset), title = "X Offset (ns)")
        x_offset_slider.on_change('value', partial(self.change_x_offset, plot_preview))
        
        linear_correction_coefficient_slider = TextInput(value = str(self.linear_correction_coefficient), title = 'Linear Coefficient')
        linear_correction_coefficient_slider.on_change('value', partial(self.change_linear_correction_coefficient, plot_preview))
        
        cubic_correction_coefficient_slider = TextInput(value = str(self.cubic_correction_coefficient), title = 'Cubic Coefficient')
        cubic_correction_coefficient_slider.on_change('value', partial(self.change_cubic_correction_coefficient, plot_preview))
        
        remove_button = Button(label = 'Remove', align = 'end')
        remove_button.on_click(partial(multipulse.remove_pulse, index, plot_preview))
        
        therow = row(amplitude_slider, x_offset_slider, linear_correction_coefficient_slider, cubic_correction_coefficient_slider, remove_button)
        therow.width = 700
        
        return therow
        