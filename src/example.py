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

    #TEST ...        
if __name__ == "__main__":
    main(sys.argv)
