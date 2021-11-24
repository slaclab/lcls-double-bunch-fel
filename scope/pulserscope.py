import numpy as np
import sys
import optparse
import argparse
import signal
import os
import shutil
import time
import pyvisa

def get_nanosec_volt_lists():
    # Get nanosecond-Volt data from Tektronix TDS 7154.
    # Previously we used floppy disks.
    
    visa_address = 'TCPIP::192.168.1.124::INSTR'

    rm = pyvisa.ResourceManager()
    scope = rm.open_resource(visa_address)
    scope.timeout = 10000 # ms
    scope.encoding = 'latin_1'
    scope.read_termination = '\n'
    scope.write_termination = None
    #scope.write('*cls') # clear ESR
    scope.write('header OFF') # disable attribute echo in replies

    print(scope.query('*idn?'))

    # default setup
    #scope.write('*rst')
    r = scope.query('*opc?') # sync
    
    r = scope.query('*opc?')

    # acquisition
    #scope.write('acquire:state OFF') # stop
    #scope.write('acquire:stopafter SEQUENCE;state ON') # single
    #r = scope.query('*opc?')

    # curve configuration
    #scope.write('data:encdg SRIBINARY') # signed integer
    scope.write('data:source CH1')
    scope.write('data:start 1')
    acq_record = int(scope.query('horizontal:recordlength?'))
    scope.write('data:stop {}'.format(acq_record))
    #scope.write('wfmoutpre:byt_n 1') # 1 byte per sample

    # data query
    bin_wave = scope.query_binary_values('curve?', datatype='b', container=np.array)

    # retrieve scaling factors
    wfm_record = int(scope.query('wfmoutpre:nr_pt?'))
    pre_trig_record = int(scope.query('wfmoutpre:pt_off?'))
    t_scale = float(scope.query('wfmoutpre:xincr?'))
    t_sub = float(scope.query('wfmoutpre:xzero?')) # sub-sample trigger correction
    v_scale = float(scope.query('wfmoutpre:ymult?')) # volts / level
    v_off = float(scope.query('wfmoutpre:yzero?')) # reference voltage
    v_pos = float(scope.query('wfmoutpre:yoff?')) # reference position (level)

    # error checking
    r = int(scope.query('*esr?'))
    print('event status register: 0b{:08b}'.format(r))
    r = scope.query('allev?').strip()
    print('all event messages: {}'.format(r))

    # disconnect
    scope.close()
    rm.close()

    # create scaled vectors
    # horizontal (time)
    total_time = t_scale * wfm_record
    t_start = (-pre_trig_record * t_scale) + t_sub
    t_stop = t_start + total_time
    scaled_time = np.linspace(t_start, t_stop, num=wfm_record, endpoint=False)
    # vertical (voltage)
    unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion
    scaled_wave = (unscaled_wave - v_pos) * v_scale + v_off
    
    print(scaled_time, scaled_wave)

    return scaled_time, scaled_wave