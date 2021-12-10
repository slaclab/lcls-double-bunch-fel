from bokeh.models import TextInput
from bokeh.layouts import column, row, grid
import functiongenerator.functiongenerator

class FunctionGeneratorPanel:
    def __init__(self):
        self.delay_nanoseconds = 0
        self.functiongenerator = functiongenerator.functiongenerator.FunctionGenerator()
        
    def change_delay(self, attr, old, new):
        self.delay_nanoseconds = float(new)
        self.functiongenerator.set_delay(new)
    
    def get_controls(self):
        delay_inputbox = TextInput(title = "Delay (nanosec)")
        delay_inputbox.on_change('value', self.change_delay)
        
        return delay_inputbox