import os
import sys
from controller.awg.tabor import pyte_visa_utils as pyte
from controller.awg.tabor.tevisainst import TEVisaInst

import numpy

def stop_waveform():
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

    ch = 1

    # Select channel
    cmd = ':INST:CHAN {0}'.format(ch)
    rc = inst.send_scpi_cmd(cmd)

    # Turn on the output of the selected channel:
    cmd = ':OUTP OFF'
    rc = inst.send_scpi_cmd(cmd)