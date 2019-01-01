#!/usr/bin/python

# -----------------------
# Import required Python libraries
# -----------------------

import pantilthat
import time

try:
    from flask import Flask, render_template, request
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

from flask import Flask, render_template, request

lastmove = ""

pantilthat.light_mode(pantilthat.WS2812)
pantilthat.light_type(pantilthat.GRBW)

direction = 0
angle = 0

def neoPixelLight(red, green, blue):
    pantilthat.set_all(red, green, blue)
    pantilthat.show()
    return

def lightOn():
    neoPixelLight(255,255,255)
    return

def lightOff():
    neoPixelLight(0,0,0)
    return

def going_Left():
    global direction
    direction = direction - 1
    if direction < -88 or direction > 88:
        return
    else:
        pantilthat.pan(direction)
    return

def going_Right():
    global direction
    direction = direction + 1
    if direction < -88 or direction > 88:
        return
    else:
        pantilthat.pan(direction)
    return

app = Flask(__name__)

@app.route("/")
@app.route("/<state>")
def update_robot(state=None):
    if state == 'left':
        going_Left()
    if state == 'right':
	    going_Right()
    if state == 'upward':
        going_Up()
    if state == 'downward':
	    going_Down()
    template_data = {
        'title' : state,
    }
    return render_template('main.html', **template_data)

@app.route('/lighton')
def lightonRoute():
    lightOn()
    return "Switch Lights On"

@app.route('/lightoff')
def lightoffRoute():
    lightOff()
    return "Switch Lights Off"

@app.route('/api/<direction>/<int:angle>')
def api(direction, angle):
    if angle < 0 or angle > 180:
        return "{'error':'out of range'}"

    angle -= 90

    if direction == 'pan':
        pantilthat.pan(angle)
        return "{{'pan':{}}}".format(angle)

    elif direction == 'tilt':
        pantilthat.tilt(angle)
        return "{{'tilt':{}}}".format(angle)

    return "{'error':'invalid direction'}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9595, debug=True)
