# homecontrol.py
# This is a MQTT client program that listens for changes
# to the feeds and does actions based on them
#
# For now it is just the garage door controls
#

# imports
from Adafruit_IO import MQTTClient
import time
import board
import digitalio

# Setup Adafruit IO account
ADAFRUIT_IO_KEY = '6a76fbbf0c46e84971cf5529f166c3ae3fde2b1d'
ADAFRUIT_IO_USERNAME = 'cubbagesj20879'

# Setup garage1 button
button1 = digitalio.DigitalInOut(board.D20)
button1.direction = digitalio.Direction.OUTPUT

# Setup garage2 button
button2 = digitalio.DigitalInOut(board.D16)
button2.direction = digitalio.Direction.OUTPUT

# Setup feeds
feed_one = 'door1digital'
feed_two = 'door2digital'


# Define callback functions which will be called when events happen
def connected(client):
    # Called when we connect
    print('Connected to Adafruit IO! Listening for changes...')
    client.subscribe(feed_one)
    client.subscribe(feed_two)

def disconnected(client):
    # Called on disconnect
    print('Disconnected from Adafruit IO!')
    sys.exit()

def message(client, topic_id, payload):
    # Called when subscribed feed changes
    print('Feed {0} received new value: {1}'.format(topic_id, payload))

    if topic_id == 'door1digital':

        print('Sending door 1 command..... Open Sesame!!!')
        time.sleep(5)
        # Toggle Pi pin to activate button
        # Press for 0.1s
        button1.value = True
        time.sleep(0.1)
        button1.value = False

    if topic_id == 'door2digital':

        print('Sending door 2 command..... Open Sesame!!!')
        time.sleep(5)
        # Toggle Pi pin to activate button
        # Press for 0.1s
        button2.value = True
        time.sleep(0.1)
        button2.value = False
# Create an MQTT client instance
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup callback functions
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

# Connect to Adafruit server
client.connect()

# Start a message loop the blocks forever
client.loop_blocking()

