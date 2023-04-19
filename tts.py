from google.cloud import texttospeech, storage

# Initialize Google TTS Client
tts_client = texttospeech.TextToSpeechClient()

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket_name = 'finter'
bucket = storage_client.bucket(bucket_name)


# Call to Google TTS API
def synthesize_text(text, is_french):
    # Set the voice parameters
    input_text = texttospeech.SynthesisInput(text=text)
    language_code = "fr-FR" if is_french else "en-EN"
    voice_name = "fr-FR-Neural2-A" if is_french else "en-GB-Standard-B"
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    # Set the audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    # Call the synthesize speech method of the client
    response = tts_client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    # Set the parameters for file upload to the cloud
    filename = "french.mp3" if is_french else "english.mp3"
    blob = bucket.blob(filename)
    # Cloud upload
    blob.upload_from_string(response.audio_content)
