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

direction = 48
angle = 0
maxdirection = 80
maxangle = 70
red = 0
green = 0 
blue = 0

pantilthat.pan(direction)
pantilthat.tilt(angle)

def neoPixelLight():
    global red
    global green
    global blue 
    pantilthat.set_all(red, green, blue)
    pantilthat.show()
    return

def lightOn():
    global red
    global green
    global blue 
    red = 255
    green = 255
    blue = 255
    neoPixelLight()
    return

def lightOnMedium():
    global red
    global green
    global blue 
    red = 90
    green = 90
    blue = 90
    neoPixelLight()
    return

def lightOff():
    global red
    global green
    global blue 
    red = 0
    green = 0
    blue = 0
    neoPixelLight()
    return

def going_Left():
    global direction
    #print "direction : " + str(direction)
    if direction < maxdirection:
        direction = direction + 1
        pantilthat.pan(direction)
    return

def going_Right():
    global direction
    #print "direction : " + str(direction)
    if direction > -maxdirection:    
        direction = direction - 1
        pantilthat.pan(direction)
    return

def going_Up():
    global angle
    #print "angle : " + str(angle)
    if angle > -maxangle:
        angle = angle - 1
        pantilthat.tilt(angle)
    return

def going_Down():
    global angle
    #print "angle : " + str(angle)
    if angle < maxangle:
        angle = angle + 1
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
    if state == 'lightonmedium':
        lightOnMedium()
    if state == 'lightoff':
	    lightOff()
    template_data = {
        'title' : state,
        'angleValue' : angle,
        'directionValue' : direction,
         'redValue' : red,
        'greenValue' : green,
        'blueValue' : blue,
    }
    return render_template('main.html', **template_data)

@app.route("/light/<redint>/<greenint>/<blueint>")
def set_light(redint,greenint,blueint):
    state = None
    global red
    global green
    global blue
    redint = int(redint)
    greenint = int(greenint)
    blueint = int(blueint)
    
    if redint >= 0 and redint <=255:
        print "set redint : " + str(redint)
        red = redint
    if greenint >= 0 and greenint <=255:
        green = greenint
    if blueint >= 0 and blueint <=255:
        blue = blueint
    neoPixelLight()

    template_data = {
        'title' : state,
        'angleValue' : angle,
        'directionValue' : direction,
        'redValue' : red,
        'greenValue' : green,
        'blueValue' : blue,
    }
    return render_template('main.html', **template_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9595, debug=True)
