import h5py
import time
from bokeh.models import Div, Button, ColumnDataSource, Slider
from bokeh.layouts import column, row, grid
from bokeh.models import Range1d, Spinner, TextAreaInput
from bokeh.server.server import Server
import pulse.multipulse
import awg.awg
import scope.awgscope
import scope.awgscope_image
import scope.pulserscope
import scope.pulserscope_image
import panel.awg_panel
import panel.pulser_panel
import panel.functiongenerator_panel

class Panel:
    def __init__(self, multipulse):
        # We want one panel to control the AWG directly, which then controls the amplifiers.
        self.awg_panel = panel.awg_panel.AWGPanel(multipulse)
        
        # We want to control oscilloscope on the pulser.
        self.pulser_panel = panel.pulser_panel.PulserPanel()
        
        # This function generator is for the pulser. Maybe wiser to put it in pulser_panel.
        self.functiongenerator_panel = panel.functiongenerator_panel.FunctionGeneratorPanel()
        
        self.number_of_traces = 1
        self.comment = ''
        
    def stop_everything(self):
        awg.awg.stop()
        self.server.stop()
        self.server.unlisten()
        self.server.io_loop.stop()
        
    def save(self):
        # Save the lot. We want the parameters of the pulse, and traces of all scopes.
        # Some boring file format. Make it readable.
        filename = time.strftime('%Y-%m-%d-%H-%M-%S')
        savefile = h5py.File(filename, 'w')
        
        savefile.attrs['comment'] = self.comment
        savefile.attrs['time'] = time.time()
        
        self.awg_panel.addto(savefile, self.number_of_traces)
        # self.pulser_panel.addto(savefile, self.number_of_traces)
        
        print('Done saving traces.')
        savefile.close()
        
    def change_number_of_traces(self, attr, old, new):
        self.number_of_traces = new
        
    def change_comment(self, attr, old, new):
        self.comment = new
        
    def start_controls(self, doc):
        stop_everything_button = Button(label='Stop everything')
        stop_everything_button.on_click(self.stop_everything)
        
        number_of_traces_spinner = Spinner(title = 'Number of traces to save', value = 1, step = 1)
        number_of_traces_spinner.on_change('value', self.change_number_of_traces)
        
        comment_box = TextAreaInput(rows = 1, title = 'Comment')
        comment_box.on_change('value', self.change_comment)
        
        save_button = Button(label='Save')
        save_button.on_click(self.save)
        
        preview_figure, awgscope_figure, awgscope_image, stop_button, send_button, preview_button, plot_awgscope_button, awgscope_image_button, multipulse_column, add_pulse_button = self.awg_panel.get_controls()
        
        pulserscope_figure, pulserscope_image, plot_pulserscope_button, pulserscope_image_button = self.pulser_panel.get_controls()
        
        delay_inputbox = self.functiongenerator_panel.get_controls()
        
        left = column(stop_everything_button, delay_inputbox, multipulse_column, add_pulse_button, send_button, stop_button, preview_button, plot_awgscope_button, awgscope_image_button, plot_pulserscope_button, pulserscope_image_button, row(number_of_traces_spinner, comment_box), save_button)
        
        right = column(preview_figure, awgscope_figure, pulserscope_figure, awgscope_image, pulserscope_image)

        doc.add_root(row(left, right))
        
    def start(self):
        self.server = Server({'/': self.start_controls})
        self.server.start()
        self.server.io_loop.add_callback(self.server.show, "/")
        self.server.io_loop.start()
