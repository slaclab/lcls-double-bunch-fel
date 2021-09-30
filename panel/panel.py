from bokeh.models import Div, Button
from bokeh.layouts import column
from bokeh.io import output_file
from bokeh.plotting import figure, curdoc
from bokeh.client import push_session
import awg.start

def send_waveform():
    awg.start.send_waveform()

def show_panel():
    # Bokeh uses the internet by default, but we need it offline. Set mode='inline' to do this.
    output_file('dbfel.html', mode='inline')
    
    # On Button
    button = Button(label="Send Waveform")
    button.on_click(send_waveform)
    
    curdoc().title("Double Bunch FEL")
    curdoc().add_root(column(button))
    
    session = push_session(curdoc())
    session.show()
