from bokeh.models import Div, Button, ColumnDataSource, Slider
from bokeh.layouts import column, row, grid
from bokeh.plotting import figure, show
from bokeh.models import Range1d, Spinner, TextAreaInput
from bokeh.server.server import Server
from functools import partial
import pulse.multipulse
import awg.awg
import scope.scope
import scope.bigscope
import scope.bigscope_image
import base64
import h5py
import time

class Panel:
    def __init__(self, multipulse):
        self.multipulse = multipulse
        
        # Anything regarding sizing is purely cosmetic.
        # Preferably Bokeh does this for us but alas.
                
        self.preview_figure_source = ColumnDataSource()
        self.preview_figure_source.data = dict(x=[], y=[])
        self.preview_figure = figure(title = 'Preview', x_axis_label = 'Nanoseconds', y_axis_label = 'Volt')
        self.preview_figure.line(source = self.preview_figure_source)
        self.preview_figure.x_range = Range1d(-20, 400)
        self.preview_figure.height = 300
        
        self.oscilloscope_image = Div(height = 480)
        
        self.bigscope_image = Div(height = 480)
        
        self.oscilloscope_figure_source = ColumnDataSource()
        self.oscilloscope_figure_source.data = dict(x=[], y=[])
        self.oscilloscope_figure = figure(title = 'Tinyscope', x_axis_label = 'Nanoseconds', y_axis_label = 'Volt')
        self.oscilloscope_figure.line(source = self.oscilloscope_figure_source)
        self.oscilloscope_figure.x_range = Range1d(600, 900)
        self.oscilloscope_figure.height = 300
        
        self.bigscope_figure_source = ColumnDataSource()
        self.bigscope_figure_source.data = dict(x=[], y=[])
        self.bigscope_figure = figure(title = 'Bigscope', x_axis_label = 'Nanoseconds', y_axis_label = 'Volt')
        self.bigscope_figure.line(source = self.bigscope_figure_source)
        self.bigscope_figure.height = 300
        
        self.number_of_traces = 1
        self.comment = ''
        
    def stop_everything(self):
        awg.awg.stop()
        self.server.stop()
        self.server.unlisten()
        self.server.io_loop.stop()
        
    def get_image(self):
        scope_image_data = scope.scope_image.get_scope_image()
        data_uri = base64.b64encode(scope_image_data).decode('utf-8')
        img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        self.oscilloscope_image.text = img_tag
        
    def get_bigscope_image(self):
        scope_file_data = scope.bigscope_image.get()
        data_uri = base64.b64encode(scope_file_data).decode('ascii')
        img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        self.bigscope_image.text = img_tag

    def plot_oscilloscope(self):
        sec_list, volt_list = scope.scope.get_nanosec_volt_lists()
        self.oscilloscope_figure_source.data = dict(x = sec_list, y = volt_list)
        
    def plot_bigscope(self):
        sec_list, volt_list = scope.bigscope.get()
        self.bigscope_figure_source.data = dict(x = sec_list, y = volt_list)
        
    def plot_preview(self):
        preview_x, preview_y = self.multipulse.get_preview_waveform()
        self.preview_figure_source.data = dict(x = preview_x, y = preview_y)
        
    def save(self):
        # Some boring file format. Make it readable.
        filename = time.strftime('%Y-%m-%d-%H-%M-%S')
        savefile = h5py.File(filename, 'w')
        
        preview_x, preview_y = self.multipulse.get_preview_waveform()
        waveform_x, waveform_y = self.multipulse.get_awg_waveform()
        savefile.create_dataset('preview_x', (len(preview_x),), data = preview_x)
        savefile.create_dataset('preview_y', (len(preview_y),), data = preview_y)
        savefile.create_dataset('waveform_x', (len(waveform_x),), data = waveform_x)
        savefile.create_dataset('waveform_y', (len(waveform_y),), data = waveform_y)
        
        # Save the traces. Each trace has x and y lists, each list is put in another list.
        # Get one spurious trace to get its dimensions.
        oscilloscope_x, oscilloscope_y = scope.scope.get_nanosec_volt_lists()
        
        oscilloscope_traces_x = list()
        oscilloscope_traces_y = list()
        
        for index in range(self.number_of_traces):
            oscilloscope_x, oscilloscope_y = scope.scope.get_nanosec_volt_lists()
            oscilloscope_traces_x.append(oscilloscope_x)
            oscilloscope_traces_y.append(oscilloscope_y)

        savefile.create_dataset('oscilloscope_traces_x', (self.number_of_traces,len(oscilloscope_x)), data = oscilloscope_traces_x)
        savefile.create_dataset('oscilloscope_traces_y', (self.number_of_traces,len(oscilloscope_y)), data = oscilloscope_traces_y)
        
        # some random dataset to store non-specific info
        attrs = savefile.create_dataset('attrs', (0,0))
        attrs.attrs['comment'] = self.comment
        attrs.attrs['time'] = time.time()
        
        # also save waveform paramters please
        # also save multiple traces please
        
        print('Done saving traces.')
        savefile.close()
        
    def change_number_of_traces(self, attr, old, new):
        self.number_of_traces = new
        
    def change_comment(self, attr, old, new):
        self.comment = new
        
    def start_controls(self, doc):
        stop_everything_button = Button(label='Stop everything')
        stop_everything_button.on_click(self.stop_everything)

        stop_button = Button(label='Stop Waveform')
        stop_button.on_click(awg.awg.stop)
        
        send_button = Button(label='Send Waveform')
        send_button.on_click(partial(awg.awg.send, self.multipulse))
        
        preview_button = Button(label='Preview Waveform')
        preview_button.on_click(self.plot_preview)
        
        plot_button = Button(label='Plot Tinyscope')
        plot_button.on_click(self.plot_oscilloscope)
        
        plot_bigscope_button = Button(label='Plot Bigscope')
        plot_bigscope_button.on_click(self.plot_bigscope)
        
        image_button = Button(label = 'Get Image')
        image_button.on_click(self.get_image)
        
        bigscope_image_button = Button(label = 'Get Big Scope')
        bigscope_image_button.on_click(self.get_bigscope_image)
        
        number_of_traces_spinner = Spinner(title = 'Number of traces to save', value = 1, low = 1, high = 50, step = 1)
        number_of_traces_spinner.on_change('value', self.change_number_of_traces)
        
        comment_box = TextAreaInput(rows = 1, title = 'Comment')
        comment_box.on_change('value', self.change_comment)
        
        save_button = Button(label='Save')
        save_button.on_click(self.save)

        multipulse_column = column()
        add_pulse_button = self.multipulse.get_add_button(multipulse_column)
        self.multipulse.add_controls_to(multipulse_column)        
        left = column(stop_everything_button, multipulse_column, add_pulse_button, send_button, stop_button, preview_button, plot_button, plot_bigscope_button, image_button, bigscope_image_button, row(number_of_traces_spinner, comment_box), save_button)
        
        right = column(self.preview_figure, self.oscilloscope_figure, self.bigscope_figure, self.oscilloscope_image, self.bigscope_image)

        doc.add_root(row(left, right))
        
    def start(self):
        self.server = Server({'/': self.start_controls})
        self.server.start()
        self.server.io_loop.add_callback(self.server.show, "/")
        self.server.io_loop.start()
