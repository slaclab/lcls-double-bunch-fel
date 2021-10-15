import numpy

class PulseInfo:
    def __init__(self, amplitude, x_offset):
        # amplitude: double from 0 to 1
        # x_offset: int from ? to ?
        self.amplitude = amplitude
        self.x_offset = x_offset
        
    def get_pulse(self):
        segLen = 4096
        x = numpy.linspace(-10, 4000, segLen)
        xo = x + self.x_offset
        y = ( (- numpy.tanh(xo - 5) - numpy.tanh(-xo - 5)) * (1 - 0.3*xo + 0.005*xo**3) ) / 1.8
        ya = y * self.amplitude
        
        return ya
        
class Waveform:
    def __init__(self, list_of_pulseinfo):
        # list_of_pulseinfo: list of at least one PulseInfo
        self.list_of_pulseinfo = list_of_pulseinfo
        
    # def get_base_waveform might be good idea so that we have base case
        
    def get_waveform(self):
        list_of_pulse = []
        
        for pulseinfo in self.list_of_pulseinfo:
            list_of_pulse.append(pulseinfo.get_pulse())
            
        waveform = list_of_pulse[0]
        
        for pulse in list_of_pulse[1:]:
            waveform += pulse
            
        return waveform