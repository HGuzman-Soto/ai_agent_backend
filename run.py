import os
from flask import Flask, request
from app.routes import bot_routes, calendar_routes, extension_routes
from app.services import (URLProcessorAgent,
                            GoogleCalendar,
                            GoogleOAuth)
from flask_cors import CORS



os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

allowed_origins = [
    "http://localhost:3000",
]

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(bot_routes.bp)
app.register_blueprint(calendar_routes.bp)
app.register_blueprint(extension_routes.bp)


# CORS(app, resources={r"/*": {
#         "origins": allowed_origins,
#         "supports_credentials": True}}, supports_credentials=True)
CORS(app)

app.run(debug=True, port=8080, host="0.0.0.0")