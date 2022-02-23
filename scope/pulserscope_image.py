import pyvisa
<<<<<<< HEAD
=======
import socket
>>>>>>> b99c02f (2022 02 18 B15 Test Code)

def get():
    # Tektronix DPO TDS7154 oscilloscope
    # Procedure:
    # 1. On the scope, enable the "LAN Server"
    # 1. Connect via ethernet to some network
    # 1. Assign the scope some IP address.
    # 1. Set the IP address here.
    # 1. Test ping that IP address.
    
    rm = pyvisa.ResourceManager()
<<<<<<< HEAD
    scope = rm.open_resource('TCPIP::192.168.1.100::INSTR')
=======
    ip = socket.gethostbyname('RFARED-PC87017-7254C')
    scope = rm.open_resource(f'TCPIP::{ip}::INSTR')
>>>>>>> b99c02f (2022 02 18 B15 Test Code)

    scope.write("HARDCopy:PORT FILE;")
    scope.write("EXPort:FORMat PNG")

    # Temporary location on scope's disk
    scope.write("HARDCopy:FILEName \"C:\\Temp.png\"")

    # Write image to scope's disk
    scope.write("HARDCopy STARt")

    # Read image from scope's disk
    scope.write("FILESystem:READFile \"C:\\Temp.png\"")
    
    # This one has the image data
    imgData = scope.read_raw()
    
    # Delete the temp image
    scope.write("FILESystem:DELEte \"C:\\Temp.png\"")

    # Closing image
    scope.close()
    rm.close()
        
    return imgData