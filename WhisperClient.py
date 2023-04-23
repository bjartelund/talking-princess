import requests

class WhisperAPIClient:
    headers = dict()
    url = "https://api.openai.com/v1/audio/transcriptions"
    data = {"model": "whisper-1"}

    def __init__(self,token):
        self.headers["Authorization"] = f"Bearer {token}"
    def Transcribe(self,filename):
        files = {"file": (filename,open(filename, "rb"),"audio/wav")}
        response = requests.post(self.url, headers=self.headers, data=self.data, files=files)
        print(response.status_code)
        return response.json()["text"]






