#!/usr/bin/python

# -----------------------
# Import required Python libraries
# -----------------------

import explorerhat
import time
from flask import Flask, render_template, request

timelength =  3
lastmove = ""


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def going_Left():
    global timelength
    global lastmove
    if lastmove == 'right':
        explorerhat.motor.one.forward()
        time.sleep(timelength*2)
        explorerhat.motor.one.stop()

    explorerhat.motor.one.forward()
    time.sleep(timelength)
    explorerhat.motor.one.stop()
    lastmove = 'left'

def going_Right():
    global timelength
    global lastmove
    if lastmove == 'left':
        explorerhat.motor.one.backward()
        time.sleep(timelength*2)
        explorerhat.motor.one.stop()
    explorerhat.motor.one.backward()
    time.sleep(timelength)
    explorerhat.motor.one.stop()
    lastmove = 'right'

app = Flask(__name__)

@app.route("/")
@app.route("/<state>")
def update_robot(state=None):
    if state == 'left':
        going_Left()
    if state == 'right':
	going_Right()
    if state == 'kill':
        shutdown_server()
    template_data = {
        'title' : state,
    }
    return render_template('main.html', **template_data)


@app.errorhandler(404)
def not_found(error):
	return "You're doomed !", 404



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
