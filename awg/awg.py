from awg.tabor.tevisainst import TEVisaInst

def send(multipulse):
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
    
    # Set the sample frequency to 1 GSa/s. (p. 66).
    # Minimum is 1E9 and maximum is 9E9. Units are samples per second.
    # The arbitrary waveform will be sampled at 1 GSa/s.
    sampleRateDAC = 1E9
    print('Sample Clock Frequency {0}'.format(sampleRateDAC))
    cmd = ':FREQ:RAST {0}'.format(sampleRateDAC)
    rc = inst.send_scpi_cmd(cmd)

    # Enable external clock EXT from the function generator.
    cmd = "FREQ:SOUR EXT"
    rc = inst.send_scpi_cmd(cmd)

    # Get the available memory in bytes of wavform-data (per DDR):
    resp = inst.send_scpi_query(":TRACe:FREE?")
    arbmem_capacity = int(resp)
    print("Available memory per DDR: {0:,} wave-bytes".format(arbmem_capacity))

    # Get the waveform to send to the FPGA's memory.
    x, y = multipulse.get_awg_waveform()

    # Set the channel and segment to send the waveform to.
    ch = 1
    segnum = 1
    print('Download wave to segment {0} of channel {1}'.format(segnum, ch))

    # Select channel.
    cmd = ':INST:CHAN {0}'.format(ch)
    rc = inst.send_scpi_cmd(cmd)

    # Select segment and the number of samples to send to the segment. The clock samples
    # these data data points sequentially. The rate at which this sample is played 
    # is defined by :SOUR:FREQ:RAST (p. 66).
    cmd = ':TRAC:DEF {0}, {1}'.format(segnum, len(y))
    rc = inst.send_scpi_cmd(cmd)

    # Select the segment
    cmd = ':TRAC:SEL {0}'.format(segnum)
    rc = inst.send_scpi_cmd(cmd)

    # Increase the timeout before writing binary-data:
    inst.timeout = 30000
    inst.write_binary_data('*OPC?; :TRAC:DATA', y)
    resp = inst.send_scpi_query(':SYST:ERR?')
    print('Response', resp)
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