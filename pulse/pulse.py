import numpy
from bokeh.models import Button, Slider, Toggle
from bokeh.layouts import row
from functools import partial

class Pulse:
    def __init__(self, amplitude, x_offset):
        self.amplitude = amplitude
        self.x_offset = x_offset
        self.correction = True
        
    def get_pulse(self):
        length = 4096
        start = -10
        end = start + length - 1
        x = numpy.linspace(start, end, length)
        x = x - self.x_offset
        
        y = ( (- numpy.tanh(x - 5) - numpy.tanh(-x - 5)) ) / 1.8
        
        if self.correction:
            y = ( (- numpy.tanh(x - 5) - numpy.tanh(-x - 5)) * (1 - 0.3*x + 0.005*x**3) ) / 1.8
            
        y = y * self.amplitude
    
        return x, y
    
    def change_amplitude(self, attr, old, new):
        self.amplitude = new
        
    def change_x_offset(self, attr, old, new):
        self.x_offset = new
        
    def change_correction(self, new):
        self.correction = new
    
    def get_control_row(self):
        amplitude_slider = Slider(start = -1, end = 1, value = self.amplitude, step = 0.01, title = "Amplitude")
        amplitude_slider.on_change('value', self.change_amplitude)
        
        x_offset_slider = Slider(start = 0, end = 200, value = self.x_offset, step = 1, title = "X Offset")
        x_offset_slider.on_change('value', self.change_x_offset)
        
        correction_tickbox = Toggle(label = 'Correction', active = self.correction)
        correction_tickbox.on_click(self.change_correction)
                
        return row(amplitude_slider, x_offset_slider, correction_tickbox)
        