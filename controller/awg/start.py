import os
import sys
import numpy
from controller.awg.tabor.tevisainst import TEVisaInst
import controller.awg.pulse

def start_waveform(list_of_pulseinfo):
    # Assuming this code runs on the Windows machine inside the AWG.
    inst_addr = 'TCPIP::127.0.0.1::5025::SOCKET'
    inst = TEVisaInst(inst_addr)

    # Always print debug info.
    resp = inst.send_scpi_query('*IDN?')
    print('Connected to: ' + resp)
    resp = inst.send_scpi_query(":SYST:iNF:MODel?")
    print("Model: " + resp)
    resp = inst.send_scpi_query(":INST:CHAN? MAX")
    print("Number of channels: " + resp)
    num_channels = int(resp)

    # Set the sample frequency to 1 GHz.
    sampleRateDAC = 1E9
    print('Sample Clk Freq {0}'.format(sampleRateDAC))
    cmd = ':FREQ:RAST {0}'.format(sampleRateDAC)
    rc = inst.send_scpi_cmd(cmd)

    # Enable external clock EXT from the function generator.
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
    
    waveform = controller.awg.pulse.Waveform(list_of_pulseinfo)
    y = waveform.get_waveform()

    max_dac = 2 ** 16 - 1
    half_dac = 2 ** 16 - 1
    quarter_dac = 2 ** 14 - 1
    data_type = numpy.uint16
    # Normalize it to the maximum the DAC can receive.
    y =  y * quarter_dac + 2**15#+ half_dac
    # Round the double to the nearest digit.
    y = numpy.round(y)
    # For safety, clip the data assuming the code is somehow faulty.
    y = numpy.clip(y, 0, max_dac)
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
    if resp[0] == '0': print('Download Succesful')
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
    cmd = ':TRIG:LEV 0.25'
    rc = inst.send_scpi_cmd(cmd)

    # Following the trigger, send :TRIG:COUN number of waveforms, then return to idle.
    cmd = ':TRIG:COUN 1'
    rc = inst.send_scpi_cmd(cmd)

    # In case something incorrectly sends another trigger, keep sending the :TRIG:COUN number of waveforms.
    cmd = ':TRIG:IDLE DC'
    rc = inst.send_scpi_cmd(cmd)

    # I believe there is no :TRIG:STAT command.
    cmd = ':TRIG:STAT ON'
    rc = inst.send_scpi_cmd(cmd)

    # Disable continuous (aka free-running) mode, and force trigger mode.
    cmd = ':INIT:CONT OFF'
    rc = inst.send_scpi_cmd(cmd)

    # Turn on the output of the selected channel.
    cmd = ':OUTP ON'
    rc = inst.send_scpi_cmd(cmd)