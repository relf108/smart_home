from pyduino import *  # allows easy serial communication with arduino
import time
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

# when the client connects to the cloud server


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")

    # subscribe to the topics relevant for this client
    client.subscribe(motion_state_topic)


# when a publish message is received from the broker


def on_message(client, userdata, msg):
    print("Message received from " + str(msg.topic) + ": " + str(msg.payload))
    # if there has been motion
    # if str(msg.topic).decode('UTF-8') == motion_state_topic and str(msg.payload) != '0':
    with open('cloud_server/home_data.json') as f:
            smart_home_data = json.load(f)
            motion_state = smart_home_data['motion_state']
    # 'engage' this edge server for the next five minutes


# the ip address of the cloud server
broker_ip = "54.234.179.237"

with open('cloud_server/home_data.json') as f:
    smart_home_data = json.load(f)
    motion_state = smart_home_data['motion_state']


# the mqtt topics that this edge server is concerned with
motion_state_topic = "smart_home/motion_state"
brightness_topic = "smart_home/brightness"

# the "timestamp" generated for when the system will disengage (will be 5 minutes after last motion detection)
#time_for_disengagement = datetime.datetime.now()


# uses default serial port, baud and timeout settings for Arduino class
arduino_connection = Arduino()

# allow time for serial connection to establish
time.sleep(3)

# initialise potentiometer sensor as input
POTENTIOMETER_PIN = 0
arduino_connection.set_pin_mode(POTENTIOMETER_PIN, 'I')

# allow time to make connection
time.sleep(1)

# set up client for mqtt communication
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883, 60)

# keep network going in a separate thread
client.loop_start()

# endless loop in this thread

try:
    while True:
        # while this edge server is engaged
        with open('cloud_server/home_data.json') as f:
            smart_home_data = json.load(f)
            motion_state = smart_home_data['motion_state']
        # while this edge server is engaged
        while motion_state == 1:
            # read softpot value from Arduino
            potentiometer_value = arduino_connection.analog_read(
                POTENTIOMETER_PIN)
            print(potentiometer_value)
            # convert softpot scale from 0 - 1023 to 0 - 255 and set the LED accordingly
            brightness = (255 / 1023) * float(potentiometer_value)
            brightness = int(float(brightness))
            publish.single(topic=brightness_topic,
                           payload=brightness, hostname=broker_ip)
        time.sleep(1)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
