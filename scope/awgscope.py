import pyvisa
import numpy
from struct import unpack

def get_scope_lib():
    # Return the pyvisa scope so we can get data and images from it.

    scope_manual_ip = '192.168.1.123'
    rm = pyvisa.ResourceManager()
    lib = rm.visalib
    scope = rm.open_resource('TCPIP::' + scope_manual_ip + '::INSTR')
    
    return scope, lib
    
def get_nanosec_volt_lists():
    # Given the pyvisa scope, get its curve where domain is nanoseconds and range is volts. It is 
    # important that the time axis is correct.
    
    scope, lib = get_scope_lib()
    
    scope.write('DATA:SOURCE CH1')
    scope.write('DATA:WIDTH 1')
    scope.write('DATA:ENC RPB')
    
    ymult = float(scope.query('WFMPRE:YMULT?'))
    yzero = float(scope.query('WFMPRE:YZERO?'))
    yoff = float(scope.query('WFMPRE:YOFF?'))
    xincr = float(scope.query('WFMPRE:XINCR?'))
    xzero = float(scope.query('WFMPRE:XZERO?'))
    
    scope.write("curve?")
    data = scope.read_raw()
    headerlen = 2 + int(data[1])
    ADC_wave = data[headerlen:-1]
    ADC_wave = numpy.array(unpack('%sB' % len(ADC_wave), ADC_wave))
    
    # Move and scale the y axis to Volts.
    y = (ADC_wave - yoff) * ymult + yzero
    
    # Move and scale the x axis to seconds.
    x = numpy.arange(0, xincr*len(y), xincr) + xzero
    
    # Scale the x axis from seconds to nanoseconds.
    x = x * 1e9
    
    return x, y
