from app.services.agent import URLProcessorAgent
from app.services.calendar import GoogleCalendar
from app.services.authentication import GoogleOAuth

agent = URLProcessorAgent(model_name="claude-3-5-sonnet-20240620", temperature=0)
