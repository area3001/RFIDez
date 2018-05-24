import time
import paho.mqtt.client as mqtt
import yhy522
# Try to connect with GPIO
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

# CONSTANTS
SERVER_IP = '192.168.1.146'

# Variables
card_id = [0,0,0,0]

# setup mqtt client and connect to it
#client = mqtt.Client(client_id, clean_session=True, obj=None)
client = mqtt.Client("rfid-reader1")
client.connect(SERVER_IP)       #client.connect(hostname, port=1883, keepalive=60)

# Setup RFID
rfid = yhy522.Yhy522()

def read_card_send_MQTT(channel):
    # Read card
    global card_id
    print('********************************')
    card_id = rfid.Card_ID()

    # send MQTT
    payload = ', '.join(map(str, card_id))
    client.publish("/fablab/log/laser/black", payload, 0)      #client.publish(topic, payload=None, qos=0, retain=false)

def main():
    global card_id

    # setup yhy522 Card Reader to callback on card present
    rfid.Sense_Mode(0x01)
    channel = 23
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(channel, GPIO.FALLING)
    GPIO.add_event_callback(channel, read_card_send_MQTT, bouncetime=400)

    # loop to detect when card is removed
    while 1:
        continue
        # Read the Card ID and compare with the previously stored value
        try:
            newly_read_card_id = rfid.Card_ID()
            if not(card_id == newly_read_card_id):
                card_id = newly_read_card_id
                payload = ', '.join(map(str, card_id))
                client.publish("/fablab/log/laser/black", payload, 0)

        except:
            print("Could read card ID")

        client.loop()     # Need to call this to process MQTT messages
        time.sleep(1)

if __name__ == "__main__":
    main()
