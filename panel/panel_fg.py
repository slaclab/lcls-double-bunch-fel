from bokeh.models import TextInput, Button, Div
from bokeh.layouts import column, row, grid
import functiongenerator.functiongenerator

class PanelFunctionGenerator:
    def __init__(self):
        self.delay_nanoseconds = 0
        self.functiongenerator = functiongenerator.functiongenerator.FunctionGenerator()
        
    def change_delay(self, attr, old, new):
        self.delay_nanoseconds = float(new)
        self.functiongenerator.set_delay(new)
        
    def find_delay(self, scope):
        # Setup:
        # Two signals. The first is the 120 Hz beam trigger, and the second is the 120 Hz beam itself.
        # Label A the delay from the trigger to the beam itself.
        # Next, 
        # Find the time delay between this function generator's trigger and the pulse on the oscilloscope.
        # Input: scope
        # Output: float, nanoseconds
        pass
    
    def get_controls(self):
        title = Div(text='<h1>Function Generator</h1>')
        
        delay_inputbox = TextInput(title = "Delay (ns)")
        delay_inputbox.on_change('value', self.change_delay)
        
        return title, delay_inputbox