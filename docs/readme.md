Control the electron stripline kickers in LCLS sector 21.

# Production Environment

![](production-diagram.png)

## Materials

- Linux system. Has at least one ethernet port, display, keyboard, and mouse.
- P1, P2: Pulsers built by Anatoly.
- AWG: Proteus P2588D
- AMP1, AMP2: R&K A009K321-6060R

## Procedure

1. Connect to the Linux server.
1. Start up the control interface using python.
	1. python dbfel.py
1. Start or stop the waveform sent to the AWG.

# Test Environment

![](test-diagram.png)


## Materials

- Tektronix Oscilloscope TDS3054B
- AWG
- Network Switch
- Clock

## Procedure

1. Set the function generator to square pulse, 120 Hz, at least 0.5 Volt.
2. Set the clock to 1.428 GHz and 1dbm
1. Set up the AWG
   1. conda create --name myenv python=3.6
   1. source activate myenv
   1. python3 -m pip install pyvisa jupyerlab numpy bokeh matplotlib
1. Set up the network.
    1. Set the scope IP manually on the oscilloscope.
    1. Set the scope IP and MAC address on the router.
    1. Test the connection using the "Test Connection" button on the oscilloscope.
1. Start the control panel.
   1. python dbfel.py
