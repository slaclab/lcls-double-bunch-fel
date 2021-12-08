Amplifier and pulser control in the LCLS Multibunch Improvement Plan.

![Capture](https://user-images.githubusercontent.com/89935000/141534359-73715a3d-bfac-4d9a-875f-b0daab74b26a.PNG)

# Production Environment

Not shown.

# Test Environment

- Location: Building 44 room 205

![](test-diagram.png)

- Oscilloscope: Tektronix TDS3054B
- AWG: Tabor Proteus 2588D
- Trigger: SRS DG645
- Clock: Agilent N5181A
- Switch: Not pictured.

![](https://user-images.githubusercontent.com/89935000/143211811-6b9165d9-7fbc-466b-b547-27252f304749.png)

- FG: Keysight DC Power Supply E3632A 0-15V 7A / 0-30V 4A
- FG?: TekPower 3003D 0-30V 0.3A -- 0.15 A 3.1 V
- PS: Matsusada High Voltage Power Supply
- Trigger: SRS DG535
- Scope1: Tektronix TDS7154
- Scope2: Tektronix TDS3054B

## Procedures

### Install

1. Set up the function generator.
    1. Set the function generator to square pulse, 120 Hz, at least 0.5 Volt.
1. Set up the clock.
    1. 1.428 GHz and +1dbm
    1. Set RF ON
3. Set up the AWG.
    1. conda create --name myenv python=3.6
    1. source activate myenv
    1. python3 -m pip install pyvisa jupyerlab numpy bokeh h5py
4. Set up the network.
    5. Plug in ethernet cables for the trigger, small scope, and big scope.
    1. On the TDS3054B, set its IP manually to 192.168.1.123.
    2. On the router, set the MAC of the small scope to 192.168.1.123.
    3. On the TDS7154, turn on the LAN server.
    4. On the function generator, set the IP to 192.168.1.125. [Ref](https://www.thinksrs.com/downloads/pdfs/manuals/DG645m.pdf)
    5. Test the connection using the "Test Connection" button on the oscilloscope.

### Turn on or off the kickers

1. Connect to the Linux server via remote desktop.
1. Start the software using python.
	1. python main.py
1. Change the waveform parameters.
1. Start or stop the waveform sent to the AWG.

