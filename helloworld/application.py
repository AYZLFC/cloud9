#!flask/bin/python
import json
from flask import Flask, Response
from helloworld.flaskrun import flaskrun
import requests
import boto3
from flask_cors import CORS

application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}})

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    

#Gets all animals from dynmoDB
@application.route('/get_animalTable', methods=['GET'])
def get_frm():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('animalTable')
    
    resp = table.scan()
    #print(str(resp))
    return Response(json.dumps(str(resp['Items'])), mimetype='application/json', status=200)



#Send photo from S3 to Rekognition and gets lables 
#/<bucket>/<image> #not so relevent
@application.route('/analyze', methods=['GET'])
def analyze(bucket='savepics', image='pekignese.jpeg'): #we need to change the name of the image to somthing constant and to make sure to set this name on the React code as the name of the image when user add an image
    return detect_labels(bucket, image)
    
    
def detect_labels(bucket, key, max_labels=10, min_confidence=50, region="us-east-1"):
    
    rekognition = boto3.client("rekognition", region)
    s3 = boto3.resource('s3', region_name = 'us-east-1')
    
    image = s3.Object(bucket, key) # Get an Image from S3
    
    img_data = image.get()['Body'].read() # Read the image

    response = rekognition.detect_labels(
        Image={
            'Bytes': img_data
        },
        MaxLabels=max_labels,
		MinConfidence=min_confidence,
    )
    
    return json.dumps(response['Labels'])



if __name__ == '__main__':
    flaskrun(application)
