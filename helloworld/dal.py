# this is the Data Access Layer, where all crud  operations happens
import boto3
import json
import requests


db_resource = 'dynamodb'
s3_resource = 's3'
rekognitoin_resource = 'rekognition'
api_ninja_url = 'https://api.api-ninjas.com/v1/animals?name={}'
api_ninja_key = 'pxwXJfjdW9672Yt5D3kPQQ==cEwkHnvnB0jFUzj6'
api_ninja_header_name = 'X-Api-Key'


#This function get the items from dynamoDB table
def get_dynamo_result(region, table_name):
    dynamodb = boto3.resource(db_resource, region_name=region)
    table = dynamodb.Table(table_name)
    resp = table.scan()
    #print(str(resp))
    
    return json.dumps(resp['Items'])
    

# This function post the uploaded image to the S3 bucket
def post_to_bucket(file, object_name, bucket, region):
    s3 = boto3.client(s3_resource, region)
    try:
        # Upload the file to S3 bucket
        s3.upload_fileobj(file, bucket, object_name)
        return(True)
    except Exception as e:
        return(False)
    
# This function get the image from S3 bucket    
def get_image(bucket, key, region):
    # s3 = boto3.resource(s3_resource, region)
    # image = s3.Object(bucket, key) # Get an Image from S3
    # return image
    try:
        s3 = boto3.resource(s3_resource, region)
        image = s3.Object(bucket, key) # Get an Image from S3
        return(True)
    except Exception as e:
        return(False)

# This function detect the labels of an image with Recognition service
def detect_labels(img_data, region, max_labels, min_confidence):
    rekognition = boto3.client(rekognitoin_resource, region)
    labels = rekognition.detect_labels(
        Image={
            'Bytes': img_data
        },
        MaxLabels=max_labels,
		MinConfidence=min_confidence,
    )
    return labels


def get_animal_data(animal_name):
    response = requests.get(api_ninja_url.format(animal_name), headers={api_ninja_header_name : api_ninja_key })
    return response