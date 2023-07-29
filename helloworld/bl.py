# This is the Business Logic Layer, where all logic happens
import json
import requests
from dal import post_to_bucket, get_image , detect_labels, get_animal_data, get_animal_ids, add_new_animal_values
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
    labels = detect_labels(img_data, region, max_labels, min_confidence)['Labels']
    # get items of dynamoDB table
    my_dyno = dyno(region, table_name)
    # compare labels to items
    animal_name=""
    for label in labels:
        for animal in my_dyno:
            if label[label_name_key] == animal[animal_name_key]:
                animal_name = label[label_name_key]
                # get ninja_api response
                response=get_animal_data(animal_name)
                #print(json.loads(response)[0])
                
                if response.status_code == requests.codes.ok:
                    animal_details = json.loads(response.text)
                else:
                    #print("Error:", response.status_code, response.text)
                    animal_details = json.loads(response.text)
                
                break # Exit inner loop if a match is found
        if animal_name !="":
            break # Exit external loop if a match is found
    if animal_name =="":
        return (json.loads(unmatch_to_db_message))
    return animal_details
    
    
def add_new_animal(region, table_name, field_name, animal_name):
    get_animal_ids_function_response = get_animal_ids(region, table_name, field_name)
    if len(get_animal_ids_function_response)==2:
        response= get_animal_ids_function_response[0]
        attribute_to_maximize = field_name
        table = get_animal_ids_function_response[1]
        items = response['Items']
        max_animal_id = None
        
        # Extract and find the maximum value
        for item in items:
            animal_id = int(item[attribute_to_maximize])  # Access the attribute value directly
            if max_animal_id is None or animal_id > max_animal_id:
                max_animal_id = animal_id
        max_animal_id=max_animal_id+1
        max_animal_id_str = str(max_animal_id)
        add_new_animal_values_response = add_new_animal_values(max_animal_id_str, animal_name, table)
        if (add_new_animal_values_response==True):
            return (True)
        else:
            return(add_new_animal_values_response)
    else:
        return(get_animal_ids_function_response)