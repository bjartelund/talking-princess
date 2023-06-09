import json
import base64
import requests

class TTSApiClient:
    url = 'https://texttospeech.googleapis.com/v1/text:synthesize'
    params = {
        'voice': {
            'languageCode': 'nb-NO',
            'name': 'nb-NO-Wavenet-A',
        },
        'audioConfig': {
            'audioEncoding': 'LINEAR16',
            'pitch': 5.0,
        },
    }
    def __init__(self,API_KEY):
        self.url = self.url+"?key="+API_KEY
    def Synthesize(self,text):
        self.params['input'] = {'text': text}
        # Send a POST request to the Google Cloud Text-to-Speech API with the parameters
        response = requests.post(self.url, json=self.params)
        data = json.loads(response.content)
        # Extract the audio content from the response
        try:
            audio_content = base64.b64decode(data['audioContent'])
        except:
            print(data)

        # Save the MP3 file to disk
        with open('output.wav', 'wb') as f:
            f.write(audio_content)
