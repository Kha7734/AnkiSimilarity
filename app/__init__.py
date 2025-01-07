from flask import Flask, jsonify
from app.databases.db import get_db, get_test_db, close_db
import json
from bson import ObjectId

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super().default(obj)

def create_app(env='development'):
    app = Flask(__name__)

    # Load configuration from config.json
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Update the configuration with values from the JSON file
    app.config.update(config)

    # Use a different database for testing
    if env == 'testing':
        app.db = get_test_db()  # Use the test database
    else:
        app.db = get_db()  # Use the main database

    app.json_encoder = CustomJSONEncoder  # Set the custom encoder

    # Register blueprints (routes)
    from app.routes.user_routes import user_bp
    from app.routes.card_collection_routes import vocab_bp  # Import vocabulary card routes
    from app.routes.user_progress_routes import progress_bp
    from app.routes.dataset_collection_routes import dataset_bp
    from app.routes.user_setting_routes import settings_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(vocab_bp)  # Register the vocabulary card blueprint
    app.register_blueprint(progress_bp)
    app.register_blueprint(dataset_bp)
    app.register_blueprint(settings_bp)

    # Ensure the database connection is closed when the app shuts down
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    return app