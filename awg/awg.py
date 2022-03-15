"""
Class to interact with the AWG. This should be extremely reliable.
"""

import time
import socket
from functools import partial

from bokeh.layouts import column
from bokeh.models import Div, Button

from awg.tabor.tevisainst import TEVisaInst
import awg.channel

def query(instrument, query_string):
    resp = instrument.send_scpi_query(query_string)
    print(query_string, resp)
    return resp
    
def command(instrument, command_string):
    resp = instrument.send_scpi_cmd(command_string)
    resp = instrument.send_scpi_query(':SYST:ERR?')
    print(command_string, 'error', resp)

class AWG:
    def __init__(self):
        self.list_of_channel = [awg.channel.Channel(self, 'TRG1', '1'),
                                awg.channel.Channel(self, 'TRG1', '2')]
        self.column = column()
        
    def get_instrument(self):
        ip = socket.gethostbyname('UFK21-9')
        addr = f'TCPIP::{ip}::5025::SOCKET'
        instrument = TEVisaInst(addr)
        
        return instrument
        
    def get_controls(self, frickin_width):        
        title = Div(text = '<h3>AWG</h3>')
        self.column.children.append(title)
        
        for channel in self.list_of_channel:
            control_column = channel.get_control_column(frickin_width)
            self.column.children.append(control_column)            
        
        return self.column
        
    def addto(self, savefile, number_of_traces):
        waveform = self.multipulse.get_awg_waveform()
        savefile.create_dataset('awg_waveform', (len(waveform),), data = waveform)
        
        preview_x, preview_y = self.multipulse.get_preview_waveform()
        savefile.create_dataset('preview_x', (len(preview_x),), data = preview_x)
        savefile.create_dataset('preview_y', (len(preview_y),), data = preview_y)

    def start(self, channel):
        """
        The AWG has multiple channels, and each channel has multiple segments. Only one segment on one channel
        is needed to send one waveform.
        """
        start_time = time.time()
        instrument = self.get_instrument()
        segnum = 1

        query(instrument, '*IDN?')
        query(instrument, ":SYST:iNF:MODel?")

        # Clear errors from previous operation.
        command(instrument, "*CLS")

        # Get the available memory in bytes of wavform-data (per DDR):
        query(instrument, ":TRACe:FREE?")
        
        # Set the expected frequency into CLK IN so the AWG can set its internal PLL. It must be within :ROSC:FREQ Hz.
        # However the output on all channels zeros out when this command is sent, and then recovered after 0.5 seconds.
        # This is not acceptable so do not use it and use worse jitter.
        # command(instrument, ":FREQ:RAST 1.428E9")

        # Enable external clock EXT from the Agilent N5181A. If :FREQ:RAST is not set then this will error.
        command(instrument, ":FREQ:SOUR EXT")

        # Select channel.
        command(instrument, f':INST:CHAN {channel.channel}')

        # Get the waveform to send to the FPGA's memory.
        waveform = channel.get_awg_waveform()

        # Select segment and the number of samples to send to the segment. The clock samples
        # these data data points sequentially. The rate at which this sample is played 
        # is defined by :SOUR:FREQ:RAST (p. 66).
        command(instrument, f':TRAC:DEF {channel.channel}, {len(waveform)}')

        # The AWG has one map of integer to waveform called the "segment table." The segment table
        # is shared between all channels and triggers, so make sure each channel is on different
        # segments if we want the waveforms to be independent of eachother.
        command(instrument, f':TRAC:SEL {channel.channel}')
        
        # Each channel can have multiple segments, just select the first one.
        command(instrument, f':SOUR:FUNC:MODE:SEGM {channel.channel}')

        # Write data to segment.
        instrument.write_binary_data('*OPC?; :TRAC:DATA', waveform)

        # Trigger waveform on front panel TRG1.
        command(instrument, f':TRIG:SOUR:ENAB {channel.trigger}')
        command(instrument, f':TRIG:SEL {channel.trigger}')

        # Magic thing that reduces jitter.
        command(instrument, ':TRIG:LTJ ON')

        # Trigger at 0.5 V.
        command(instrument, ':TRIG:LEV 0.5')
        
        # TRIG:WID should be 0, which means trigger on pulse of width 0.

        # Following the trigger, send :TRIG:COUN number of waveforms, then return to idle.
        command(instrument, ':TRIG:COUN 1')

        # In case something incorrectly sends another trigger, keep sending the previous waveform.
        command(instrument, ':TRIG:IDLE DC')

        # Disable continuous (aka free-running) mode, and force trigger mode.
        command(instrument, ':INIT:CONT OFF')

        # Turn the trigger on.
        command(instrument, ':TRIG:STAT ON')
        
        # Turn on the output of the selected channel.
        command(instrument, ':OUTP ON')
        
        # The peak voltage.
        command(instrument, ':VOLT 1.2')

        end_time = time.time()
        print('Changed waveform in', end_time - start_time, 'seconds.')

    def stop(self, channel):
        instrument = self.get_instrument()

        # Select channel
        command(instrument, f':INST:CHAN {channel.channel}')

        # Turn on the output of the selected channel:
        command(instrument, ':OUTP OFF')