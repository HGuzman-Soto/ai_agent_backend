import os
import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from flask_cors import CORS

# For development, disable the need for HTTPS
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = flask.Flask(__name__)
CORS(app)  # Enable CORS if you need to access it from the frontend
app.secret_key = 'your_secret_key'

# Path to your client_secrets.json file
CLIENT_SECRETS_FILE = 'client_secrets.json'

# Google Docs API scope
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
API_SERVICE_NAME = 'docs'
API_VERSION = 'v1'

# The ID of the document you want to retrieve
DOCUMENT_ID = '1SHOvynRfXMhtH6brUKego88Zsie225f--xidSSeM5Rs'  # Replace with your Google Doc ID

# Index route to start the app
@app.route('/')
def index():
    return 'Welcome to Google Docs API Flask App'

# Route to start OAuth flow for Google Docs
@app.route('/authorize')
def authorize():
    # Create OAuth 2.0 flow to handle user login and consent
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = flask.url_for('callback', _external=True)
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    
    # Store the state in session to verify it later
    flask.session['state'] = state
    
    return flask.redirect(authorization_url)

# OAuth callback route
@app.route('/callback')
def callback():
    # Retrieve the state and continue the OAuth flow
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    
    flow.redirect_uri = flask.url_for('callback', _external=True)
    
    # Get the authorization response from the query parameters
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    # Store credentials in session for later use
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    
    return flask.redirect(flask.url_for('get_doc_title'))

# Route to fetch and display the title of the document
@app.route('/docs')
def get_doc_title():
    # Check if user credentials are available
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('authorize'))

    # Load credentials from session
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    # Build the Google Docs API service object
    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Fetch the document from the Google Docs API
    try:
        document = service.documents().get(documentId=DOCUMENT_ID).execute()
        title = document.get('title')
        return f"The title of the document is: {title}"
    except googleapiclient.errors.HttpError as error:
        return f"An error occurred: {error}"

# Helper function to store credentials in session
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

if __name__ == '__main__':
    # Run the Flask app on localhost
    app.run('localhost', 5000, debug=True)
