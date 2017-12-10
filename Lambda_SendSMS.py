import boto3
import os

sns = boto3.client('sns')

def lambda_handler(event, context):
    
    
    sns.publish(
        TopicArn = os.environ['SNS_TOPIC'],
        Message = event['Records'][0]['dynamodb']['NewImage']['url']['S']
    )
    
    return "I've just send SMS!"
