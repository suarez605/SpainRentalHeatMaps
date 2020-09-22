import requests
import base64


IDEALISTA_BASE_URL = 'https://api.idealista.com/oauth/token'

class Auth:
    def __init__(self, apikey, secret):
        self.apikey = apikey
        self.secret = secret
        pass

    def auth(self):

        data = self.apikey + ':' + self.secret
        data_bytes = data.encode('ascii')
        base64_key = base64.urlsafe_b64encode(data_bytes)
        base64_key = base64_key.decode('ascii')
        headers = {
            'Authorization' : 'Basic ' + str(base64_key),
            'Content-Type' : 'application/x-www-form-urlencoded'
        }
        payload = {
            'grant_type': 'client_credentials',
            'scope' : 'read'
        }
        r = requests.post(IDEALISTA_BASE_URL, headers = headers, params = payload)
        
        if r.status_code != 200:
            return 'Error'

        return r.json()
        
if __name__ == "__main__":
    a = Auth('', '')
    a.auth()
    pass
