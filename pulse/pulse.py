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
        segLen = 4096
        x = numpy.linspace(-10, segLen - 11, segLen)
        xo = x - self.x_offset
        
        y = ( (- numpy.tanh(xo - 5) - numpy.tanh(-xo - 5)) ) / 1.8
        
        if self.correction:
            y = ( (- numpy.tanh(xo - 5) - numpy.tanh(-xo - 5)) * (1 - 0.3*xo + 0.005*xo**3) ) / 1.8
            
        ya = y * self.amplitude
    
        return ya
    
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
        