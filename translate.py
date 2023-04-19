from google.cloud import translate_v2 as translate


# Call to Google translate API
def translate_english(french):
    client = translate.Client()
    response = client.translate(french, target_language="en")
    return response['translatedText']
