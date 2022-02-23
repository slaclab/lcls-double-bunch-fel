import os
import sys
<<<<<<< HEAD
srcpath = os.path.realpath('../SourceFiles')
=======
import numpy as np
srcpath = os.path.realpath('SourceFiles')
>>>>>>> b99c02f (2022 02 18 B15 Test Code)
sys.path.append(srcpath)
import pyte_visa_utils as pyte
from tevisainst import TEVisaInst

<<<<<<< HEAD
import numpy as np

=======
>>>>>>> b99c02f (2022 02 18 B15 Test Code)
#internal
#inst_addr = 'TCPIP::127.0.0.1::5025::SOCKET'
#usb cable
inst_addr = 'TCPIP::192.168.1.102::5025::SOCKET'
  
inst = TEVisaInst(inst_addr)

# Get the instrument's *IDN
resp = inst.send_scpi_query('*IDN?')
print('Connected to: ' + resp)

# Get the model name
resp = inst.send_scpi_query(":SYST:iNF:MODel?")
print("Model: " + resp)

# Get number of channels
resp = inst.send_scpi_query(":INST:CHAN? MAX")
print("Number of channels: " + resp)
num_channels = int(resp)

<<<<<<< HEAD


=======
>>>>>>> b99c02f (2022 02 18 B15 Test Code)
# set sampling DAC freq.
sampleRateDAC = 1E9
print('Sample Clk Freq {0}'.format(sampleRateDAC))
cmd = ':FREQ:RAST {0}'.format(sampleRateDAC)
rc = inst.send_scpi_cmd(cmd)

#Enable external clock EXT, internal clock INT
cmd = "FREQ:SOUR EXT"
rc = inst.send_scpi_cmd(cmd)

# Get the maximal number of segments
resp = inst.send_scpi_query(":TRACe:SELect:SEGMent? MAX")
print("Max segment number: " + resp)
max_seg_number = int(resp)

# Get the available memory in bytes of wavform-data (per DDR):
resp = inst.send_scpi_query(":TRACe:FREE?")
arbmem_capacity = int(resp)
print("Available memory per DDR: {0:,} wave-bytes".format(arbmem_capacity))

max_dac = 2 ** 16 - 1
half_dac = 2 ** 16 - 1
quarter_dac = 2 ** 14 - 1
data_type = np.uint16
segLen = 4096
x = np.linspace(-10, 4000, segLen)
# Make the function.
def single_waveform(x):
    return ( (- np.tanh(x-5) - np.tanh(-x-5)) * (1 - 0.3*x + 0.005*x**3) ) / 1.8 #(1 - 0.3*x + 0.005*x**3)

y = single_waveform(x) - 0.7 * single_waveform(x - 50) - 0.4 * single_waveform(x - 100) - 0.9 * single_waveform(x - 150) 

# Normalize it to the maximum the DAC can receive.
y =  y * quarter_dac + 2.01**15#+ half_dac
# Round the double to the nearest digit.
y = np.round(y)
# If the values are in the valid range, numpy.clip will not change the data.
y = np.clip(y, 0, max_dac)
# Convert from double to int.
y = y.astype(data_type)

ch = 1
segnum = 1
print('Download wave to segment {0} of channel {1}'.format(segnum, ch))

# Select channel
cmd = ':INST:CHAN {0}'.format(ch)
rc = inst.send_scpi_cmd(cmd)

# Define segment
cmd = ':TRAC:DEF {0}, {1}'.format(segnum, len(y))
rc = inst.send_scpi_cmd(cmd)

# Select the segment
cmd = ':TRAC:SEL {0}'.format(segnum)
rc = inst.send_scpi_cmd(cmd)

# Increase the timeout before writing binary-data:
inst.timeout = 30000
inst.write_binary_data('*OPC?; :TRAC:DATA', y)
resp = inst.send_scpi_query(':SYST:ERR?')
if resp[0] == '0':
    print('Download Succesful')
else:
    print('NOT SUCCESSFUL')
    print(resp)
    
# Set normal timeout
inst.timeout = 10000

# Play the specified segment at the selected channel:
cmd = ':SOUR:FUNC:MODE:SEGM {0}'.format(segnum)
rc = inst.send_scpi_cmd(cmd)

# Enable Ext Trigger
cmd = ':TRIG:SOUR:ENAB TRG1'
rc = inst.send_scpi_cmd(cmd)

# Select the external trigger 1.
cmd = ':TRIG:SEL EXT1'
rc = inst.send_scpi_cmd(cmd)

cmd = 'TRIG:LTJ ON'
rc = inst.send_scpi_cmd(cmd)

# Set the trigger level.
# This was originally 0, we had to change to 0.1.
cmd = ':TRIG:LEV 0.05'
rc = inst.send_scpi_cmd(cmd)

# Following the trigger, send :TRIG:COUN number of waveforms, then return to idle.
cmd = ':TRIG:COUN 1'
rc = inst.send_scpi_cmd(cmd)

# Keep sending the :TRIG:COUN number waveforms, even if another triggers appears. 
cmd = ':TRIG:IDLE DC'
rc = inst.send_scpi_cmd(cmd)

# There is no :TRIG:STAT command
cmd = ':TRIG:STAT ON'
rc = inst.send_scpi_cmd(cmd)

# Disable continuous (aka free-running) mode, and force trigger mode.
cmd = ':INIT:CONT OFF'
rc = inst.send_scpi_cmd(cmd)

# Turn on the output of the selected channel:
cmd = ':OUTP ON'
rc = inst.send_scpi_cmd(cmd)