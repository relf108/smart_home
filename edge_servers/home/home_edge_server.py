from pyduino import * # allows easy serial communication with arduino
import time
import paho.mqtt.client as mqtt

# when the client connects to the cloud server
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")

    # subscribe to the topics relevant for this client
    client.subscribe([(temperature_topic, 0), (brightness_topic, 0)])

# when a publish message is received from the broker
def on_message(client, userdata, msg):
    print("Message received from " + str(msg.topic) + ": " + str(msg.payload))
    # decode the message
    decoded_message = str(msg.payload)
    if str(msg.topic) == temperature_topic:
        # if temperature is above 30 degrees
        if int(float(decoded_message)) > 25:
            # sound the alarm
            arduino_connection.digital_play(BUZZER_PIN, 1000)
    if str(msg.topic) == brightness_topic:
        arduino_connection.analog_write(LED_PIN, int(float(decoded_message)))

# the ip address of the cloud server
broker_ip = "54.234.179.237"

# the mqtt topics that this edge server is concerned with
temperature_topic = "smart_home/temperature"
brightness_topic = "smart_home/brightness"

# uses default serial port, baud and timeout settings for Arduino class
arduino_connection = Arduino()

# allow time for serial connection to establish
time.sleep(3)

# initialise buzzer as output
BUZZER_PIN = 11
arduino_connection.set_pin_mode(BUZZER_PIN,'O')

# initialise LED as output
LED_PIN = 10
arduino_connection.set_pin_mode(LED_PIN,'O')

# allow time to make connection
time.sleep(1)

# set up client for mqtt communication
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883, 60)

# keep network going
client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()