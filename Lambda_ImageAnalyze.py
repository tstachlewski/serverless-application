import boto3
import io

def lambda_handler(event, context):

    key = event['Records'][0]['s3']['object']['key']
    bucket = event['Records'][0]['s3']['bucket']['name']
    txtName = key[7:-4] + ".txt"


    # Invoke Rekognition service
    client = boto3.client('rekognition')
    response = client.recognize_celebrities(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        }
    )
    
    celebrity = response['CelebrityFaces'][0]['Name']
    print 'TTTTT'
    
    

    text = "I see " + celebrity + ' on the picture'

    with io.FileIO("/tmp/" + txtName, "w") as file:
        file.write(text)

    #Save a file with description in S3
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/' + txtName, bucket, 'text/Joanna/' + txtName)

    return 'Done'
