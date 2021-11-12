Control the electron stripline kickers in the LCLS linear accelerator.

![Capture](https://user-images.githubusercontent.com/89935000/141534359-73715a3d-bfac-4d9a-875f-b0daab74b26a.PNG)

# Production Environment

![](production.png)

- Ethernet: 127.0.0.1 port 5025 CAT5
- Clock: Agilent N5181A 1.428 GHz BNC +1 dBm
- Trigger: 120 Hz BNC square pulse 120 Hz 0.5 Volt
- Waveform: -0.25 to 0.25 V Amperage unknown
- Windows: Windows 10
- Linux: OS to be determined. Must be approved to operate in the tunnel, must be shell-able, and must be able to caget production LCLS PVs. Must run Anaconda, Python 3.6, with packages pyvisa and bokeh.
- AWG: Tabor Proteus P2588D

## Materials

- Linux system. Unknown OS. Has at least one ethernet port, display, keyboard, and mouse. Should be approved to operate in the tunnel and connect to EPICS. Capable of running Anaconda, Python 3.6, Firefox.
- AWG: Proteus P2588D

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

- Building 44 room 205
- Tektronix Oscilloscope TDS3054B
- Tabor Proteus 2588D
- Switch: Linksys WRT110
- Trigger: SRS DG645
- Clock: Agilent N5181A

## Procedure

1. Set the function generator to square pulse, 120 Hz, at least 0.5 Volt.
1. Set the clock to 1.428 GHz and 1dbm
1. Set up the AWG
   1. conda create --name myenv python=3.6
   1. source activate myenv
   1. python3 -m pip install pyvisa jupyerlab numpy bokeh
1. Set up the network.
    1. Set the scope IP manually on the oscilloscope.
    1. Set the scope IP and MAC address on the router.
    1. Test the connection using the "Test Connection" button on the oscilloscope.
1. Start the control panel.
   1. python main.py
