import serial
import yhy522constants as cmd

class Yhy522(object):

    def __init__(self, port="/dev/ttyAMA0"):
        self.__conn = serial.Serial(port, 19200, timeout=1)

    def __del__(self):
        self.__conn.close()

    def __validate(self, response):
        if len(response) < 5:
            return False
        result = True
        header1 = ord(response[0])
        header2 = ord(response[1])
        length = ord(response[2])
        status = ord(response[3])
        csum = ord(response[-1])
        if(length > 2):
            data = [ ord(x) for x in response[4:-1] ]
        else:
            data = None

        if(header1 != Header_1 | header2 != Header_2):
            #print "Header is not correct"
            result = False
        if(length != (len(response[2:-1]))):
            #print "Length is not correct"
            result = False
        my_csum = __calculate_checksum(length, status, data)
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
        length = __calculate_length(command, data)
        csum = __calculate_checksum(length, command, data)

        self.__conn.write(chr(cmd.Header_1))
        self.__conn.write(chr(cmd.Header_2))
        self.__conn.write(chr(length))
        self.__conn.write(chr(command))

        if data:
            for d in data:
                self.__conn.write(chr(d))
        self.__conn.write(chr(csum))

        to_send = ""
        to_send += format(cmd.Header, '02X')
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
            if(not __validate(line)):
                return False, None

            recv_length = ord(line[2])
            recv_status = ord(line[3])

            if(recv_length > 2):
                recv_data = [ ord(x) for x in line[4:-1] ]
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
        success, recv_data = __send_command(cmd.Test_Com, None)
        return success

    def MSleep(self, data):
        self.__send_command(cmd.MSleep, data)

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
        succes, data = __send_command(cmd.MConfigure, data)

        # Insert a reset command here
        return success

    def Download_Keys(self, data):
        __send_command(cmd.Download_Keys, data)
    def Download_Block_String(self, data):
        __send_command(cmd.Download_Block_String, data)
    def Download_Value(self, data):
        __send_command(cmd.Download_Value, data)
    def Antenna_Control(self, state):
        if(state):
            data = [0x03]
        else:
            data = [0x00]
        succes, data = __send_command(cmd.Antenna_Control, data)

        if(succes):
            return True
        else:
            return False


    def Sense_Mode(self, code):
        if(code >= 0 & code < 8):
            data = [code]
            success, data = __send_command(cmd.Sense_Mode, data)
            return success
        else:
            raise Exception("Unknown code. Should be between 0 and 7")

    def Beep(self, activate, amount):
        if(activate & amount >= 0 & amount < 10):
            data = [0x10 + amount]
        else:
            data = [0x0F]

        success, data = __send_command(cmd.Beep, data)
        return success

    def Beep_time(self, interval_ms):
        data = interval_ms / 10
        if(data > 255):
            data = 255
        data = [data]
        success, data = __send_command(cmd.Beep_time, data)
        return success

    def Output1(self, data):
        success, data = __send_command(cmd.Output1, data)
        return success

    def Output2(self, data):
        success, data = __send_command(cmd.Output2, data)
        return success

    # RFID commands
    def Change_Card_Keys(self, data):
        success, data = __send_command(cmd.Change_Card_Keys, data)
        return success

    def LOCK_Card(self, data):
        success, data = __send_command(cmd.LOCK_Card, data)
        return success

    def Card_Sleep(self, data):
        success, data = __send_command(cmd.Card_Sleep, data)
        return success

    def Card_Type(self):
        succes, data = __send_command(cmd.Card_Type, [])
        if(succes):
            return data[0] * 256 + data[1]
        else:
            raise Exception("Error getting card type")

    def Card_ID(self, data=None):
        succes, data = __send_command(cmd.Card_ID, data)
        if(succes):
            return data
        else:
            return []

    def Block_Read(self, data):
        __send_command(cmd.Block_Read, data)
    def Block_Write(self, data):
        __send_command(cmd.Block_Write, data)
    def Value_Init(self, data):
        __send_command(cmd.Value_Init, data)
    def Value_Read(self, data):
        __send_command(cmd.Value_Read, data)
    def Value_Inc(self, data):
        __send_command(cmd.Value_Inc, data)
    def Value_Dec(self, data):
        __send_command(cmd.Value_Dec, data)
    def Value_Backup(self, data):
        __send_command(cmd.Value_Backup, data)
    def Sector_Read(self, data):
        __send_command(cmd.Sector_Read, data)
    def Sector_Write(self, data):
        __send_command(cmd.Sector_Write, data)
