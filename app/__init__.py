# app/__init__.py

from flask import Flask, jsonify
from app.databases.db import db
import json
from bson import ObjectId

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super().default(obj)

def create_app():
    app = Flask(__name__)

    # Load configuration from config.json
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Update the configuration with values from the JSON file
    app.config.update(config)
    app.json_encoder = CustomJSONEncoder  # Set the custom encoder

    app.db = db  # Add database connection to app

    # Register blueprints (routes)
    from app.routes.user_routes import user_bp
    from app.routes.card_collection_routes import vocab_bp  # Import vocabulary card routes
    app.register_blueprint(user_bp)
    app.register_blueprint(vocab_bp)  # Register the vocabulary card blueprint

    return app
