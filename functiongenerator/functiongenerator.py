# Control the SRS DG645 function generator. Pretty important. Delay the trigger, delay the pulser, match the electron bunches. Programatically the same as the oscilloscopes.

import time

import pyvisa
import numpy
from bokeh.models import TextInput, Button, Div
from bokeh.layouts import column, row, grid

class FunctionGenerator:
    def __init__(self):
        self.delay_nanoseconds = 0
        self.delay_start = 0
        self.delay_end = 0
    
    def get_resource(self):
        scope_manual_ip = '192.168.1.125'
        rm = pyvisa.ResourceManager()
        resource = rm.open_resource('TCPIP::' + scope_manual_ip + '::INSTR')
        
        return resource

    def set_delay(self, delay_nanoseconds):
        # Set the delay of trigger C relative to trigger A by the given nanoseconds.
        
        # Page 56 https://www.thinksrs.com/downloads/pdfs/manuals/DG645m.pdf
        
        resource = self.get_resource()

        resp = resource.query('*IDN?')
        print('Got the function generator. Response', resp)
        
        resp = resource.query('DLAY?2')
        print(resp)
        
        delay_command = f'DLAY 2,0,{delay_nanoseconds}e-9'
        resp = resource.write(delay_command)
        
    def change_delay(self, attr, old, new):
        self.delay_nanoseconds = float(new)
        self.set_delay(new)
        
    def delay_start(self, attr, old, new):
        self.delay_start = int(new)
        
    def delay_end(self, attr, old, new):
        self.delay_end = int(new)
        
    def scan_delay(self):
        for i in range(self.delay_start, self.delay_end):
            self.set_delay(i)
            time.sleep(1)
    
    def get_controls(self, frickin_width):
        title = Div(text='<h3>Function Generator</h3>')
        
        delay_inputbox = TextInput(title = "Delay (ns)")
        delay_inputbox.on_change('value', self.change_delay)
        
#         start_input = TextInput(title = "Delay Start (ns int)")
#         start_input.on_change('value', self.delay_start)
        
#         end_input = TextInput(title = "Delay Stop (ns int)")
#         end_input.on_change('value', self.delay_end)
        
#         scan_delay_button = Button(label = 'Scan Delay', align = 'end')
#         scan_delay_button.on_click(self.scan_delay)
        
        return column(title, row(delay_inputbox))