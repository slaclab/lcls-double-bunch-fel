import numpy
from bokeh.models import Button, Slider, Toggle
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
        end = start + length - 1
        x = numpy.linspace(start, end, length)
        x = x - self.x_offset
        
        y = ( (- numpy.tanh(x - 5) - numpy.tanh(-x - 5)) *
             (1 + self.linear_correction_coefficient*x + self.cubic_correction_coefficient*x**3) )
            
        y = y * self.amplitude / 1.8
    
        return x, y
    
    def change_amplitude(self, attr, old, new):
        self.amplitude = new
        
    def change_x_offset(self, attr, old, new):
        self.x_offset = new
        
    def change_linear_correction_coefficient(self, attr, old, new):
        self.linear_correction_coefficient = new
        
    def change_cubic_correction_coefficient(self, attr, old, new):
        self.cubic_correction_coefficient = new 
    
    def get_control_row(self):
        amplitude_slider = Slider(start = -1, end = 1, value = self.amplitude, step = 0.01, title = "Amplitude")
        amplitude_slider.on_change('value', self.change_amplitude)
        amplitude_slider.width = 150
        
        x_offset_slider = Slider(start = 0, end = 200, value = self.x_offset, step = 1, title = "X Offset")
        x_offset_slider.on_change('value', self.change_x_offset)
        x_offset_slider.width = 150
        
        linear_correction_coefficient_slider = Slider(start = -0.5, end = 0,
                                                      value = self.linear_correction_coefficient,
                                                      step = 0.1,
                                                      title = 'Linear Correction Coefficient')
        linear_correction_coefficient_slider.on_change('value', self.change_linear_correction_coefficient)
        linear_correction_coefficient_slider.width = 200
        
        cubic_correction_coefficient_slider = Slider(start = 0, end = 0.01,
                                                     value = self.cubic_correction_coefficient,
                                                     step = 0.001,
                                                     format = '0[.]000',
                                                     title = 'Cubic Correction Coefficient')
        cubic_correction_coefficient_slider.on_change('value', self.change_cubic_correction_coefficient)
        cubic_correction_coefficient_slider.width = 200
                
        return row(amplitude_slider, x_offset_slider, linear_correction_coefficient_slider, cubic_correction_coefficient_slider)
        