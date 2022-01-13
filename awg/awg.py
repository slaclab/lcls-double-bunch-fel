from awg.tabor.tevisainst import TEVisaInst
import time
import socket

def query(instrument, query_string):
    resp = instrument.send_scpi_query(query_string)
    print(query_string, resp)
    return resp
    
def command(instrument, command_string):
    resp = instrument.send_scpi_cmd(command_string)
    resp = instrument.send_scpi_query(':SYST:ERR?')
    print(command_string, 'error', resp)

def start(multipulse):
    # The address, channel, segment to send the waveform to.
    ip = socket.gethostbyname('UFK21-9')
    addr = f'TCPIP::{ip}::5025::SOCKET'
    print(addr)
    ch = 1
    segnum = 1
    
    start_time = time.time()
    instrument = TEVisaInst(addr)

    query(instrument, '*IDN?')
    query(instrument, ":SYST:iNF:MODel?")
    query(instrument, ":INST:CHAN? MAX")
    query(instrument, ":TRACe:SELect:SEGMent? MAX")
    command(instrument, "*CLS")

    # Get the available memory in bytes of wavform-data (per DDR):
    query(instrument, ":TRACe:FREE?")
    
    # Select channel.
    command(instrument, ':INST:CHAN {0}'.format(ch))
    
    # Get the waveform to send to the FPGA's memory.
    waveform = multipulse.get_awg_waveform()

    # Select segment and the number of samples to send to the segment. The clock samples
    # these data data points sequentially. The rate at which this sample is played 
    # is defined by :SOUR:FREQ:RAST (p. 66).
    command(instrument, ':TRAC:DEF {0}, {1}'.format(segnum, len(waveform)))
    
    # Select the segment
    command(instrument, ':TRAC:SEL {0}'.format(segnum))

    # Mean time to write the waveform is 0.5 seconds. Set to 10 seconds.
    instrument.write_binary_data('*OPC?; :TRAC:DATA', waveform)

    # Play the specified segment at the selected channel:
    command(instrument, ':SOUR:FUNC:MODE:SEGM {0}'.format(segnum))
    
    # Enable external clock EXT from the Agilent N5181A.
    command(instrument, ":FREQ:SOUR EXT")
    
    # ?
    #command(instrument, ':FREQ:RAST 1.428E9')

    # External trigger
    command(instrument, ':TRIG:SOUR:ENAB TRG1')

    # ?
    command(instrument, ':TRIG:SEL EXT1')
    
    # Magic thing that reduces jitter.
    command(instrument, ':TRIG:LTJ ON')

    # Set the trigger level.
    # 0 doesn't work, 0.1 minimum, 0.2 always works, 0.25 doesn't work sometimes
    command(instrument, ':TRIG:LEV 0.2')

    # Following the trigger, send :TRIG:COUN number of waveforms, then return to idle.
    command(instrument, ':TRIG:COUN 1')

    # In case something incorrectly sends another trigger, keep sending the :TRIG:COUN number of waveforms.
    command(instrument, ':TRIG:IDLE DC')

    # Turn the trigger on.
    command(instrument, ':TRIG:STAT ON')

    # Disable continuous (aka free-running) mode, and force trigger mode.
    command(instrument, ':INIT:CONT OFF')

    # Turn on the output of the selected channel.
    command(instrument, ':OUTP ON')
    
    end_time = time.time()
    print('Changed waveform in', end_time - start_time, 'seconds.')
    
def stop():
    addr = 'TCPIP::127.0.0.1::5025::SOCKET'
    instrument = TEVisaInst(addr)

    # Select channel
    command(instrument, ':INST:CHAN 1')

    # Turn on the output of the selected channel:
    command(instrument, ':OUTP OFF')