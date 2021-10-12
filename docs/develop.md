1. Set up python
   1. conda create --name myenv python=3.6
   1. source activate myenv
   1. python3 -m pip install pyvisa jupyerlab numpy bokeh matplotlib
1. Set up the network.
    1. Set the scope IP manually on the oscilloscope.
    1. Set the scope IP and MAC address on the router.
    1. Test the connection using the "Test Connection" button on the oscilloscope.
1. Start the interface
   1. python dbfel.py
   

A couple ideas for how to communicate with the scope
- http://sites.science.oregonstate.edu/~hetheriw/whiki/py/topics/inst/files/scope/tds1012b.py
- 