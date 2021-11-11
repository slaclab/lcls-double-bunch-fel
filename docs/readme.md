Control the electron stripline kickers in LCLS sector 21.

# Production Environment

![](production.png)

- Ethernet: 127.0.0.1 port 5025.
- Clock: 1.428 GHz BNC.
- Trigger: 120 Hz BNC.
- Waveform: -0.25 to 0.25 V signal which is replicated by the amplifiers. Amperage unknown.
- Windows: Windows 10. Embedded.

## Materials

- Linux system. Unknown OS. Has at least one ethernet port. Should be approved to operate in the tunnel and connect to EPICS. Capable of running Anaconda, Python 3.6.
- AWG: Tabor Proteus P2588D

## Procedures

### Turn on or off the kickers

1. Connect to the Linux server via remote desktop.
1. Start the software using python.
	1. python main.py
1. Change the waveform parameters.
1. Start or stop the waveform sent to the AWG.

# Test Environment

![](test-diagram.png)

## Materials

- Tektronix Oscilloscope TDS3054B
- AWG
- Network Switch
- Clock

## Procedures

### Installation

1. Set the function generator to square pulse, 120 Hz, at least 0.5 Volt.
1. Set the clock to 1.428 GHz and +1dbm
1. Set up the AWG
   1. conda create --name myenv python=3.6
   1. source activate myenv
   1. python3 -m pip install pyvisa jupyerlab numpy bokeh
1. Set up the network.
    1. Set the scope IP manually on the oscilloscope.
    1. Set the scope IP and MAC address on the router.
    1. Test the connection using the "Test Connection" button on the oscilloscope.
