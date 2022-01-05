from awg.tabor.tevisainst import TEVisaInst

def start(multipulse):
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
    resp = inst.send_scpi_query(":TRACe:SELect:SEGMent? MAX")
    print("Max segment number: " + resp)
    resp = inst.send_scpi_cmd("*CLS")
    print("CLS response", resp)
    resp = inst.send_scpi_query(':SYST:ERR?')
    print('CLS error', resp)
    
    # I thought it was the rate at which the data points on the waveform were sampled, but this is wrong,
    # the rate at which the data points are sampled is 1.428 GHz which is the clock rate. What does this do?
    #cmd = ':FREQ:RAST 1E9'
    #rc = inst.send_scpi_cmd(cmd)
    #resp = inst.send_scpi_query(':SYST:ERR?')
    #print('Rast response', resp)

    # Get the available memory in bytes of wavform-data (per DDR):
    resp = inst.send_scpi_query(":TRACe:FREE?")
    arbmem_capacity = int(resp)
    print("Available memory per DDR: {0:,} wave-bytes".format(arbmem_capacity))

    # Set the channel and segment to send the waveform to.
    ch = 1
    segnum = 1
    print('Download wave to segment {0} of channel {1}'.format(segnum, ch))

    # Select channel.
    cmd = ':INST:CHAN {0}'.format(ch)
    rc = inst.send_scpi_cmd(cmd)
    
    # Get the waveform to send to the FPGA's memory.
    waveform = multipulse.get_awg_waveform()

    # Select segment and the number of samples to send to the segment. The clock samples
    # these data data points sequentially. The rate at which this sample is played 
    # is defined by :SOUR:FREQ:RAST (p. 66).
    cmd = ':TRAC:DEF {0}, {1}'.format(segnum, len(waveform))
    rc = inst.send_scpi_cmd(cmd)
    
    # Select the segment
    cmd = ':TRAC:SEL {0}'.format(segnum)
    rc = inst.send_scpi_cmd(cmd)

    # Mean time to write the waveform is 0.5 seconds. Set to 10 seconds.
    inst.timeout = 10000
    inst.write_binary_data('*OPC?; :TRAC:DATA', waveform)
    resp = inst.send_scpi_query(':SYST:ERR?')
    print('Write error', resp)

    # Play the specified segment at the selected channel:
    cmd = ':SOUR:FUNC:MODE:SEGM {0}'.format(segnum)
    rc = inst.send_scpi_cmd(cmd)
    
    # Enable external clock EXT from the Agilent N5181A.
    cmd = "FREQ:SOUR EXT"
    rc = inst.send_scpi_cmd(cmd)

    # Enable Ext Trigger
    cmd = ':TRIG:SOUR:ENAB TRG1'
    rc = inst.send_scpi_cmd(cmd)

    # Select the external trigger 1.
    cmd = ':TRIG:SEL EXT1'
    rc = inst.send_scpi_cmd(cmd)
    
    # Magic thing that reduces jitter.
    cmd = 'TRIG:LTJ ON'
    rc = inst.send_scpi_cmd(cmd)

    # Set the trigger level.
    # This was originally 0. 0 doesn't work, 0.1 minimum, 0.2 always works, 0.25 doesn't work sometimes
    cmd = ':TRIG:LEV 0.25'
    rc = inst.send_scpi_cmd(cmd)

    # Following the trigger, send :TRIG:COUN number of waveforms, then return to idle.
    cmd = ':TRIG:COUN 1'
    rc = inst.send_scpi_cmd(cmd)

    # In case something incorrectly sends another trigger, keep sending the :TRIG:COUN number of waveforms.
    cmd = ':TRIG:IDLE DC'
    rc = inst.send_scpi_cmd(cmd)

    # Turn the trigger on.
    cmd = ':TRIG:STAT ON'
    rc = inst.send_scpi_cmd(cmd)

    # Disable continuous (aka free-running) mode, and force trigger mode.
    cmd = ':INIT:CONT OFF'
    rc = inst.send_scpi_cmd(cmd)

    # Turn on the output of the selected channel.
    cmd = ':OUTP ON'
    rc = inst.send_scpi_cmd(cmd)
    
def stop():
    inst_addr = 'TCPIP::127.0.0.1::5025::SOCKET'
    inst = TEVisaInst(inst_addr)
    ch = 1

    # Select channel
    cmd = ':INST:CHAN {0}'.format(ch)
    rc = inst.send_scpi_cmd(cmd)

    # Turn on the output of the selected channel:
    cmd = ':OUTP OFF'
    rc = inst.send_scpi_cmd(cmd)