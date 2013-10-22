import serial
import yhy522commands

HEADER = 0xAABB
HEADER_1 = 0xAA
HEADER_2 = 0xBB

# XOR of Length and Data bytes
def calculate_checksum(length, command, data):
    result = length ^ command
    if data:
        result = result ^ data
    return result

def send_command(command, data):
    conn = serial.Serial('/dev/ttyAMA0', 19200, timeout=1)
    if data:
        length = len(str(command)) + len(str(data))
    else:
        length = len(str(command))
    csum = calculate_checksum(length, command, data)
    
    conn.write(format(HEADER, 'X'))
    conn.write(chr(length))
    conn.write(chr(command))
    if data:
        conn.write(format(data, 'X'))
    conn.write(chr(csum))
    
    if data:
        print("{0} {1} {2} {3} {4}".format(hex(HEADER), hex(length), hex(command), hex(data), hex(csum)))
    else:
        print("{0} {1} {2} {3}".format(hex(HEADER), hex(length), hex(command), hex(csum)))
        
    line = conn.readline()   # read a '\n' terminated line
    print line
    for c in line:
        print "%#x" % ord(c)
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
