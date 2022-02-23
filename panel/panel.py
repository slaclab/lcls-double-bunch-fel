import h5py
import time
from bokeh.models import Button
from bokeh.layouts import column, row
from bokeh.models import Spinner, TextAreaInput
from bokeh.server.server import Server
<<<<<<< HEAD
import pulse.multipulse
import awg.awg
import panel.awg_panel
import panel.pulser_panel
import panel.functiongenerator_panel
=======
import awg.multipulse
import awg.awg
import panel.panel_awg
import panel.panel_pulser
import panel.panel_fg
>>>>>>> b99c02f (2022 02 18 B15 Test Code)

# The software interface.
class Panel:
    def __init__(self, multipulse):
<<<<<<< HEAD
        # The function generator that triggers the AWG waveform.
        self.functiongenerator_panel = panel.functiongenerator_panel.FunctionGeneratorPanel()
        
        # The oscilloscope connected to the AWG.
        self.awg_panel = panel.awg_panel.AWGPanel(multipulse)
        
        # The oscilloscope connected to the amplifier.
        # ...
        
        # The oscilloscope connected to the pulser.
        self.pulser_panel = panel.pulser_panel.PulserPanel()
        
        self.number_of_traces = 1
        self.comment = ''
        
    def stop_everything(self):
        # Stop the AWG waveform and exit this program. The program must be run again.
        awg.awg.stop()
        self.server.stop()
        self.server.unlisten()
        self.server.io_loop.stop()
        
    def change_number_of_traces(self, attr, old, new):
        self.number_of_traces = new
        
    def change_comment(self, attr, old, new):
        self.comment = new
        
    def save(self):
        # Save to one HDF5 file.
        # - The parameters of the pulse, and traces of all scopes.
        # - The waveform sent from the AWG to the amplifier. Units of nanosecond - Volt.
        # - The delay of the function generator that triggers the pulser.
        # - The comment for the file

        filename = time.strftime('%Y-%m-%d-%H-%M-%S')
        savefile = h5py.File(filename, 'w')
        
        savefile.attrs['comment'] = self.comment
        savefile.attrs['time'] = time.time()
        
        self.awg_panel.addto(savefile, self.number_of_traces)
        #self.pulser_panel.addto(savefile, self.number_of_traces)
        
        print('Done saving traces.')
        savefile.close()
        
    def add_elements(self, doc):
        stop_everything_button = Button(label='Stop everything')
        stop_everything_button.on_click(self.stop_everything)
=======
        # The function generator that triggers the AWG.
        self.panel_fg = panel.panel_fg.PanelFunctionGenerator()
        
        # The oscilloscope connected to the AWG.
        self.panel_awg = panel.panel_awg.PanelAWG(multipulse)
        
        # The oscilloscope connected to the pulser.
        self.panel_pulser = panel.panel_pulser.PanelPulser()
        
        self.number_of_traces = 1
        self.comment = ''
        
    def stop_webserver(self):
        # Stop the webserver and exit this program.
        self.server.stop()
        self.server.unlisten()
        self.server.io_loop.stop()
        
    def save(self):
        # Save to one HDF5 file.
        # - The parameters of the pulse, and traces of all scopes.
        # - The waveform sent from the AWG to the amplifier. Units of nanosecond - Volt.
        # - The delay of the function generator that triggers the pulser.
        # - The comment for the file

        filename = time.strftime('%Y-%m-%d-%H-%M-%S.hdf')
        savefile = h5py.File(filename, 'w')
        
        savefile.attrs['comment'] = self.comment
        savefile.attrs['time'] = time.time()
        
        #self.panel_awg.addto(savefile, self.number_of_traces)
        self.panel_pulser.addto(savefile, self.number_of_traces)
        
        print('Done saving traces.')
        savefile.close()
    
    def change_number_of_traces(self, attr, old, new):
        # Change the number of traces to save into the data file.
        self.number_of_traces = new
        
    def change_comment(self, attr, old, new):
        # Change the comment saved to the data file.
        self.comment = new
        
    def get_controls(self, doc):
        stop_webserver_button = Button(label='Stop webserver')
        stop_webserver_button.on_click(self.stop_webserver)
>>>>>>> b99c02f (2022 02 18 B15 Test Code)
        
        number_of_traces_spinner = Spinner(title = 'Number of traces to save', value = 1, step = 1)
        number_of_traces_spinner.on_change('value', self.change_number_of_traces)
        
        comment_box = TextAreaInput(rows = 1, title = 'Comment')
        comment_box.on_change('value', self.change_comment)
        
<<<<<<< HEAD
        save_button = Button(label='Save')
        save_button.on_click(self.save)
        
        preview_figure, awgscope_figure, awgscope_image, stop_button, send_button, plot_awgscope_button, awgscope_image_button, multipulse_column, add_pulse_button = self.awg_panel.get_controls()
        
        pulserscope_figure, pulserscope_image, plot_pulserscope_button, pulserscope_image_button = self.pulser_panel.get_controls()
        
        delay_inputbox = self.functiongenerator_panel.get_controls()
        
        left = column(stop_everything_button, delay_inputbox, multipulse_column, add_pulse_button, send_button, stop_button, plot_awgscope_button, awgscope_image_button, plot_pulserscope_button, pulserscope_image_button, row(number_of_traces_spinner, comment_box), save_button)
=======
        save_button = Button(label = 'Save', align = 'end')
        save_button.on_click(self.save)
        
        preview_figure, awgscope_figure, awgscope_image, awg_control_row, plot_awgscope_button, awgscope_image_button, multipulse_column, awg_title = self.panel_awg.get_controls()
        
        pulserscope_figure, pulserscope_image, plot_pulserscope_button, pulserscope_image_button = self.panel_pulser.get_controls()
        
        title_fg, delay_inputbox = self.panel_fg.get_controls()
        
        panel_row = row(number_of_traces_spinner, comment_box, save_button)
        panel_row.width = 700
        
        left = column(stop_webserver_button, panel_row, delay_inputbox, awg_control_row, multipulse_column, plot_awgscope_button, awgscope_image_button, plot_pulserscope_button, pulserscope_image_button)
>>>>>>> b99c02f (2022 02 18 B15 Test Code)
        
        right = column(preview_figure, awgscope_figure, pulserscope_figure, awgscope_image, pulserscope_image)

        doc.add_root(row(left, right))
        
    def start(self):
<<<<<<< HEAD
        self.server = Server({'/': self.add_elements})
=======
        # Start the control interface and hold the main thread.
        
        self.server = Server({'/': self.get_controls})
>>>>>>> b99c02f (2022 02 18 B15 Test Code)
        self.server.start()
        self.server.io_loop.add_callback(self.server.show, "/")
        self.server.io_loop.start()
