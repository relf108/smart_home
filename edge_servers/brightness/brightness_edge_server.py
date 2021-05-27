from pyduino import * # allows easy serial communication with arduino
import time
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# when the client connects to the cloud server
def on_connect(client, userdata, flags, rc):
    print("Connected")

    # subscribe to the topics relevant for this client
    client.subscribe(motion_state_topic)
    
# when a publish message is received from the broker
def on_message(client, userdata, msg):
    print("Msg Received: " + str(msg.payload))
    # if there has been motion
    if str(msg.topic) == motion_state_topic and msg.payload != '0':
        # 'engage' this edge server for the next five minutes
        time_for_disengagement = datetime.now() + (timedelta(minutes=5))

# the ip address of the cloud server
broker_ip = "54.234.179.237"
time_for_disengagement:datetime = datetime.now()

# the mqtt topics that this edge server is concerned with
motion_state_topic = "smart_home/motion_state"
brightness_topic = "smart_home/brightness"

# the "timestamp" generated for when the system will disengage (will be 5 minutes after last motion detection)

# uses default serial port, baud and timeout settings for Arduino class
arduino_connection = Arduino()

# allow time for serial connection to establish
time.sleep(3)

# initialise soft potentiometer sensor as input
SOFTPOT_PIN = 2
arduino_connection.set_pin_mode(SOFTPOT_PIN,'I')

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
        while datetime.now() < time_for_disengagement:
            # read softpot value from Arduino
            softpot_value = arduino_connection.analog_read(SOFTPOT_PIN)
            # convert softpot scale from 0 - 1023 to 0 - 255 and set the LED accordingly
            brightness = (255 / 1023) * float(softpot_value)
            publish.single(brightness_topic, brightness, hostname=broker_ip)
            time.sleep(1)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()