from pyduino import * # allows easy serial communication with arduino
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# when the client connects to the cloud server
def on_connect(client, userdata, flags, rc):
    print("Connected")

# when a publish message is received from the broker
def on_message(client, userdata, msg):
    print("Msg Received: " + str(msg.payload))

# the ip address of the cloud server
broker_ip = "54.234.179.237"

# the mqtt topics that this edge server is concerned with
motion_state_topic = "smart_home/motion_state"

# uses default serial port, baud and timeout settings for Arduino class
arduino_connection = Arduino()

# allow time for serial connection to establish
time.sleep(3)

# initialise motion sensor as input
MOTION_PIN = 11
arduino_connection.set_pin_mode(MOTION_PIN,'I')

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
        # read motion state from Arduino
        motion_state = arduino_connection.digital_read(MOTION_PIN)
        # publish if there is motion
        if motion_state != '0':
            publish.single(motion_state_topic, motion_state, hostname=broker_ip)
        time.sleep(1)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()