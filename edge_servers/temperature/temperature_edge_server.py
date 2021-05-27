from pyduino import * # allows easy serial communication with arduino
import time
from datetime import datetime
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
        time_for_disengagement = datetime.now() + datetime.timedelta(minutes=5)

# the ip address of the cloud server
broker_ip = "54.234.179.237"

# the mqtt topics that this edge server is concerned with
motion_state_topic = "smart_home/motion_state"
temperature_topic = "smart_home/temperature"

# the "timestamp" generated for when the system will disengage (will be 5 minutes after last motion detection)
time_for_disengagement = datetime.now()

# uses default serial port, baud and timeout settings for Arduino class
arduino_connection = Arduino()

# allow time for serial connection to establish
time.sleep(3)

# initialise temperature sensor as input
TEMPERATURE_PIN = 0
arduino_connection.set_pin_mode(TEMPERATURE_PIN,'I')

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
            # read temperature from Arduino
            read_value = arduino_connection.analog_read(TEMPERATURE_PIN)
            # convert to voltage
            voltage = read_value * 5.0
            voltage /= 1024.0
            # convert to celsius with 500 mV offset
            temperature = (voltage - 0.5) * 100
            publish.single(temperature_topic, temperature, hostname=broker_ip)
            time.sleep(1)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()