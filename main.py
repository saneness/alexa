import logging
import os

from config import *
from flask import Flask
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch():
    reply = "Welcome to Raspberry Pi automation"
    return reply

@ask.intent("startDevice", mapping = {"device":"device"})
def startDevice(device,room):
    device = device.lower()
    if device in DEVICES.pc.commands:
        action = DEVICES.pc.action
        reply = DEVICES.pc.reply
    else:
        action = None
        reply = f"Sorry, I don't know what {device} is"
    if action:
        eval(action)
    return statement(reply)

@ask.intent("AMAZON.FallbackIntent")
def help():
    reply = "Something went wrong, please check server logs for more information"
    return statement(reply)

@ask.intent("AMAZON.HelpIntent")
def help():
    reply = "I can only ask Raspberry Pi to launch your computer, but I hope that we will be friends and I will be able to do much more using our interaction"
    return statement(reply)

@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
