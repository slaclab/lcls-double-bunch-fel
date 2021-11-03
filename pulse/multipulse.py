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
        newpulse = pulse.pulse.Pulse(1, 0)
        index = len(self.list_of_pulse)
        self.list_of_pulse.append(newpulse)
        
        control_row = newpulse.get_control_row()
        remove_button = Button(label='Remove')
        remove_button.on_click(partial(self.remove_pulse, multipulse_column, index))
        control_row.children.append(remove_button)
        multipulse_column.children.append(control_row)
        
    def remove_pulse(self, multipulse_column, index):
        # Ensure there is one pulse to send into the AWG.
        if len(self.list_of_pulse) > 0:
            del multipulse_column.children[index]
            del self.list_of_pulse[index]
        
    def get_controls(self):
        multipulse_column = column()
        
        for index, pulse in enumerate(self.list_of_pulse):
            control_row = pulse.get_control_row()
            remove_button = Button(label='Remove')
            remove_button.on_click(partial(self.remove_pulse, multipulse_column, index))
            control_row.children.append(remove_button)
            multipulse_column.children.append(control_row)
        
        add_pulse_button = Button(label='Add pulse')
        add_pulse_button.on_click(partial(self.add_default_pulse, multipulse_column))        

        return add_pulse_button, multipulse_column
        
    def get_multipulse(self):
        waveform = self.list_of_pulse[0].get_pulse()
        
        for pulse in self.list_of_pulse[1:]:
            waveform += pulse.get_pulse()
            
        # Make the waveform compatible with the AWG input parameters.
        # Basically, a big array of integers with range from 0 to 64000.
        # 0 is -0.25 V and 64000 is 0.25 V. Amperage unknown.
            
        max_dac = 2 ** 16
        half_dac = 2 ** 15
        quarter_dac = 2 ** 14

        # Move the "0 Volt" value to 32000.
        waveform = waveform * quarter_dac + half_dac
        # Round the double to the nearest digit.
        waveform = numpy.round(waveform)
        # These values should be from 0 to 64000. Clip for safety.
        waveform = numpy.clip(waveform, 0, max_dac)
        # Convert from double to int.
        waveform = waveform.astype(numpy.uint16)
            
        return waveform