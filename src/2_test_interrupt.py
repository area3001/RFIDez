'''
Created on 15 okt. 2013

@author: bert
'''
import sys
import time
import mosquitto
sys.path.append("../yhy522")
import yhy522commands as yhy522

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

# set mosquitto client
#client = mosquitto.Mosquitto(client_id, clean_session=True, obj=None)
client = mosquitto.Mosquitto("test-client")

def my_callback_one(channel):
    print('********************************')
    #GPIO.input(channel):
    sys.stdout.write("Card_ID:")
    yhy522.Card_ID()
    print('Sending MQTT command')
    client.publish("/fablab/log/hostname", "hello world", 0)
    time.sleep(1)

def main(argv):
#     print '0x%.2x' % yhy522.calculate_checksum(0x03, [0x01,0x02,0x03])
#    print "Test_Com(0x44)"
#    yhy522.Test_Com([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])
#   print "Card_ID()"
#   yhy522.Card_ID()
#     yhy522.Card_ID(data)

    #client.connect(hostname, port=1883, keepalive=60)
    client.connect("192.168.1.146")

    # setup yhy522
    yhy522.Sense_Mode([0x01])
    channel = 23
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(channel, GPIO.FALLING)
    GPIO.add_event_callback(channel, my_callback_one)
    #GPIO.add_event_callback(channel, my_callback_two)

    while 1:
       time.sleep(1)
       #client.loop(timeout=-1)
       client.loop()

if __name__ == "__main__":
    main(sys.argv)
