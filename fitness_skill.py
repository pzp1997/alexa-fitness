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
    # DEBUG ONLY
    print 'starting workout'

    with open('defaultWorkouts.json') as fp:
        default_workouts = json.load(fp)

    exercises = default_workouts['default']['exercises']

    speech_text = render_template('startWorkout',
                                  activity=exercises[0]['activity'],
                                  repetitions=exercises[0]['repititions'])

    session.attributes['workout'] = exercises
    session.attributes['activity_number'] = 0
    session.attributes['repitition_count'] = 1

    return question(speech_text).reprompt(speech_text)


@ask.intent('AMAZON.YesIntent')
def start_count():
    speech_text = render_template('startCount')
    return question(speech_text).reprompt(speech_text)


def next_exercise(leftover_speech_response=None):
    workout = session.attributes.get('workout')
    activity_number = session.attributes.get('activity_number')
    if workout is None or activity_number is None:
        return welcome_and_help()

    activity_number += 1

    try:
        exercise = workout[activity_number]
    except IndexError:
        speech_text = render_template('completedWorkout')
        return statement(speech_text)
    else:
        speech_text = render_template('nextExercise',
                                      activity=exercise['activity'],
                                      repetitions=exercise['repititions'])
        if leftover_speech_response:
            speech_text = render_template('addLeftover',
                                          leftover=leftover_speech_response,
                                          original=speech_text)

        # DEBUG ONLY
        print speech_text

        session.attributes['activity_number'] = activity_number
        session.attributes['repitition_count'] = 1
        return question(speech_text).reprompt(speech_text)


@ask.intent('CountWithMeIntent', convert={'number': int})
def count_with_me_intent(number):
    # DEBUG ONLY
    print 'counting... {}'.format(number)

    workout = session.attributes.get('workout')
    activity_number = session.attributes.get('activity_number')
    rep_count = session.attributes.get('repitition_count')
    if rep_count is None or activity_number is None or rep_count is None:
        return welcome_and_help()

    if number is not None and number == rep_count + 1:
        rep_count += 2
        speech_text = '{}!'.format(rep_count)
        session.attributes['repitition_count'] = rep_count

        number_of_reps = workout[activity_number]['repititions']
        if number_of_reps - number < 2:
            return (next_exercise()
                    if number_of_reps == number
                    else next_exercise(speech_text))
    else:
        speech_text = '{}!'.format(rep_count)

    return question(speech_text).reprompt(speech_text)


@ask.intent('AMAZON.NextIntent')
def skip_exercise():
    return next_exercise()


@ask.intent('AMAZON.HelpIntent')
def help_():
    return welcome_and_help()


@ask.intent('AMAZON.StopIntent')
def stop():
    return stop_and_cancel()


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return stop_and_cancel()


@ask.session_ended
def session_ended():
    return '', 200


def stop_and_cancel():
    speech_text = render_template('exit')
    return statement(speech_text)


def welcome_and_help():
    speech_text = render_template('welcome')
    return question(speech_text).reprompt(speech_text)

if __name__ == '__main__':
    app.run(debug=True)
