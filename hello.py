from flask import Flask, render_template, request
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


# Route serving back office main page
@app.route('/')
def form():
    return render_template('index.html')


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

    detect_objects('gs://finter/images/quatre.jpg')

    # Return success message
    return 'Fichier de configuration mis à jour !'


if __name__ == '__main__':
    app.run(debug=True, port=5009)
