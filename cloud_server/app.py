import time
import datetime
import paho.mqtt.publish as publish
from datetime import datetime, timedelta
from flask import Flask, Response, jsonify, make_response, request, render_template
import json
app = Flask(__name__)

# End point to do stuff (temperature,..)


@app.route('/temperature')
def getTemp():
    with open('cloud_server/home_data.json') as f:
        data = json.load(f)
    resp = {'temp': data['temperature']}
    return resp


@app.route('/brightness')
def getBrightness():
    with open('cloud_server/home_data.json') as f:
        data = json.load(f)
    resp = {'brightness': data['brightness']}
    return resp


@app.route('/motion_state')
def getMotionState():
    with open('cloud_server/home_data.json') as f:
        data = json.load(f)
    resp = {'motion_state': data['motion_state']}
    return resp
