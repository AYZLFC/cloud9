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
from bl import add_new_animal as add_new_animal_bl




application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}})

#curl -i -X POST -d'{"animal_name":"Dog"}' -H "Content-Type: application/json" http://localhost:8000/add_new_animal
#This route for adding new animals to the DynmoDB table
@application.route('/add_new_animal', methods=['POST'])
def add_new_animal():
    # get post data  
    data = request.data
    # convert the json to dictionary
    data_dict = json.loads(data)
    # retreive the parameters
    animal_name = data_dict.get('animal_name','default')
    
    # Deliver the request content to bl.py
    response_add_animal = add_new_animal_bl(region="us-east-1", table_name="animalTable", field_name="animalId", animal_name=animal_name)
    #Check that an error didn't occured
    if (response_add_animal==True):
        return Response('New animal was added successfully.', mimetype='application/json', status=200)
    else:
        return Response('Error in adding the new animal. Please contact support', mimetype='application/json', status=200)
    
 
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
@application.route('/animal_details/<string:image_name>', methods=['GET'])
def get_animal_details(image_name):
    #Sort image name because of retreive from url
    sorted_image_name = image_name.replace('%20', ' ')
    # Deliver the request content to bl.py
    details=animal_details(bucket="savepics", image_name=sorted_image_name , region="us-east-1", table_name="animalTable")
    
    return Response(json.dumps(details), mimetype='application/json', status=200)


if __name__ == '__main__':
    flaskrun(application)
