"""
The host interface.
"""

from functools import partial
import time

import h5py
from bokeh.models import Button, Div, TextInput
from bokeh.layouts import column, row
from bokeh.server.server import Server

import functiongenerator.functiongenerator
import awg.channel
import awg.awg
import scope.scope
import scope.smallscope_data
import scope.smallscope_image

class Host:
    """
    This class represents the host computer, which calls other devices for multibunch operation. Most importantly it displays the interface
    using Bokeh.
    """
    
    def __init__(self):
        """
        Init, but do not initiate any connections. We want to minimize persistent connections.
        """
        
        # The function generator that triggers the AWG.
        self.fg = functiongenerator.functiongenerator.FunctionGenerator()
        
        # The oscilloscope connected to the AWG.
        self.awg = awg.awg.AWG()
        
        self.number_of_traces = 1
        self.comment = ''
        
        self.frickin_width = 700
        
    def stop_webserver(self):
        """
        Stop the webserver and exit this program.
        """
        self.server.stop()
        self.server.unlisten()
        self.server.io_loop.stop()
        
    def save(self):
        """
        Save to one HDF5 file.
        - The parameters of the pulse, and traces of all scopes.
        - The waveform sent from the AWG to the amplifier. Units of nanosecond - Volt.
        - The delay of the function generator that triggers the pulser.
        - The comment for the file
        """

        filename = time.strftime('%Y-%m-%d-%H-%M-%S.hdf')
        savefile = h5py.File(filename, 'w')
        
        savefile.attrs['comment'] = self.comment
        savefile.attrs['time'] = time.time()
        
        #self.host_awg.addto(savefile, self.number_of_traces)
        #self.panel_pulser.addto(savefile, self.number_of_traces)
        
        print('Done saving traces.')
        savefile.close()
    
    def change_number_of_traces(self, attr, old, new):
        """
        Change the number of traces to save from scope to data file.
        """
        self.number_of_traces = new
        
    def change_comment(self, attr, old, new):
        """
        Change the comment saved to the data file.
        """
        self.comment = new
        
    def get_host_controls(self):
        """
        Get controls that operate on the host directly. Save calls other devices.
        """
        
        title = Div(text = '<h3>Host</h3>')
        
        stop_webserver_button = Button(label = 'Stop webserver', align = 'end')
        stop_webserver_button.on_click(self.stop_webserver)
        
        num_traces_box = TextInput(value = str(self.number_of_traces), title = 'Number of traces to save')
        num_traces_box.on_change('value', self.change_number_of_traces)
        
        comment_box = TextInput(title = 'Comment')
        comment_box.on_change('value', self.change_comment)
        
        save_button = Button(label = 'Save', align = 'end')
        save_button.on_click(self.save)
        
        host_row = row(stop_webserver_button, num_traces_box, comment_box, save_button)
        host_row.width = self.frickin_width
        
        host_column = column(title, host_row)
        host_column.width = self.frickin_width
        
        return host_column
        
    def get_controls(self, doc):
        """
        On startup, get all the control elements, and display.
        """
        host_column = self.get_host_controls()
        
        fg_control_column = self.fg.get_controls(self.frickin_width)
        
        awg_column = self.awg.get_controls(self.frickin_width)
        
        scope_column = scope.scope.get_controls(self.frickin_width)

        doc.add_root(column(host_column, fg_control_column, awg_column, scope_column))
        
    def start_interface(self):
        """
        Start the control interface and hold the main thread.
        """
        self.server = Server({'/': self.get_controls})
        self.server.start()
        self.server.io_loop.add_callback(self.server.show, "/")
        self.server.io_loop.start()
