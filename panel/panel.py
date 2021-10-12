from bokeh.models import Div, Button
from bokeh.layouts import column
from bokeh.io import output_file
from bokeh.server.server import Server
import awg.start
import awg.stop
import scope.scope

def start_bokeh_server():
    myapp = {'/': start_bokeh_app}
    myserver = Server(myapp)
    myserver.start()
    myserver.io_loop.add_callback(myserver.show, "/")
    myserver.io_loop.start()
    
def add_awg_controls(doc):
    # Return list of the buttons to control AWG.
    
    start_button = Button(label='Send Waveform')
    start_button.on_click(awg.start.start_waveform)
    
    stop_button = Button(label='Stop Waveform')
    stop_button.on_click(awg.stop.stop_waveform)
    
    doc.add_root(column(start_button, stop_button))
    
def add_scope_controls(doc):
    # Return list of buttons to control scope.
    
    plot_button = Button(label='Plot Oscilloscope')
    plot_button.on_click(scope.scope.plot_oscilloscope)
    
    doc.add_root(column(plot_button))

def start_bokeh_app(doc):
    add_awg_controls(doc)
    add_scope_controls(doc)