Control the electron stripline kickers in LCLS sector 21.

# Production Environment

![](production.png)

## Materials

- Ethernet: 127.0.0.1 port 5025 CAT5
- Clock: Agilent N5181A 1.428 GHz BNC +1 dBm
- Trigger: 120 Hz BNC square pulse 120 Hz 0.5 Volt
- Waveform: -0.25 to 0.25 V Amperage unknown
- Windows: Windows 10
- Linux: OS to be determined. Must be approved to operate in the tunnel, must be shell-able, and must be able to caget production LCLS PVs. Must run Anaconda, Python 3.6. Not required to run graphics.
- AWG: Proteus P2588D

## Procedure

1. Connect the cables, turn everything on, set the clock and trigger
2. ...

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

1. Connect the cables, turn everything on, set the clock and trigger
1. Set up the AWG
   1. conda create --name myenv python=3.6
   1. source activate myenv
   1. python3 -m pip install pyvisa jupyerlab numpy bokeh matplotlib
1. Set up the network
    1. Set the scope IP manually on the oscilloscope.
    1. Set the scope IP and MAC address on the router.
    1. Test the connection using the "Test Connection" button on the oscilloscope.
1. python dbfel.py
