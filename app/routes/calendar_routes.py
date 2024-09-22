
from flask import Blueprint, session, redirect, url_for, request, jsonify
from datetime import datetime, timedelta

from app.services.calendar import GoogleCalendar
from app.services.authentication import GoogleOAuth, credentials_to_dict, dict_to_credentials

bp = Blueprint('calendar', __name__, url_prefix='/calendar')


google_oauth = GoogleOAuth()

# Route to start OAuth flow
@bp.route('/authorize')
def authorize():
    # Initialize the OAuth flow and get the authorization URL
    google_oauth.create_flow(redirect_uri=url_for('calendar.callback', _external=True))
    authorization_url, state = google_oauth.get_authorization_url()
    
    # Store the state in the session to verify the response later
    session['state'] = state
    
    # Redirect the user to the Google OAuth 2.0 authorization URL
    return redirect(authorization_url)

# Callback route for OAuth 2.0
@bp.route('/callback')
def callback():
    # Retrieve the state stored in the session and handle the OAuth callback
    state = session.get('state')
    
    # Fetch the authorization response URL (from query parameters)
    authorization_response = request.url
    credentials = google_oauth.fetch_token(authorization_response=authorization_response, state=state)
    
    # Store the credentials in the session
    session['credentials'] = credentials_to_dict(credentials)
    
    # Redirect to the calendar events route
    return redirect(url_for('calendar.calendar_events'))


# Route to fetch calendar events
@bp.route('/list')
def calendar_events():
    # Check if credentials are stored in the session
    if 'credentials' not in session:
        return redirect(url_for('calendar.authorize'))
    
    # Load credentials from the session and create a GoogleCalendar instance
    credentials = dict_to_credentials(session['credentials'])
    google_calendar = GoogleCalendar(credentials)
    
    # Fetch upcoming week's calendar events
    events = google_calendar.get_events_for_upcoming_week()
    print("Events:", events)
    
    # Display the events
    if not events:
        return 'No upcoming events found.'
    
    output = 'Upcoming events for the next week:<br>'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        output += f"{start}: {event['summary']}<br>"
    
    return output

@bp.route('/add_event')
def add_calendar_event():
    # Check if credentials are stored in the session
    if 'credentials' not in session:
        return redirect(url_for('calendar.authorize'))
    
    # Load credentials from the session and create a GoogleCalendar instance
    credentials = dict_to_credentials(session['credentials'])
    google_calendar = GoogleCalendar(credentials)

    # Define dummy event data (you can replace this with actual form data or input)
    event_time = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0).isoformat()  # Event scheduled for tomorrow
    event_name = 'Sample Event'
    event_description = 'This is a dummy description for the event.'

    # Add the event to the calendar
    new_event = google_calendar.add_event(event_time, event_name, event_description)
    
    return f"Event created: {new_event.get('htmlLink')}"