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
        
    def add_default_pulse(self, multipulse_column, plot_preview):  
        default_pulse = pulse.pulse.Pulse(0, 0)
        index = len(self.list_of_pulse)
        self.list_of_pulse.append(default_pulse)
        remove_button = Button(label = 'Remove')
        remove_button.on_click(partial(self.remove_pulse, multipulse_column, index, plot_preview))
        control_row = default_pulse.get_control_row(plot_preview)
        control_row.children.append(remove_button)
        multipulse_column.children.append(control_row)
        
    def get_add_button(self, multipulse_column, plot_preview):
        add_pulse_button = Button(label = 'Add pulse')
        add_pulse_button.on_click(partial(self.add_default_pulse, multipulse_column, plot_preview))
        
        return add_pulse_button
        
    def add_controls_to(self, multipulse_column, plot_preview):        
        for index, pulse in enumerate(self.list_of_pulse):
            remove_button = Button(label = 'Remove')
            remove_button.on_click(partial(self.remove_pulse, multipulse_column, index, plot_preview))
            control_row = pulse.get_control_row(plot_preview)
            control_row.children.append(remove_button)

            multipulse_column.children.append(control_row)
    
    def remove_pulse(self, multipulse_column, index, plot_preview):
        if len(self.list_of_pulse) > 1:
            del self.list_of_pulse[index]
            # The indices break on the other ones.
            # Just delete everything and remake the controls so the indices are correct.
            # Not exquisite programming.
            multipulse_column.children.clear()
            self.add_controls_to(multipulse_column, plot_preview)
        
    def get_awg_waveform(self):
        # Get the waveform to send to the AWG.
        # The waveform is 4096 floats in the range  [0, 2^16].
        # The range [0, 2^16] maps to [-0.25 Volt, 0.25 Volt].
        # The waveform is sampled at 1.428 GHz. 
        
        w = self.list_of_pulse[0].get_pulse()
        
        for pulse in self.list_of_pulse[1:]:
            next_waveform = pulse.get_pulse()
            w += next_waveform
            
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
            
        return w
    
    def get_preview_waveform(self):
        # Preview what the AWG will output to the amplifier.
        # Units of nanosecond - Volt.
        
        # Scale the waveform to units of nanosecond and Volt to preview 
        # what the output waveform should look like in theory.
        w = self.get_awg_waveform()
        
        # The time between each x data point is 1 / 1.428 GHz.
        # This works, somehow.
        x = numpy.arange(0, len(w)) / 1.428
        
        # The range [0, 2^16] maps to the range [-0.25 Volt, 0.25 Volt].
        w = (w / 2 ** 17) - 0.25
        
        return x, w