# app/__init__.py

from flask import Flask
from app.databases.db import db
import json

def create_app():
    app = Flask(__name__)

    # Load configuration from config.json
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Update the configuration with values from the JSON file
    app.config.update(config)

    app.db = db # Add database connection to app

    # Register blueprints (routes)
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    return app
