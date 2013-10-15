'''
Created on 15 okt. 2013

@author: bert
'''

import sys
from yhy522 import yhy522

def main(argv):
#     print '0x%.2x' % yhy522.calculate_checksum(0x03, [0x01,0x02,0x03])
#     yhy522.Test_Com(0x445566)
    yhy522.Card_ID(0x20)
#     yhy522.Card_ID(data)

if __name__ == "__main__":
    main(sys.argv)