# This is the Business Logic Layer, where all logic happens
import simplejson as json
from helloworld.dal import post_to_bucket, get_image , detect_labels, get_animal_data
from helloworld.dal import get_dynamo_result as dyno


max_labels=10 
min_confidence=50


def get_request_header(request_data):
    # convert the json to dictionary
    data_dict = json.loads(request_data)
    image = data_dict.get('image')
    
    # dal.py function that upload the image to the S3 bucket
    post_to_bucket(image)

    
# This function get the image, recognize the labels, compare with the animals table and get the animal details    
def animal_details(bucket, image_name, region, table_name):
    # get the image from S3 bucket
    image = get_image(bucket, image_name, region)
    img_data = image.get()['Body'].read() # Read the image
    # get lables of the image from Recognition
    labels = detect_labels(img_data, region, max_labels, min_confidence)
    labels = labels.json()
    # get items of dynamoDB table
    my_dyno = dyno(region, table_name).json()
    my_dyno = my_dyno.json()
    
    # compare labels to items
    animal_name=""
    for label in labels:
        for animal in my_dyno:
            if label["Name"] == animal["animalName"]:
                animal_name = label["Name"]
                # get animal data
                animal_details=get_animal_data(animal_name)
                #print(json.loads(animal_details)[0])
                break # Exit inner loop if a match is found
        if animal_name !="":
            break # Exit external loop if a match is found
    return animal_details
    
    
    