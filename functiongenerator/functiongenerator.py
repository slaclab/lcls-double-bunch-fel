# Control the SRS DG645 function generator. Pretty important. Delay the trigger, delay the pulser, match the electron bunches. Programatically the same as the oscilloscopes.

import pyvisa
import numpy

class FunctionGenerator:
    def __init__(self):
        pass
    
    def get_resource(self):
        scope_manual_ip = '192.168.1.125'
        rm = pyvisa.ResourceManager()
        resource = rm.open_resource('TCPIP::' + scope_manual_ip + '::INSTR')
        
        return resource

    def set_delay(self, delay_nanoseconds):
        # Page 56 https://www.thinksrs.com/downloads/pdfs/manuals/DG645m.pdf
        
        resource = self.get_resource()

        resp = resource.query('*IDN?')
        print('Got the function generator. Response', resp)
        
<<<<<<< HEAD
        #resp = resource.write('IFRS 2')
        #print(resp)
        
=======
>>>>>>> b99c02f (2022 02 18 B15 Test Code)
        resp = resource.query('DLAY?2')
        print(resp)
        
        delay_command = f'DLAY 4,0,{delay_nanoseconds}e-9'
        resp = resource.write(delay_command)
        
<<<<<<< HEAD
        print(resp)
=======
    def find_delay(self, scope):
        # Given some VISA resource of the oscilloscope, measure the difference between 
        pass
>>>>>>> b99c02f (2022 02 18 B15 Test Code)
