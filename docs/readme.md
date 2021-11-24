Amplifier and pulser control in the LCLS Multibunch Improvement Plan.

![Capture](https://user-images.githubusercontent.com/89935000/141534359-73715a3d-bfac-4d9a-875f-b0daab74b26a.PNG)

# Production Environment

Not official.

![](production.png)

- Location: LCLS Sector 21
- Ethernet: 127.0.0.1 port 5025 CAT5
- Clock: Agilent N5181A 1.428 GHz BNC +1 dBm
- Trigger: 120 Hz BNC square pulse 120 Hz 0.5 Volt
- Waveform: -0.25 to 0.25 V Amperage unknown
- Windows: Windows 10
- Linux: OS to be determined. Must be approved to operate in the tunnel, must be shell-able, and must be able to caget production LCLS PVs. Must run Anaconda, Python 3.6, with packages pyvisa and bokeh.
- AWG: Tabor Proteus P2588D

## Procedures

# Test Environment

- Location: Building 44 room 205

![](test-diagram.png)

- Oscilloscope: Tektronix TDS3054B
- AWG: Tabor Proteus 2588D
- Trigger: SRS DG645
- Clock: Agilent N5181A

![](https://user-images.githubusercontent.com/89935000/143211811-6b9165d9-7fbc-466b-b547-27252f304749.png)

- FG: Keysight DC Power Supply E3632A 0-15V 7A / 0-30V 4A
- FG?: TekPower 3003D 0-30V 0.3A: 0.15 A 3.1 V
- PS: Matasuda
- Trigger: SRS DG535
- Scope1: Tektronix TDS 7154
- Scope2: Tektronix TDS 3054B

## Procedures

### Install the AWG

2. Set the function generator to square pulse, 120 Hz, at least 0.5 Volt.
3. Set the clock to 1.428 GHz and 1dbm
4. Set up the AWG
   1. conda create --name myenv python=3.6
   1. source activate myenv
   1. python3 -m pip install pyvisa jupyerlab numpy bokeh h5py
5. Set up the network.
    1. Set the scope IP manually on the oscilloscope.
    1. Set the scope IP and MAC address on the router.
    1. Test the connection using the "Test Connection" button on the oscilloscope.

### Turn on or off the kickers

1. Connect to the Linux server via remote desktop.
1. Start the software using python.
	1. python main.py
1. Change the waveform parameters.
1. Start or stop the waveform sent to the AWG.

