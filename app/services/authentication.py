import os
import google.oauth2.credentials
import google_auth_oauthlib.flow

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']

# Class to handle OAuth2 authentication
class GoogleOAuth:
    def __init__(self):
        self.flow = None

    def create_flow(self, redirect_uri):
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES)
        self.flow.redirect_uri = redirect_uri

    def get_authorization_url(self):
        if not self.flow:
            raise Exception("OAuth flow not initialized.")
        authorization_url, state = self.flow.authorization_url(
            access_type='offline', include_granted_scopes='true', prompt='consent')
        return authorization_url, state

    def fetch_token(self, authorization_response, state):
        if not self.flow:
            self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
        self.flow.fetch_token(authorization_response=authorization_response)
        return self.flow.credentials

#  Helper function to store credentials in a dict (for session storage)
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

# Helper function to load credentials from a dict
def dict_to_credentials(session_data):
    return google.oauth2.credentials.Credentials(
        token=session_data['token'],
        refresh_token=session_data.get('refresh_token'),
        token_uri=session_data['token_uri'],
        client_id=session_data['client_id'],
        client_secret=session_data['client_secret'],
        scopes=session_data['scopes']
    )