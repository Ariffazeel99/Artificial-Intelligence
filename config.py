scope=""
client_id=""
client_secret=""


grant_type=""
access_token_request_data={'scope': scope, 'client_id': client_id, 'grant_type': grant_type, 'client_secret': client_secret}
access_token_url=""
access_token_response = requests.post(access_token_url, data=access_token_request_data).json()
access_token=access_token_response['access_token']

query = 
