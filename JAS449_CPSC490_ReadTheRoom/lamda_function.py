import json
import boto3

access_key = "X"
access_secret = "X"
region ="X"
queue_url = "X"

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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

def pop_message(client, url):
    response = client.receive_message(QueueUrl = url, MaxNumberOfMessages = 10)

    #last message posted becomes messages
    message = response['Messages'][0]['Body']
    receipt = response['Messages'][0]['ReceiptHandle']
    client.delete_message(QueueUrl = url, ReceiptHandle = receipt)
    return message
    
def post_message(client, message_body, url):
    response = client.send_message(QueueUrl = url, MessageBody= message_body)

    
def lambda_handler(event, context):
    client = boto3.client('sqs', aws_access_key_id = access_key, aws_secret_access_key = access_secret, region_name = region)
    intent_name = event['request']['intent']['name']
    if intent_name == "Listen":
        post_message(client, 'Listening', queue_url)
        message = "I'm Listening"
    elif intent_name == "Respond":
        post_message(client, 'Responding', queue_url)
        message = "I think you should play" + str(pop_message(client, queue_url))
    else:
        message = "Unknown"
        
    speechlet = build_speechlet_response("Room Status", message, "", "true")
    return build_response({}, speechlet)
