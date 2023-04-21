from flask import Flask, make_response, render_template, request, jsonify
from google.cloud import storage
from translate import translate_english
from tts import synthesize_text
from cloudvision import detect_objects
import json

app = Flask(__name__)

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket_name = 'finter'
bucket = storage_client.bucket(bucket_name)
image1_blob = bucket.blob('images/deux.jpeg')
image2_blob = bucket.blob('images/sept.jpeg')
image3_blob = bucket.blob('images/neuf.jpg')
image4_blob = bucket.blob('images/quatre.jpg')
image5_blob = bucket.blob('images/trois.jpg')


# Route serving main page
@app.route('/')
def studio1():
    image1_url = image1_blob.public_url
    # Get config.json from GCS
    blob = bucket.blob('config.json')
    json_data = blob.download_as_string()

    # parse the JSON data and extracts number
    config = json.loads(json_data)
    max_capacity = int(config["number"])
    return render_template(
        'studio1.html', image1_url=image1_url, max_capacity=max_capacity)


@app.route('/studio2/')
def studio2():
    image2_url = image2_blob.public_url
    # Get config.json from GCS
    blob = bucket.blob('config.json')
    json_data = blob.download_as_string()

    # parse the JSON data and extracts number
    config = json.loads(json_data)
    max_capacity = int(config["number"])
    return render_template(
        'studio2.html', image2_url=image2_url, max_capacity=max_capacity)


@app.route('/studio3/')
def studio3():
    image3_url = image3_blob.public_url
    # Get config.json from GCS
    blob = bucket.blob('config.json')
    json_data = blob.download_as_string()

    # parse the JSON data and extracts number
    config = json.loads(json_data)
    max_capacity = int(config["number"])
    return render_template(
        'studio3.html', image3_url=image3_url, max_capacity=max_capacity)


@app.route('/studio4/')
def studio4():
    image4_url = image4_blob.public_url
    # Get config.json from GCS
    blob = bucket.blob('config.json')
    json_data = blob.download_as_string()

    # parse the JSON data and extracts number
    config = json.loads(json_data)
    max_capacity = int(config["number"])
    return render_template(
        'studio4.html', image4_url=image4_url, max_capacity=max_capacity)


@app.route('/studio5/')
def studio5():
    image5_url = image5_blob.public_url
    # Get config.json from GCS
    blob = bucket.blob('config.json')
    json_data = blob.download_as_string()

    # parse the JSON data and extracts number
    config = json.loads(json_data)
    max_capacity = int(config["number"])
    return render_template(
        'studio5.html', image5_url=image5_url, max_capacity=max_capacity)


# Compare the number of people in a room with
# the number in config.json
@app.route('/people')
def comparePeople():
    studio_image = request.args.get('studio_image')
    # Get config.json from GCS
    blob = bucket.blob('config.json')
    json_data = blob.download_as_string()

    # parse the JSON data and extracts config number
    config = json.loads(json_data)
    people_config = int(config["number"])

    # Call computer vision to check
    # the number of people in the studio
    people_studio = detect_objects(studio_image)

    # Compares both numbers
    if people_studio > people_config:
        return jsonify({'room': "full"})
    else:
        return jsonify({'room': "notfull"})


# Fetch sound annoucements from GSC and return them
@app.route('/sound')
def get_sound():
    # Get the language from query parameter or use french as default
    language = request.args.get('language', 'french')

    if language == 'english':
        blob = bucket.blob('english.mp3')
    else:
        blob = bucket.blob('french.mp3')

    # Get the audio data as bytes
    audio_data = blob.download_as_bytes()

    # Create a Flask response with the audio data
    response = make_response(audio_data)
    response.headers.set('Content-Type', 'audio/mpeg')
    print(response)
    return response


@app.route('/form')
def form():
    return render_template('form.html')


# Route handling the form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get data from form
    number = request.form['number']
    french = request.form['french']

    # Call to the translation function
    english = translate_english(french)

    # Create dictionary object with data
    data = {'number': number, 'french': french, 'english': english}

    # Write data to JSON file in Google Cloud Storage
    filename = 'config.json'
    blob = bucket.blob(filename)
    blob.upload_from_string(json.dumps(data))

    # Generate audio files
    synthesize_text(french, True)
    synthesize_text(english, False)

    # Return success message
    return jsonify({"message": "Fichier de configuration mis à jour"})


if __name__ == "__main__":
    app.run(debug=True)
