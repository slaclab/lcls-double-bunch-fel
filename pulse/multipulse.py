import pulse.pulse
from bokeh.layouts import column
from bokeh.models import Button
from functools import partial
import numpy

class Multipulse:
    def __init__(self):        
        self.list_of_pulse = [pulse.pulse.Pulse(-0.5, 0),
                              pulse.pulse.Pulse(-0.7, 50),
                              pulse.pulse.Pulse(-0.4, 100),
                              pulse.pulse.Pulse(-0.9, 150)]
        
    def add_default_pulse(self, multipulse_column):  
        default_pulse = pulse.pulse.Pulse(0, 0)
        index = len(self.list_of_pulse)
        self.list_of_pulse.append(default_pulse)
        remove_button = Button(label = 'Remove')
        remove_button.on_click(partial(self.remove_pulse, multipulse_column, index))
        control_row = default_pulse.get_control_row()
        control_row.children.append(remove_button)
        multipulse_column.children.append(control_row)
        
    def get_add_button(self, multipulse_column):
        add_pulse_button = Button(label = 'Add pulse')
        add_pulse_button.on_click(partial(self.add_default_pulse, multipulse_column))
        
        return add_pulse_button
        
    def add_controls_to(self, multipulse_column):        
        for index, pulse in enumerate(self.list_of_pulse):
            remove_button = Button(label = 'Remove')
            remove_button.on_click(partial(self.remove_pulse, multipulse_column, index))
            control_row = pulse.get_control_row()
            control_row.children.append(remove_button)

            multipulse_column.children.append(control_row)
    
    def remove_pulse(self, multipulse_column, index):
        if len(self.list_of_pulse) > 1:
            del self.list_of_pulse[index]
            # The indices break on the other ones.
            # Just delete everything and remake the controls so the indices are correct.
            # Not exquisite programming.
            multipulse_column.children.clear()
            self.add_controls_to(multipulse_column)
        
    def get_awg_waveform(self):
        # Get the waveform to send to the AWG.
        x, y = self.list_of_pulse[0].get_pulse()
        
        for pulse in self.list_of_pulse[1:]:
            next_x, next_y = pulse.get_pulse()
            y += next_y
            
        # Make the waveform compatible with the AWG input parameters.
        # Basically, a big array of integers with range from 0 to 2^16.
        # 0 is -0.25 V and 2^16 is 0.25 V. Amperage unknown.
            
        max_dac = 2 ** 16
        half_dac = 2 ** 15
        quarter_dac = 2 ** 14

        # Move the "0 Volt" value to 2^15.
        y = y * quarter_dac + half_dac
        # Round the double to the nearest digit.
        y = numpy.round(y)
        # These values should be from 0 to 2^16. Clip for safety.
        y = numpy.clip(y, 0, max_dac)
        # Convert from double to int.
        y = y.astype(numpy.uint16)
            
        return x, y
    
    def get_preview_waveform(self):
        # Scale the input waveform to units of nanosecond and Volt to preview 
        # what the output waveform should look like in theory.  
        x, y = self.get_awg_waveform()
        
        # Each sample is scaled by 1 Gigasample per second. Therefore the domain x
        # is in units of nanoseconds, which is what we want to plot. But the domain is shifted
        # to -10 so shift it back.
        x = x + 10
        
        # The range [0, 2^16] maps to the range [-0.25 Volt, 0.25 Volt].
        y = (y / 2 ** 17) - 0.25
        
        return x, y