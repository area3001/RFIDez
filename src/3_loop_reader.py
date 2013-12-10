'''
Created on 10 dec. 2013

@author: Paul 
'''
import sys
import time
import mosquitto
sys.path.append("../yhy522")
import yhy522commands as yhy522

# CONSTANTS 
SERVER_IP = '192.168.1.146'
MQTT_QOS = 1

# Variables
card_id = [0,0,0,0]
topic = "/fablab/log/laser/black"

# Try to connect with GPIO 
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

# setup mosquitto client and connect to it
#client = mosquitto.Mosquitto(client_id, clean_session=True, obj=None)
client = mosquitto.Mosquitto("rfid-reader1")
client.connect(SERVER_IP)       #client.connect(hostname, port=1883, keepalive=60)

def read_card():
    # Read card, returns True if the card is new, and stores the global card_id
    global card_id
    result = False  
    try:
        newly_read_card_id = yhy522.Card_ID()
        if not(card_id == newly_read_card_id): 
            card_id = newly_read_card_id
            result = True
            #print("Different !!!") 
    except:
        print("Could NOT read card ID")
    return result

def send_MQTT(): 
    global card_id
    # send MQTT
    payload = '[' + ', '.join(map(hex, card_id)) + ']'
    client.publish(topic, payload, MQTT_QOS)      #client.publish(topic, payload=None, qos=0, retain=false)
    print("MQTT:" + topic + " , " + payload) 

def main(argv):
    while 1:
        # If Card is new, send MQTT 
        if(read_card()):
            send_MQTT()
 
        client.loop()     # Need to call this to process MQTT messages
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv)
