# This is the Business Logic Layer, where all logic happens
import json
import requests
from dal import post_to_bucket, get_image , detect_labels, get_animal_data
from dal import get_dynamo_result as dyno


max_labels=10 
min_confidence=50
unmatch_to_db_message = "There isn't a match to an animal in our data-base."
animal_name_key = "animalName"
label_name_key = "Name"

def handle_request_data(file, bucket, region):
     # Set the desired object key or file name for the image in the S3 bucket
    object_name = 'images/' + file.filename
    return(post_to_bucket(file, object_name, bucket, region))
    

    
# This function get the image, recognize the labels, compare with the animals table and get the animal details    
def animal_details(bucket, image_name, region, table_name):
    key= 'images/'+image_name
    # get the image from S3 bucket
    image = get_image(bucket, key, region)
    img_data = image.get()['Body'].read() # Read the image
    # get lables of the image from Recognition
    labels = detect_labels(img_data, region, max_labels, min_confidence)
    return labels['Labels']
        # # get items of dynamoDB table
        # my_dyno = dyno(region, table_name).json()
        # my_dyno = my_dyno.json()
        
        # # compare labels to items
        # animal_name=""
        # for label in labels:
        #     for animal in my_dyno:
        #         if label[label_name_key] == animal[animal_name_key]:
        #             animal_name = label[label_name_key]
        #             # get ninja_api response
        #             response=get_animal_data(animal_name)
        #             #print(json.loads(response)[0])
                    
        #             if response.status_code == requests.codes.ok:
        #                 response_json = json.loads(response.text)
        #                 animal_details = json.dumps(response_json, indent=4)  # Convert the Python object to formatted JSON string
        #             else:
        #                 #print("Error:", response.status_code, response.text)
        #                 response_json = json.loads(response.text)
        #                 animal_details =  json.dumps(response_json, indent=4)
                    
        #             break # Exit inner loop if a match is found
        #     if animal_name !="":
        #         break # Exit external loop if a match is found
        # if animal_name =="":
        #     return (unmatch_to_db_message)
        # return animal_details
        
    
    