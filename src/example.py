'''
Created on 15 okt. 2013

@author: bert
'''

import sys
sys.path.append("../yhy522")
import yhy522commands as commands
import time

def main(argv):
    #TEST Test_Com
    print "Test_Com([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])"
    if(commands.Test_Com([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])):
    	print "Test_Com succes"
    else:
    	print "Test_Com failed"
    
    #TEST Card_ID
    print "Card_ID()"
    try:
        card_id = commands.Card_ID()
        result = "Card ID Succes: "
        for c in card_id:
            result += format(c, 'X')
        print result
    except Exception as e:
        print "Card_ID() Failed"

    #TEST Card_Type
    print "Card_Type()"
    try:
        card_type = commands.Card_Type()
        print "Card Type = {0}".format(card_type, '02X')
    except Exception as e:
        print "Card_Type() Failed"   

    #TEST Antenna_Control
    print "Antenna_Control()"
    if(commands.Antenna_Control(False)):
    	print "Setting antenna OFF: Succes"
    else:
		print "Setting antenna OFF: Failed"  
    if(commands.Antenna_Control(True)):
    	print "Setting antenna ON: Succes"
    else:
		print "Setting antenna ON: Failed"    	

    #TEST Sense_Mode
    print "Sense_Mode()"
    if(commands.Sense_Mode(1)):
        print "Setting sense mode to 'Auto seek card': Succes"
    else:
        print "Setting sense mode to 'Auto seek card': Failed"

    #TEST Beep
    print "Beep()"
    if(commands.Beep(True, 1)):
        print "Beep success"
    else:
        print "Beep failed"

    #TEST SetAutoModeOff
    #print "SetAutoModeOff()"
    #if(commands.SetAutoModeOff()):
    #    print "SetAutoModeOff success"
    #else:
    #    print "SetAutoModeOff failed"

    #TEST SetAutoSeekCardMode
    #print "SetAutoSeekCardMode()"
    #if(commands.SetAutoSeekCardMode()):
    #    print "SetAutoSeekCardMode success"
    #else:
    #    print "SetAutoSeekCardMode failed"

    #TEST SetAutoSeekCardMode
    #print "SetAutoReadIdMode()"
    #if(commands.SetAutoReadIdMode()):
    #    print "SetAutoReadIdMode success"
    #else:
    #    print "SetAutoReadIdMode failed"

    while 1:
       time.sleep(1)

if __name__ == "__main__":
    main(sys.argv)
