import requests

class Message(dict):
    role=""
    content=""
    def __init__ (self, role,content):
        self.role = role
        self.content = content
        dict.__init__(self, role=role,content=content) 


class ChatGPTAPIClient:
    headers = {
        'Content-Type': 'application/json',
        }
    url = 'https://api.openai.com/v1/chat/completions'
    messages = [Message("system","Du er i samtale med en liten jente, og spiller skuespill der du er en prinsesse. Du skal ikke, med mindre du blir spurt, røpe at du er en språkmodell."),        
    Message("system","Du vil prøve å underholde og utvikle, og dele gode råd."),
        ]

    data = {
        'messages': messages,
        'temperature': 0.7,
        'model': 'gpt-3.5-turbo'
    }
    def __init__(self,api_key):
        self.headers['Authorization'] = f'Bearer {api_key}' 

    def AddToDialog(self,message):
        self.messages.append(message)
    
    def chat(self,prompt):
        message = Message("user",prompt)
        self.AddToDialog(message)
        response = requests.post(self.url, headers=self.headers, json=self.data)
        response_text = response.json()['choices'][0]['message']['content']
        self.AddToDialog(Message("assistant",response_text))
        return response_text
    

