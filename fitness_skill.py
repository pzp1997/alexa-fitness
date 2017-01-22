import json
import logging

from flask import Flask
from flask import render_template
from flask_ask import Ask
# from flask_ask import request
from flask_ask import session
from flask_ask import question
from flask_ask import statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = render_template('welcome')
    return question(speech_text).reprompt(speech_text)


@ask.intent('StartWorkoutIntent')
def hello_world():
    speech_text = render_template('start')
    default_workouts = json.load('defaultWorkouts.json')
    session.attributes['workout'] = default_workouts['default']
    session.attributes['activity_number'] = 0
    return statement(speech_text).simple_card('HelloWorld', speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = render_template('welcome')
    return question(speech_text).reprompt(speech_text)


@ask.session_ended
def session_ended():
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
