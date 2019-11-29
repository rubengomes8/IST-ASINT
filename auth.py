import requests

client_id = '1695915081465934'
redirect_uri = 'http://127.0.0.1:3998/redirect'
client_secret = 'WVVcjUVINVFwgXDyG1VOzLNN5Q4AU6tHt8/6LKFsswA+Tj00Yc9j1ryu5AKyrBDv+no+UbIUIB3INUWzw1w9Mg=='
access_token = ''
refresh_token = ''
expires_in = ''

# https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=1695915081465934&redirect_uri=http://127.0.0.1:3998/redirect
def request_user_permission():
    global client_id
    global redirect_uri
    url = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=' + client_id + '&redirect_uri=' + redirect_uri
    r = requests.get(url=url)

def request_access_token(code):
    global client_id
    global redirect_uri
    global client_secret
    global access_token
    global refresh_token
    global expires_in
    url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'
    r = requests.post(url, params={'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': redirect_uri, 'code': code, 'grant_type': 'authorization_code'})
    data = r.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_in = data['expires_in']
    return data