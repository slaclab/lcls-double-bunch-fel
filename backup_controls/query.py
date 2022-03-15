import os
import sys
srcpath = os.path.realpath('SourceFiles')
sys.path.append(srcpath)
import socket

import numpy as np

import pyte_visa_utils as pyte
from tevisainst import TEVisaInst

def get_instrument():
    ip = socket.gethostbyname('UFK21-9')
    addr = f'TCPIP::{ip}::5025::SOCKET'
    instrument = TEVisaInst(addr)

    return instrument

def query(instrument, query_string):
    resp = instrument.send_scpi_query(query_string)
    print(query_string, resp)
    return resp
    
def command(instrument, command_string):
    resp = instrument.send_scpi_cmd(command_string)
    resp = instrument.send_scpi_query(':SYST:ERR?')
    print(command_string, 'error', resp)
    
inst = get_instrument()

for i in [1, 2]:
    print(f'Channel {i}')
    
    ch = i
    segnum = i

    # Select channel
    cmd = ':INST:CHAN {0}'.format(ch)
    rc = inst.send_scpi_cmd(cmd)

    # Channel is selected. Make the query you want.
    
    query(inst, ":OUTP?")
    query(inst, ":FREQ:RAST?")
    query(inst, ":FREQ:SOUR?")
    query(inst, ":FREQ?")
    query(inst, ":VOLT?")
    