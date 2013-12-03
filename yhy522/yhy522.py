import serial
import yhy522commands as cmd

HEADER = 0xAABB
HEADER_1 = 0xAA
HEADER_2 = 0xBB

def validate(response):
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

    line = conn.readline()   # read a '\n' terminated line
    if line:
        result = ""
        for c in line:
            result += format(ord(c), '02X')
        if(validate(line)):
            print "Received: " + result
        else:
            print "Received invalid data: " + result
    else:
        print "Received no response"
    
    conn.close()

    recv_status = ord(line[3])
    recv_data = [ ord(x) for x in line[4:-1] ]

    if(recv_status == command):
        return True, recv_data
    elif(recv_status == command ^ 0xFF):
        return False, data

# System commands
def Test_Com(data):
    succes, recv_data = send_command(cmd.Test_Com, data)
    if(succes):
        if(recv_data == data):
            # received the same data back == success
            return True
        else:
            # Failed
            return False
    else:
        return False

def MSleep(data):
    send_command(cmd.MSleep, data)


def MConfigure(data):
    succes, data = send_command(cmd.MConfigure, data)


def Download_Keys(data):
    send_command(cmd.Download_Keys, data)
def Download_Block_String(data):
    send_command(cmd.Download_Block_String, data)
def Download_Value(data):
    send_command(cmd.Download_Value, data)
def Antenna_Control(state):
    if(state):
        data = [0x03]
    else:
        data = [0x00]
    succes, data = send_command(cmd.Antenna_Control, data)

    if(succes):
        return True
    else:
        return False


def Sense_Mode(code):
    if(code >= 0 & code < 8):
        data = [code]
        succes, data = send_command(cmd.Sense_Mode, data)
        if(succes):
            return True
        else:
            return False
    else:
        raise Exception("Unknown code. Should be between 0 and 7")

def Beep(activate, amount):
    if(activate & amount >= 0 & amount < 10):
        data = [0x10 + amount]
    else:
        data = [0x0F]

    succes, data = send_command(cmd.Beep, data)
    if(succes):
        return True
    else:
        return False

def Beep_time(interval_ms):
    data = interval_ms / 10
    if(data > 255):
        data = 255
    data = [data]
    succes, data = send_command(cmd.Beep_time, data)
    if(succes):
        return True
    else:
        return False

def Output1(data):
    send_command(cmd.Output1, data)
def Output2(data):
    send_command(cmd.Output2, data)

# RFID commands

def Change_Card_Keys(data):
    send_command(cmd.Change_Card_Keys, data)
def LOCK_Card(data):
    send_command(cmd.LOCK_Card, data)
def Card_Sleep(data):
    send_command(cmd.Card_Sleep, data)
def Card_Type():
    succes, data = send_command(cmd.Card_Type, [])
    if(succes):
        return data[0] * 256 + data[1]
    else:
        raise Exception("Error getting card type")

def Card_ID(data=None):
    succes, data = send_command(cmd.Card_ID, data)
    if(succes):
        return data
    else:
        raise Exception("Card_ID error")

def Block_Read(data):
    send_command(cmd.Block_Read, data)
def Block_Write(data):
    send_command(cmd.Block_Write, data)
def Value_Init(data):
    send_command(cmd.Value_Init, data)
def Value_Read(data):
    send_command(cmd.Value_Read, data)
def Value_Inc(data):
    send_command(cmd.Value_Inc, data)
def Value_Dec(data):
    send_command(cmd.Value_Dec, data)
def Value_Backup(data):
    send_command(cmd.Value_Backup, data)
def Sector_Read(data):
    send_command(cmd.Sector_Read, data)
def Sector_Write(data):
    send_command(cmd.Sector_Write, data)
