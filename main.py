import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

PC_DEVICES = {
    "pc"         : "your pc",
    "computer"   : "your computer", 
    "my pc"      : "your pc",
    "my computer": "your computer"
}

@ask.launch
def launch():
    speech_text = "Welcome to Raspberry Pi Automation."
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent("startDevice", mapping = {"device":"device"})
def startDevice(device,room):
    if device.lower() in PC_DEVICES:
        os.system("/usr/local/bin/wol")
        return statement(f"Turning {PC_DEVICES[device.lower()]} on.")
    else:
        return statement(f"Sorry, I don't know what {device.lower()} is.")    
 
@ask.intent("AMAZON.HelpIntent")
def help():
    speech_text = "You can control Raspbery Pi with me!"
    return question(speech_text).reprompt(speech_text).simple_card("Raspbery Pi", speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
