import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import os
import time
import sys
# connecting to itself


def on_connect(client, userdata, flags, rc):
    print("Connected")

    # subscribe to every topic
    client.subscribe(
        [(motion_state_topic, 0), (temperature_topic, 0), (brightness_topic, 0)])

# when receiving a message


def on_message(client, userdata, msg):
    print("Message received from " + str(msg.topic) + ": " + str(msg.payload))

    if str(msg.topic) == motion_state_topic:
        smart_home_data['motion_state'] = extractPayload(msg.payload)
        with open("cloud_server/home_data.json", "w") as outfile:
            json.dump(smart_home_data, outfile)

    if str(msg.topic) == temperature_topic:
        smart_home_data['temperature'] = extractPayloadTemp(msg.payload)
        with open("cloud_server/home_data.json", "w") as outfile:
            json.dump(smart_home_data, outfile)

    if str(msg.topic) == brightness_topic:
        smart_home_data['brightness'] = extractPayload(msg.payload)
        with open("cloud_server/home_data.json", "w") as outfile:
            json.dump(smart_home_data, outfile)


def extractPayload(payload):
    payload = str(payload)
    res = payload.split("'")
    return int(res[1])

def extractPayloadTemp(payload):
    payload = str(payload)
    res = payload.split("'")
    return int(float(res[1]))

thingsboard_host = 'localhost:8080'
access_token = '12345'

# the ip address of the cloud server, i.e. own ip address
broker_ip = '54.234.179.237'

# the json representation of all the smart home data, for sending to ThingsBoard

# Data to be written

smart_home_data = {'temperature': 0, 'brightness': 0, 'motion_state': 0}


# all the mqtt topics
motion_state_topic = "smart_home/motion_state"
brightness_topic = "smart_home/brightness"
temperature_topic = "smart_home/temperature"

# set up client for mqtt communication
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(access_token)  # for accessing the ThingsBoard device
client.connect(broker_ip, 1883, 60)

# keep network going in a separate thread
client.loop_start()

# endless loop in this thread
while True:
    # send all smart home data to ThingsBoard
    #client.publish('v1/devices/me/telemetry', json.dumps(smart_home_data), 1)

    time.sleep(1)

client.loop_stop()
client.disconnect()
