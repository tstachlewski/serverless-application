
"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session, speech):

    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': speech
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Main handler ------------------

def prepare_the_response(speech):
    session_attributes = {}
    card_title = ""
    speech_output = ""
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, speech))


def lambda_handler(event, context):

    print("LOG")
    print(event['request']['intent']['slots'])
    name = event['request']['intent']['slots']['name']['value']
    i = name.rfind(' ')
    if (i != -1):
        name = name[i+1:]

    print (name)

    name = name.lower()

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_NAME'])
    items = table.query(KeyConditionExpression=Key('name').eq(name))
    url = items['Items'][0]['url']

    speech = '<speak><audio src="' + url +'"/></speak>'

    return prepare_the_response(speech)

    
