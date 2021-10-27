Control the electron stripline kickers in the LCLS Multibunch project.

# Production Environment

![](production-diagram.png)

# Test Environment

1. Set up the AWG
   1. conda create --name myenv python=3.6
   1. source activate myenv
   1. python3 -m pip install pyvisa jupyerlab numpy bokeh matplotlib
1. Set up the network.
    1. Set the scope IP manually on the oscilloscope.
    1. Set the scope IP and MAC address on the router.
    1. Test the connection using the "Test Connection" button on the oscilloscope.
1. Start the interface
   1. python dbfel.py

## Materials

1. Tektronix Oscilloscope TDS3054B
2. AWG
3. Network Switch
4. Function generator

## Procedure

1. Set the function generator to square pulse, 120 Hz, at least 0.5 Volt.
2. Set the clock to 1.428 GHz and 1dbm
3. Set up 
