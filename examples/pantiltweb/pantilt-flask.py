#!/usr/bin/python

# -----------------------
# Import required Python libraries
# -----------------------

import pantilthat

try:
    from flask import Flask, render_template, request
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

from flask import Flask, render_template, request

pantilthat.light_mode(pantilthat.WS2812)
pantilthat.light_type(pantilthat.GRBW)

direction = 0
angle = 0

pantilthat.pan(direction)
pantilthat.tilt(angle)

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
    print "direction : " + direction
    if direction < -88 or direction > 88:
        return
    else:
        pantilthat.pan(direction)
    return

def going_Right():
    global direction
    direction = direction + 1
    print "direction : " + direction
    if direction < -88 or direction > 88:    
        return
    else:
        pantilthat.pan(direction)
    return

def going_Up():
    global angle
    angle = angle - 1
    print "angle : " + angle
    if angle < -88 or angle > 88:
        return
    else:
        pantilthat.tilt(angle)
    return

def going_Down():
    global angle
    angle = angle + 1
    print "angle : " + angle
    if angle < -88 or angle > 88:
        return
    else:
        pantilthat.tilt(angle)
    return

app = Flask(__name__)

@app.route("/")
@app.route("/<state>")
def update_pantilt(state=None):
    if state == 'left':
        going_Left()
    if state == 'right':
	    going_Right()
    if state == 'upward':
        going_Up()
    if state == 'downward':
	    going_Down()
    if state == 'lighton':
        lightOn()
    if state == 'lightoff':
	    lightOff()
    template_data = {
        'title' : state,
    }
    return render_template('main.html', **template_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9595, debug=True)
