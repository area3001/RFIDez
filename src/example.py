'''
Created on 15 okt. 2013

@author: bert
'''

import sys
sys.path.append("../yhy522")
import yhy522

def main(argv):
    #TEST Test_Com
    print "Test_Com([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])"
    if(yhy522.Test_Com([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])):
    	print "Test_Com succes"
    else:
    	print "Test_Com failed"
    
    #TEST Card_ID
    print "Card_ID()"
    try:
        card_id = yhy522.Card_ID()
        result = "Card ID Succes: "
        for c in card_id:
            result += format(c, 'X')
        print result
    except Exception as e:
        print "Card_ID() Failed"

    #TEST Card_Type
    print "Card_Type()"
    try:
        card_type = yhy522.Card_Type()
        print "Card Type = {0}".format(card_type, '02X')
    except Exception as e:
        print "Card_Type() Failed"   

    #TEST Antenna_Control
    print "Antenna_Control()"
    if(yhy522.Antenna_Control(False)):
    	print "Setting antenna OFF: Succes"
    else:
		print "Setting antenna OFF: Failed"  
    if(yhy522.Antenna_Control(True)):
    	print "Setting antenna ON: Succes"
    else:
		print "Setting antenna ON: Failed"    	

    #TEST Sense_Mode
    print "Sense_Mode()"
    if(yhy522.Sense_Mode(1)):
        print "Setting sense mode to 'Auto seek card': Succes"
    else:
        print "Setting sense mode to 'Auto seek card': Failed"

if __name__ == "__main__":
    main(sys.argv)
