import serial

cmd_Header = 0xAABB
cmd_Header_1 = 0xAA
cmd_Header_2 = 0xBB

# System commands

cmd_Test_Com = 0x00
cmd_MSleep = 0x03
cmd_MConfigure = 0x04
cmd_Download_Keys = 0x05
cmd_Download_Block_String = 0x08
cmd_Download_Value = 0x09
cmd_Antenna_Control = 0x11
cmd_Sense_Mode = 0x13
cmd_Beep = 0x14
cmd_Beep_time = 0x15
cmd_Output1 = 0x16
cmd_Output2 = 0x17

# RFID commands

cmd_Change_Card_Keys = 0x06
cmd_LOCK_Card = 0x07
cmd_Card_Sleep = 0x12
cmd_Card_Type = 0x19
cmd_Card_ID = 0x20
cmd_Block_Read = 0x21
cmd_Block_Write = 0x22
cmd_Value_Init = 0x23
cmd_Value_Read = 0x24
cmd_Value_Inc = 0x25
cmd_Value_Dec = 0x26
cmd_Value_Backup = 0x27
cmd_Sector_Read = 0x2a
cmd_Sector_Write = 0x2b

class Yhy522(object):

    def __init__(self, port="/dev/ttyAMA0"):
        self.__conn = serial.Serial(port, 19200, timeout=1)

    def __del__(self):
        self.__conn.close()

    def __validate(self, response):
        if len(response) < 5:
            return False
        result = True
        header1 = response[0]
        header2 = response[1]
        length = response[2]
        status = response[3]
        csum = response[-1]
        if(length > 2):
            data = response[4:-1]
        else:
            data = None

        if(header1 != cmd_Header_1 | header2 != cmd_Header_2):
            #print "Header is not correct"
            result = False
        if(length != (len(response[2:-1]))):
            #print "Length is not correct"
            result = False
        my_csum = self.__calculate_checksum(length, status, data)
        if(my_csum != csum):
            #print "Checksum not ok: %x != %x" % (my_csum, csum)
            result = False

        #print "Status = 0x" + format(status, 'X')
        #print "data = " + data

        return result

    # XOR of Length and Data bytes
    def __calculate_checksum(self, length, command, data):
        result = length ^ command
        if data:
            for d in data:
                result = result ^ d
        return result

    def __calculate_length(self, command, data):
        length = 2
        if data:
            for d in data:
                length += 1
        return length

    def __send_command(self, command, data):
        length = self.__calculate_length(command, data)
        csum = self.__calculate_checksum(length, command, data)

        self.__conn.write(bytes([cmd_Header_1]))
        self.__conn.write(bytes([cmd_Header_2]))
        self.__conn.write(bytes([length]))
        self.__conn.write(bytes([command]))

        if data:
            for d in data:
                self.__conn.write(bytes([d]))
        self.__conn.write(bytes([csum]))

        to_send = ""
        to_send += format(cmd_Header, '02X')
        to_send += format(length, '02X')
        to_send += format(command, '02X')
        if data:
            for d in data:
               to_send += format(d, '02X')
        to_send += format(csum, '02X')
        #print "Sending:  " + to_send

        validated = False
        line = self.__conn.readline()   # read a '\n' terminated line

        if line:
            if(not self.__validate(line)):
                return False, None

            recv_length = line[2]
            recv_status = line[3]

            if(recv_length > 2):
                recv_data = line[4:-1]
            else:
                recv_data = None

            if (recv_status == command):
                #print "recv_status and validate ok"
                return True, recv_data
            # elif(recv_status == command ^ 0xFF):
            #     #print "something went wrong"
            #     return False, None

        return False, None

    # System commands
    def Test_Com(self):
        success, recv_data = self.__send_command(cmd_Test_Com, None)
        return success

    def MSleep(self, data):
        self.__send_command(cmd_MSleep, data)

    def SetAutoModeOff(self):
        return MConfigure(auto_code=0)

    def SetAutoSeekCardMode(self):
        return MConfigure(auto_code=1)

    def SetAutoReadIdMode(self):
        return MConfigure(auto_code=2)

    def SetAutoReadBlockMode(self, block):
        return MConfigure(auto_code=3, block_rw = block)

    def SetAutoWriteBlockMode(self, block):
        succes, data = MConfigure(auto_code=4, block_rw = block)
        succes2, data2 = Download_Block_String(value)
        # TODO: implement this stuff

    def SetAutoDecrementBlockMode(self):
        return MConfigure(auto_code=5)

    def SetAutoIncrementBlockMode(self):
        return MConfigure(auto_code=6)

    def SetAutoReadSectorMode(self):
        return MConfigure(auto_code=7)

    def MConfigure(self,
                    auto_code = 0,
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
        succes, data = self.__send_command(cmd_MConfigure, data)

        # Insert a reset command here
        return success

    def Download_Keys(self, data):
        self.__send_command(cmd_Download_Keys, data)
    def Download_Block_String(self, data):
        self.__send_command(cmd_Download_Block_String, data)
    def Download_Value(self, data):
        self.__send_command(cmd_Download_Value, data)
    def Antenna_Control(self, state):
        if(state):
            data = [0x03]
        else:
            data = [0x00]
        succes, data = self.__send_command(cmd_Antenna_Control, data)

        if(succes):
            return True
        else:
            return False


    def Sense_Mode(self, code):
        if(code >= 0 & code < 8):
            data = [code]
            success, data = self.__send_command(cmd_Sense_Mode, data)
            return success
        else:
            raise Exception("Unknown code. Should be between 0 and 7")

    def Beep(self, activate, amount):
        if(activate & amount >= 0 & amount < 10):
            data = [0x10 + amount]
        else:
            data = [0x0F]

        success, data = self.__send_command(cmd_Beep, data)
        return success

    def Beep_time(self, interval_ms):
        data = interval_ms / 10
        if(data > 255):
            data = 255
        data = [data]
        success, data = self.__send_command(cmd_Beep_time, data)
        return success

    def Output1(self, data):
        success, data = self.__send_command(cmd_Output1, data)
        return success

    def Output2(self, data):
        success, data = self.__send_command(cmd_Output2, data)
        return success

    # RFID commands
    def Change_Card_Keys(self, data):
        success, data = self.__send_command(cmd_Change_Card_Keys, data)
        return success

    def LOCK_Card(self, data):
        success, data = self.__send_command(cmd_LOCK_Card, data)
        return success

    def Card_Sleep(self, data):
        success, data = self.__send_command(cmd_Card_Sleep, data)
        return success

    def Card_Type(self):
        succes, data = self.__send_command(cmd_Card_Type, [])
        if(succes):
            return data[0] * 256 + data[1]
        else:
            raise Exception("Error getting card type")

    def Card_ID(self, data=None):
        succes, data = self.__send_command(cmd_Card_ID, data)
        if(succes):
            return data
        else:
            return []

    def Block_Read(self, data):
        self.__send_command(cmd_Block_Read, data)
    def Block_Write(self, data):
        self.__send_command(cmd_Block_Write, data)
    def Value_Init(self, data):
        self.__send_command(cmd_Value_Init, data)
    def Value_Read(self, data):
        self.__send_command(cmd_Value_Read, data)
    def Value_Inc(self, data):
        self.__send_command(cmd_Value_Inc, data)
    def Value_Dec(self, data):
        self.__send_command(cmd_Value_Dec, data)
    def Value_Backup(self, data):
        self.__send_command(cmd_Value_Backup, data)
    def Sector_Read(self, data):
        self.__send_command(cmd_Sector_Read, data)
    def Sector_Write(self, data):
        self.__send_command(cmd_Sector_Write, data)
