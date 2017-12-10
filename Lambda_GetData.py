import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
import json

def lambda_handler(event, context):

    name = event["queryStringParameters"]["name"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_NAME'])

    items = table.query(KeyConditionExpression=Key('name').eq(name))

    url = items['Items'][0]['url']
    
    return {
            'statusCode': "200",
            'body': " \
                <html> \
                    <div style='text-align: center'> \
                        <br/><br/><br/><br/><br/><br/><br/><br/>\
                        <img src='http://bit.ly/1fDRUZk' width=300><br/><br/><br/><br/> \
                    <body bgcolor='#e6eeff'> \
                        <audio controls><source src='" + url + "' type='audio/mp3'></audio> \
                    </body> \
                    </div> \
                </html>",
            'headers': {
                'Content-Type': 'text/html',
            }
        }
