from google.cloud import vision
import requests

client = vision.ImageAnnotatorClient()


# Call to Google Cloud Vision API
def detect_objects(image_url):
    # Set image from local file
    # with open(image_path, 'rb') as image_file:
    #     content = image_file.read()
    #     image = vision.Image(content=content)

    # # Set image from GCS uri
    # image = vision.Image()
    # image.source.image_uri = uri

    # Set image from URL
    response = requests.get(image_url)
    content = response.content

    # Set image content from binary data
    image = vision.Image(content=content)

    # Call to the object_localization method of the client
    objects = client.object_localization(
        image=image).localized_object_annotations
    # Return number of people in response
    person_count = sum(1 for obj in objects if obj.name == 'Person')
    return person_count
    # for object_ in objects:
    #     print('\n{} (confidence: {})'.format(object_.name, object_.score))
