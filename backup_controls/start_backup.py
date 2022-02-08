import os
import sys
srcpath = os.path.realpath('../SourceFiles')
sys.path.append(srcpath)
import pyte_visa_utils as pyte
from tevisainst import TEVisaInst

import numpy as np

#internal
inst_addr = 'TCPIP::127.0.0.1::5025::SOCKET'
#usb cable
#inst_addr = 'TCPIP::192.168.71.1::5025::SOCKET'
  
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

# set sampling DAC freq.
sampleRateDAC = 1E9
print('Sample Clk Freq {0}'.format(sampleRateDAC))
cmd = ':FREQ:RAST {0}'.format(sampleRateDAC)
rc = inst.send_scpi_cmd(cmd)

# Get the maximal number of segments
resp = inst.send_scpi_query(":TRACe:SELect:SEGMent? MAX")
print("Max segment number: " + resp)
max_seg_number = int(resp)

# Get the available memory in bytes of wavform-data (per DDR):
resp = inst.send_scpi_query(":TRACe:FREE?")
arbmem_capacity = int(resp)
print("Available memory per DDR: {0:,} wave-bytes".format(arbmem_capacity))

dac_res = 16
max_dac = 2 ** dac_res - 1
half_dac = max_dac / 2.0
data_type = np.uint16

amp = 1    
segLen = 4096
cycles = 100
time = np.linspace(0, segLen-1, segLen)
omega = 2 * np.pi * cycles
dacWave = (np.sin(omega*time/segLen) + 1.0) * half_dac
dacWave = np.round(dacWave)
dacWave = np.clip(dacWave, 0, max_dac)
dacWave = dacWave.astype(data_type)

ch=1
segnum = 1
print('Download wave to segment {0} of channel {1}'.format(segnum, ch))

# Select channel
cmd = ':INST:CHAN {0}'.format(ch)
rc = inst.send_scpi_cmd(cmd)

# Define segment
cmd = ':TRAC:DEF {0}, {1}'.format(segnum, len(dacWave))
rc = inst.send_scpi_cmd(cmd)

# Select the segment
cmd = ':TRAC:SEL {0}'.format(segnum)
rc = inst.send_scpi_cmd(cmd)

# Increase the timeout before writing binary-data:
inst.timeout = 30000
inst.write_binary_data('*OPC?; :TRAC:DATA', dacWave)
resp = inst.send_scpi_query(':SYST:ERR?')
if resp[0] == '0':
    print('Download Succesful')
else:
    print('NOT Successful')
    print(resp)

# Set normal timeout
inst.timeout = 10000


# Play the specified segment at the selected channel:
cmd = ':SOUR:FUNC:MODE:SEGM {0}'.format(segnum)
rc = inst.send_scpi_cmd(cmd)

#Enable Ext Trigger
cmd = ':TRIG:SOUR:ENAB TRG1'
rc = inst.send_scpi_cmd(cmd)
cmd = ':TRIG:SEL EXT1'
rc = inst.send_scpi_cmd(cmd)
cmd = ':TRIG:LEV 0.1'
rc = inst.send_scpi_cmd(cmd)
cmd = ':TRIG:COUN 1'
rc = inst.send_scpi_cmd(cmd)
cmd = ':TRIG:IDLE DC'
rc = inst.send_scpi_cmd(cmd)
cmd = ':TRIG:STAT ON'
rc = inst.send_scpi_cmd(cmd)
cmd = ':INIT:CONT OFF'
rc = inst.send_scpi_cmd(cmd)

# Turn on the output of the selected channel:
cmd = ':OUTP ON'
rc = inst.send_scpi_cmd(cmd)