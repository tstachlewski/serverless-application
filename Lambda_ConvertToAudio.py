import boto3
import uuid
import os
from contextlib import closing

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    voice = key[5:][:key[5:].find("/")]
    fileName = key[5:][key[5:].find("/")+1:]

    print "Text-To-Speech function"
    print "Bucket: " +  bucket
    print "Key: " +  key
    print "Voice: " + voice
    print "File name: " + fileName

    # Saving file in local directory
    s3 = boto3.resource('s3')
    s3.meta.client.download_file(bucket, key, "/tmp/"+fileName)

    # Reading a file
    with open("/tmp/"+fileName, 'r') as myfile:
        content=myfile.read().replace('\n', '')

    # Using Amazon Polly service to convert text to speech
    polly = boto3.client('polly')
    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=content,
        TextType='text',
        VoiceId=voice
    )

    # Save audio on local directory
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join("/tmp/", fileName)
            with open(output, "a") as file:
                file.write(stream.read())

    # Save audio file on S3
    newKey = "audio/" + fileName[:-4] + ".mp3"
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/' + fileName, bucket, newKey)
    s3.put_object_acl(ACL='public-read', Bucket=bucket, Key= newKey)

    #Creating new record in DynamoDB table
    location = s3.get_bucket_location(Bucket=bucket)
    region = location['LocationConstraint']

    if region is None:
        url_begining = "https://s3.amazonaws.com/"
    else:
        url_begining = "https://s3-" + str(region) + ".amazonaws.com/" \

    url = url_begining + bucket + "/" + newKey

    #Adding information about new audio file to DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_NAME'])
    table.put_item(
        Item={
            'name' : fileName[:-4],
            'text' : content,
            'voice' : voice,
            'url' : url
        }
    )

    return 'Everything when well!'
