load_dotenv('api_key.env')
api_key = os.getenv('API_KEY')


from imports import *
class ClaudeAgent:
    def __init__(self, prompt,message, api_key):
        self.prompt = prompt
        self.message = message
        self.api_key = api_key
        self.headers = {
        'x-api-key': self.api_key,
        'anthropic-version' : '2023-06-01',
        'Content-Type' :'application/json'
        }
    
    def send_request(self):

        messages = [
                {'role': 'user', 'content':self.message}

            ]

        data = {
            "model": "claude-3-5-sonnet-20240620",
            "max_tokens": 3000,
            "temperature": 0,
            "messages": messages,
            'system' : self.prompt,
            }
        
        response = requests.post("https://api.anthropic.com/v1/messages", headers=self.headers, json=data)
    
        if response.status_code == 200:
            response_json = response.json()
            #print("Response JSON:", response_json)  # For debugging
            if 'content' in response_json and response_json['content']:
                
                if 'text' in response_json['content'][0] and response_json['content'][0]['text']:
                    return response_json['content'][0]['text']
                else:
                    return None
            else:
                return None
        else:
            return f"Error: Request failed with status code {response.status_code}. Response: {response.text}"
        