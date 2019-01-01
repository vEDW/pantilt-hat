#!/usr/bin/env python

import pantilthat
from sys import exit

try:
    from flask import Flask, render_template
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

app = Flask(__name__)

pantilthat.light_mode(pantilthat.WS2812)
pantilthat.light_type(pantilthat.GRBW)

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

@app.route('/lighton')
def lightonRoute():
    lightOn()
    return "Switch Lights On"

@app.route('/lightoff')
def lightoffRoute():
    lightOff()
    return "Switch Lights Off"

@app.route('/')
def home():
    return render_template('gui.html')

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

