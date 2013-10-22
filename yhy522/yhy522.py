import serial
import yhy522commands

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
    print "Status = 0x" + format(status, 'X')

    
    print data
    my_csum = calculate_checksum(length, status, data)
    if(my_csum != csum):
        print "Checksum not ok: %x != %x" % (my_csum, csum)
        result = False
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
    to_send += format(HEADER, 'X')
    to_send += format(length, 'X')
    to_send += format(command, 'X')
    if data:
        for d in data:
           to_send += format(d, 'X')
    to_send += format(csum, 'X')
    print "Sending:  " + to_send    

    line = conn.readline()   # read a '\n' terminated line
    validate(line)
    result = ""
    if line:
        for c in line:
            result += format(ord(c), 'X')
        print "Received: " + result
    else:
        print "No response"
    
    conn.close()
    return line

# System commands
def Test_Com(data):
    send_command(yhy522commands.Test_Com, data) 
def MSleep(data):
    send_command(yhy522commands.MSleep, data)
def MConfigure(data):
    send_command(yhy522commands.MConfigure, data)
def Download_Keys(data):
    send_command(yhy522commands.Download_Keys, data)
def Download_Block_String(data):
    send_command(yhy522commands.Download_Block_String, data)
def Download_Value(data):
    send_command(yhy522commands.Download_Value, data)
def Antenna_Control(data):
    send_command(yhy522commands.Antenna_Control, data)
def Sense_Mode(data):
    send_command(yhy522commands.Sense_Mode, data)
def Beep(data):
    send_command(yhy522commands.Beep, data)
def Beep_time(data):
    send_command(yhy522commands.Beep_time, data)
def Output1(data):
    send_command(yhy522commands.Output1, data)
def Output2(data):
    send_command(yhy522commands.Output2, data)

# RFID commands

def Change_Card_Keys(data):
    send_command(yhy522commands.Change_Card_Keys, data)
def LOCK_Card(data):
    send_command(yhy522commands.LOCK_Card, data)
def Card_Sleep(data):
    send_command(yhy522commands.Card_Sleep, data)
def Card_Type(data):
    send_command(yhy522commands.Card_Type, data)
def Card_ID(data=None):
    send_command(yhy522commands.Card_ID, data)
def Block_Read(data):
    send_command(yhy522commands.Block_Read, data)
def Block_Write(data):
    send_command(yhy522commands.Block_Write, data)
def Value_Init(data):
    send_command(yhy522commands.Value_Init, data)
def Value_Read(data):
    send_command(yhy522commands.Value_Read, data)
def Value_Inc(data):
    send_command(yhy522commands.Value_Inc, data)
def Value_Dec(data):
    send_command(yhy522commands.Value_Dec, data)
def Value_Backup(data):
    send_command(yhy522commands.Value_Backup, data)
def Sector_Read(data):
    send_command(yhy522commands.Sector_Read, data)
def Sector_Write(data):
    send_command(yhy522commands.Sector_Write, data)
