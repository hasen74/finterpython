from google.cloud import vision

client = vision.ImageAnnotatorClient()


# Call to Google Cloud Vision API
def detect_objects(uri):
    # # Open file in binary mode to be read by Cloud Vision
    # with open(image_path, 'rb') as image_file:
    #     content = image_file.read()
    #     image = vision.Image(content=content)

    # Set image from GCS uri
    image = vision.Image()
    image.source.image_uri = uri

    # Call to the object_localization method of the client
    objects = client.object_localization(
        image=image).localized_object_annotations
    # Counts number of people in response
    person_count = sum(1 for obj in objects if obj.name == 'Person')
    print('Number of people found: {}'.format(person_count))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
