import numpy as np
import sys
import optparse
import argparse
import signal
import os
import shutil
import time
import numpy
import pyvisa

def get_nanosec_volt_lists(channel):
    # Get data from the short repetition rate pulser oscilloscope.
    # Tektronix TDS 7154.
    # Previously we used floppy disks.
    
    # Needs to be set manually.
    visa_address = 'TCPIP::192.168.1.101::INSTR'

    rm = pyvisa.ResourceManager()
    scope = rm.open_resource(visa_address)
    scope.timeout = 10000 # ms
    scope.encoding = 'latin_1'
    scope.read_termination = '\n'
    scope.write_termination = None
    #scope.write('*cls') # clear ESR
    scope.write('header OFF') # disable attribute echo in replies

    print('Getting trace from', scope.query('*idn?'))

    # default setup
    r = scope.query('*opc?') # sync

    # curve configuration
    scope.write('data:source {0}'.format(channel))
    scope.write('data:start 1')
    acq_record = int(scope.query('horizontal:recordlength?'))
    scope.write('data:stop {}'.format(acq_record))
    scope.write('wfmoutpre:byt_n 2')

    # data query
    bin_wave = scope.query_binary_values('curve?', datatype='b', container=np.array)

    # retrieve scaling factors
    nr_pt = int(scope.query('wfmoutpre:nr_pt?'))
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
    duration = t_scale * nr_pt
    t_start = (-pre_trig_record * t_scale) + t_sub
    t_stop = t_start + duration
    scaled_time = np.linspace(t_start, t_stop, num=nr_pt, endpoint=False)
    # vertical (voltage)
    unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion
    scaled_volt = (unscaled_wave - v_pos) * v_scale + v_off
    
    scaled_time_nanoseconds = numpy.asarray(scaled_time) * 1e9

    return scaled_time_nanoseconds, scaled_volt