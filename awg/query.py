import os
import sys
srcpath = os.path.realpath('tabor')
sys.path.append(srcpath)
import pyte_visa_utils as pyte
from tevisainst import TEVisaInst

#internal
inst_addr = 'TCPIP::127.0.0.1::5025::SOCKET'
#usb cable
#inst_addr = 'TCPIP::192.168.71.1::5025::SOCKET'
  
inst = TEVisaInst(inst_addr)

ch = 1
segnum = 1

# Select channel
cmd = ':INST:CHAN {0}'.format(ch)
rc = inst.send_scpi_cmd(cmd)

# Channel is selected. Make the query you want.

resp = inst.send_scpi_query(":TRIG:LTJ?")

print("Resp: " + resp)

cmd = "FREQ:SOUR EXT"
rc = inst.send_scpi_cmd(cmd)