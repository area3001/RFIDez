import serial
import sys

HEADER = 0xAABB
HEADER_1 = 0xAA
HEADER_2 = 0xBB

def validate(response):
    sys.stdout.write("validating response: ")
    print([ord(x) for x in response])
    if len(response) < 5:
        return False
    result = True
    header1 = ord(response[0])
    header2 = ord(response[1])
    length = ord(response[2])
    status = ord(response[3])
    csum = ord(response[-1])
    data = [ ord(x) for x in response[4:-1] ]    

    if(header1 != HEADER_1 | header2 != HEADER_2):
        print "Header is not correct"
        result = False
    if(length != (len(response[2:-1]))):
        print "Length is not correct"
        result = False
    my_csum = calculate_checksum(length, status, data)
    if(my_csum != csum):
        print "Checksum not ok: %x != %x" % (my_csum, csum)
        result = False
            
    #print "Status = 0x" + format(status, 'X')
    #print "data = " + data

    return result

# XOR of Length and Data bytes
def calculate_checksum(length, command, data):
    result = length ^ command
    if data:
        for d in data:
            result = result ^ d
    return result

def calculate_length(command, data):
    length = 2
    if data:
        for d in data:
            length += 1
    return length

def send_command(command, data):
    conn = serial.Serial('/dev/ttyAMA0', 19200, timeout=1)
    length = calculate_length(command, data)
    csum = calculate_checksum(length, command, data)
    
    conn.write(chr(HEADER_1))
    conn.write(chr(HEADER_2))
    conn.write(chr(length))
    conn.write(chr(command))

    if data:
        for d in data:
            conn.write(chr(d))
    conn.write(chr(csum))
    
    to_send = ""
    to_send += format(HEADER, '02X')
    to_send += format(length, '02X')
    to_send += format(command, '02X')
    if data:
        for d in data:
           to_send += format(d, '02X')
    to_send += format(csum, '02X')
    print "Sending:  " + to_send    

    validated = False
    line = conn.readline()   # read a '\n' terminated line
    conn.close()

    if line:
        result = ""
        for c in line:
            result += format(ord(c), '02X')
        if(validate(line)):
            validated = True
            print "Received: " + result
        else:
            print "Received invalid data: " + result
            return False, 0 
    
        recv_status = ord(line[3])
        recv_data = [ ord(x) for x in line[4:-1] ]

        if ((recv_status == command) and (validated == True)):
            print "recv_status and validate ok"
            return True, recv_data
        elif(recv_status == command ^ 0xFF):
            print "something went wrong"
            return False, 0 
    else:
        print "Received no response"
        return False, 0 


