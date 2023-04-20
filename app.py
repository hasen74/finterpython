from flask import Flask, render_template, request, jsonify
from google.cloud import storage
from translate import translate_english
from tts import synthesize_text
from cloudvision import detect_objects
import json
import time

app = Flask(__name__)

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket_name = 'finter'
bucket = storage_client.bucket(bucket_name)


# Route serving main page
@app.route('/')
def studio1():
    image1_blob = bucket.blob('images/deux.jpeg')
    image1_url = image1_blob.public_url
    return render_template('studio1.html', image1_url=image1_url)


@app.route('/studio2/')
def studio2():
    return render_template('studio1.html')


@app.route('/studio3/')
def studio3():
    return render_template('studio1.html')


@app.route('/studio4/')
def studio4():
    return render_template('studio1.html')


@app.route('/studio5/')
def studio5():
    return render_template('studio1.html')


start_time = None


# Route keeping track of time when we change page
@app.route('/time')
def get_time():
    global start_time
    # If time never was initialized, initialize it from now
    if start_time is None:
        start_time = time.time()
    # Calculates elapsed time between when the variable
    # was first initialized and the new call
    elapsed_time = time.time() - start_time
    # Substracts that time from 60 to determine
    # the remaining time
    remaining_time = 10 - int(elapsed_time)
    if remaining_time < 0:
        remaining_time = 0
        start_time = time.time()
    # Returns that number to the caller
    return jsonify({'time': remaining_time})


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

    detect_objects('gs://finter/images/neuf.jpg')

    # Return success message
    return 'Fichier de configuration mis à jour !'


if __name__ == '__main__':
    app.run(debug=True, port=5012)
