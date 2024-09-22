from datetime import datetime, timedelta

import google.oauth2.credentials
import googleapiclient.discovery


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

# Class to handle Google Calendar API interactions
class GoogleCalendar:
    def __init__(self, credentials):
        self.credentials = credentials
        self.service = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=self.credentials)

    def get_calendar_events(self):
        events_result = self.service.events().list(
            calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime').execute()

        events = events_result.get('items', [])
        return events
    
    def get_events_for_upcoming_week(self, calendar_id='primary'):
        # Get the current date and time
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # Get the date and time for one week from now
        one_week_later = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'

        # Fetch events for the upcoming week
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            timeMax=one_week_later,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return events

    def get_calendar_summary(self, calendar_id='primary'):
        calendar_list_entry = self.service.calendarList().get(calendarId=calendar_id).execute()
        return calendar_list_entry['summary']

    def add_event(self, start_time, name, description, calendar_id='primary'):
        # Format the start_time properly for Google Calendar API (YYYY-MM-DDTHH:MM:SSZ)
        start_time = datetime.fromisoformat(start_time).replace(microsecond=0).isoformat() + 'Z'
        
        # Event end time, assuming 1 hour duration
        end_time = (datetime.fromisoformat(start_time[:-1]) + timedelta(hours=1)).replace(microsecond=0).isoformat() + 'Z'

        # Event details
        event = {
            'summary': name,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
        }
        # Insert the event into the calendar
        event_result = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        return event_result

# Helper function to store credentials in a dict (for session storage)
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