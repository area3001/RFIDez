import yhy522commands as cmd
import yhy522

# System commands
def Test_Com(data):
    succes, recv_data = yhy522.send_command(cmd.Test_Com, data)
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
    yhy522.send_command(cmd.MSleep, data)

def SetAutoModeOff():
    return MConfigure(auto_code=0)

def SetAutoSeekCardMode():
    return MConfigure(auto_code=1)

def SetAutoReadIdMode():
    return MConfigure(auto_code=2)

def SetAutoReadBlockMode(block):
    return MConfigure(auto_code=3, block_rw = block)

def SetAutoWriteBlockMode(block):
    succes, data = MConfigure(auto_code=4, block_rw = block, value)
    succes2, data2 = Download_Block_String(value)
    # TODO: implement this stuff

def SetAutoDecrementBlockMode():
    return MConfigure(auto_code=5)

def SetAutoIncrementBlockMode():
    return MConfigure(auto_code=6)

def SetAutoReadSectorMode():
    return MConfigure(auto_code=7)

def MConfigure( auto_code = 0,
                key_type = 0x00,
                key_string = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
                block_rw = 0x00,
                block_value = 0x00,
                value_backup = 0x00,
                start_sector = 0x00,
                end_sector = 0x00,
                auth_mode = 0x00,
                RFU = 0x60,
                baud_code = 5):
    if(auto_code < 0 | auto_code > 7):
        raise Exception("Auto Code is not valid: {0}".format(auto_code))

    if(baud_code < 1 | baud_code > 9):
        baud_code = 5 # default baudrate

    data = [auto_code, key_type] + key_string + [block_rw, block_value, value_backup, start_sector, end_sector, auth_mode, RFU, baud_code]
    succes, data = yhy522.send_command(cmd.MConfigure, data)

    # Insert a reset command here

    if(succes):
        return True
    else:
        return False

def Download_Keys(data):
    yhy522.send_command(cmd.Download_Keys, data)
def Download_Block_String(data):
    yhy522.send_command(cmd.Download_Block_String, data)
def Download_Value(data):
    yhy522.send_command(cmd.Download_Value, data)
def Antenna_Control(state):
    if(state):
        data = [0x03]
    else:
        data = [0x00]
    succes, data = yhy522.send_command(cmd.Antenna_Control, data)

    if(succes):
        return True
    else:
        return False


def Sense_Mode(code):
    if(code >= 0 & code < 8):
        data = [code]
        succes, data = yhy522.send_command(cmd.Sense_Mode, data)
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

    succes, data = yhy522.send_command(cmd.Beep, data)
    if(succes):
        return True
    else:
        return False

def Beep_time(interval_ms):
    data = interval_ms / 10
    if(data > 255):
        data = 255
    data = [data]
    succes, data = yhy522.send_command(cmd.Beep_time, data)
    if(succes):
        return True
    else:
        return False

def Output1(data):
    yhy522.send_command(cmd.Output1, data)
def Output2(data):
    yhy522.send_command(cmd.Output2, data)

# RFID commands

def Change_Card_Keys(data):
    yhy522.send_command(cmd.Change_Card_Keys, data)
def LOCK_Card(data):
    yhy522.send_command(cmd.LOCK_Card, data)
def Card_Sleep(data):
    yhy522.send_command(cmd.Card_Sleep, data)
def Card_Type():
    succes, data = yhy522.send_command(cmd.Card_Type, [])
    if(succes):
        return data[0] * 256 + data[1]
    else:
        raise Exception("Error getting card type")

def Card_ID(data=None):
    succes, data = yhy522.send_command(cmd.Card_ID, data)
    if(succes):
        return data
    else:
        raise Exception("Card_ID error")

def Block_Read(data):
    yhy522.send_command(cmd.Block_Read, data)
def Block_Write(data):
    yhy522.send_command(cmd.Block_Write, data)
def Value_Init(data):
    yhy522.send_command(cmd.Value_Init, data)
def Value_Read(data):
    yhy522.send_command(cmd.Value_Read, data)
def Value_Inc(data):
    yhy522.send_command(cmd.Value_Inc, data)
def Value_Dec(data):
    yhy522.send_command(cmd.Value_Dec, data)
def Value_Backup(data):
    yhy522.send_command(cmd.Value_Backup, data)
def Sector_Read(data):
    yhy522.send_command(cmd.Sector_Read, data)
def Sector_Write(data):
    yhy522.send_command(cmd.Sector_Write, data)