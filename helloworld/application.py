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



if __name__ == '__main__':
    flaskrun(application)
