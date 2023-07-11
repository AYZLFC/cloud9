#!flask/bin/python
import json
from flask import Flask, Response , request
from helloworld.flaskrun import flaskrun
import requests
import boto3
from flask_cors import CORS
import json
from bl import animal_details as animal_details
from bl import handle_request_data as imageToS3




application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}})

# @application.route('/', methods=['GET'])
# def get():
#     return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

# @application.route('/', methods=['POST'])
# def post():
#     return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
#This route for uploading an image to S3 bucket
@application.route('/upload_image', methods=['POST'])
def upload_image():
    # Retrieve the file from the POST request
    file = request.files['file']
    
    # Deliver the request content to bl.py
    response = imageToS3(file, bucket = 'savepics', region = "us-east-1")
    
    if(response):
        return Response('File uploaded successfully.', mimetype='application/json', status=200)
    else:
        #print( f'Error uploading file: {str(e)}')
        return Response('Error uploading file', mimetype='application/json', status=200)

#This route for get the animal's details
@application.route('/animal_details', methods=['GET','POST'])
def get_animal_details():
    details=animal_details(bucket="savepics", image_name=request.data , region="us-east-1", table_name="animalTable") #we need to change the name of the image to somthing constant and to make sure to set this name on the React code as the name of the image when user add an image
    
    return Response(json.dumps(details), mimetype='application/json', status=200)

# # #Gets all animals from dynmoDB
# @application.route('/get_animalTable', methods=['GET'])
# def get_animalTable():
#     my_dyno = dyno('us-east-1', 'animalTable') #need to be move to bl.py
#     return Response((my_dyno), mimetype='application/json', status=200)

# def dyno(region, table_name):
#     dynamodb = boto3.resource('dynamodb', region_name=region)
#     table = dynamodb.Table(table_name)
#     resp = table.scan()
#     #print(str(resp))
    
#     return json.dumps(resp['Items'])


# # #Send photo from S3 to Rekognition and gets lables 
# # #/<bucket>/<image> #not so relevent
# @application.route('/analyze', methods=['GET'])
# def analyze(bucket='savepics', image='spider.jpg'): #we need to change the name of the image to somthing constant and to make sure to set this name on the React code as the name of the image when user add an image
#     return detect_labels(bucket, image)
    
    
# def detect_labels(bucket, key, max_labels=10, min_confidence=50, region="us-east-1"):
    
#     rekognition = boto3.client("rekognition", region)
#     s3 = boto3.resource('s3', region_name = 'us-east-1')
    
#     image = s3.Object(bucket, key) # Get an Image from S3
    
#     img_data = image.get()['Body'].read() # Read the image

#     response = rekognition.detect_labels(
#         Image={
#             'Bytes': img_data
#         },
#         MaxLabels=max_labels,
# 		MinConfidence=min_confidence,
#     )
    
#     return json.dumps(response['Labels'])



# # #Get the animal data from NinjaAPI
# @application.route('/animal_details', methods=['GET'])    
# def get_animal_data(animal_name='cheetah'):
#     name = animal_name
#     api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(name)
#     response = requests.get(api_url, headers={'X-Api-Key': 'pxwXJfjdW9672Yt5D3kPQQ==cEwkHnvnB0jFUzj6'}) 
#     if response.status_code == requests.codes.ok:
#         response_json = json.loads(response.text)
#         return json.dumps(response_json, indent=4)  # Convert the Python object to formatted JSON string
#     else:
#         #print("Error:", response.status_code, response.text)
#         response_json = json.loads(response.text)
#         return json.dumps(response.text)


# @application.route('/test', methods=['GET']) 
# def compare_lable_to_table():
#     # Fetch labels from the first source
#     response1 = requests.get('http://ec2-34-230-71-62.compute-1.amazonaws.com/analyze')
#     Labels = response1.json()
#     # Fetch animalTable names from the second source
#     response2 = requests.get('http://ec2-34-230-71-62.compute-1.amazonaws.com/get_animalTable')
#     Animal_Table = response2.json()
#     # Compare each name    
#     animal_name=""
#     for label in Labels:
#         for animal in Animal_Table:
#             if label["Name"] == animal["animalName"]:
#                 animal_name = label["Name"]
#                 animal_data=get_animal_data(animal_name)
                
#                 print(json.loads(animal_data)[0])
#                 break # Exit inner loop if a match is found
#         if animal_name !="":
#             break # Exit external loop if a match is found



if __name__ == '__main__':
    flaskrun(application)
