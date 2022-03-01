import socket, re, time

def get_scope_lib():
    # Return the pyvisa scope so we can get data and images from it.

    scope_manual_ip = '192.168.1.123'
    rm = pyvisa.ResourceManager()
    lib = rm.visalib
    scope = rm.open_resource('TCPIP::' + scope_manual_ip + '::INSTR')
    
    return scope, lib

def get():
    input_buffer = 32 * 1024

    # Use sockets. It would be smarter to use the requests library, but this is fine.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.123', 80))

    # This won't work if the scope is password protected.
    cmd = b"GET /image.png HTTP/1.0\n\n"
    s.send(cmd)

    # Get the HTTP header
    status = s.recv(input_buffer)
    
    #Read the first chunk of data
    data = s.recv(input_buffer)
    
    imgData = b""

    # Check if the content is png image
    if (b"Content-Type: image/png" in data):
        # Find the length of the png data
        searchObj = re.search(b"Content-Length: (\d+)\r\n", data)
        imgSizeLeft = int(searchObj.group(1))
        
        # Pull the image data out of the first buffer
        startIdx = data.find(b"\x89PNG")
        
        # For the TDS3000B Series, the PNG image data may not come out with the
        # HTTP header
        # If the PNG file header was not found then do another read
        if (startIdx == -1):
            data = s.recv(input_buffer)
            imgData = data[data.find(b"\x89PNG"):]
        else:
            imgData = data[startIdx:]
            
        imgSizeLeft = imgSizeLeft - len(imgData)

        # Read the rest of the image data
        data = s.recv(input_buffer)

        while imgSizeLeft > len(data):
            imgData = b"".join([imgData, data])
            imgSizeLeft = imgSizeLeft - len(data)
            data = s.recv(input_buffer)

            # The TDS3000B Series sends the wrong value for Content-Length.  It
            # sends a value much larger than the real length.
            # If there is no more data then break out of the loop
            if (len(data) == 0):
                break

        # Add the last chunk of data
        imgData = b"".join([imgData, data])
    else:
        print("Content returned is not image/png")
        
    s.close()

    return imgData