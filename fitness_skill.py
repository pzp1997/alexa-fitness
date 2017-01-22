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
    return welcome_and_help()


@ask.intent('StartWorkoutIntent')
def start_workout_intent():
    ## DEBUG ONLY
    print 'starting workout'

    with open('defaultWorkouts.json') as fp:
        default_workouts = json.load(fp)

    exercises = default_workouts['default']['exercises']

    speech_text = render_template('startWorkout',
                                  activity=exercises[0]['activity'],
                                  repetitions=exercises[0]['repititions'])

    session.attributes['workout'] = exercises
    session.attributes['activity_number'] = 1

    return question(speech_text).reprompt(speech_text)


@ask.intent('AMAZON.YesIntent')
def next_exercise():
    workout = session.attributes.get('workout')
    activity_number = session.attributes.get('activity_number')

    if workout is not None and activity_number is not None:
        try:
            exercise = workout[activity_number]
        except IndexError:
            speech_text = render_template('completedWorkout')
            return statement(speech_text)
        else:
            speech_text = render_template('nextExercise',
                                          activity=exercise['activity'],
                                          repetitions=exercise['repititions'])
            session.attributes['activity_number'] += 1
            return question(speech_text).reprompt(speech_text)
    else:
        return welcome_and_help()


@ask.intent('AMAZON.HelpIntent')
def help_():
    return welcome_and_help()


@ask.intent('AMAZON.StopIntent')
def stop():
    return stop_and_canel()


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return stop_and_canel()


@ask.session_ended
def session_ended():
    return '', 200


def stop_and_canel():
    speech_text = render_template('exit')
    return statement(speech_text)


def welcome_and_help():
    speech_text = render_template('welcome')
    return question(speech_text).reprompt(speech_text)



if __name__ == '__main__':
    app.run(debug=True)
