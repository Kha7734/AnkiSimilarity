import json
import os
import logging
from flask import Flask
from flask_cors import CORS
from bson import ObjectId
from app.databases.db import get_db, get_test_db, close_db

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super().default(obj)

def create_app(env='development'):
    app = Flask(__name__)
    # CORS(app, supports_credentials=True,  origins='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    cors = CORS()
    app_v1_cors = {
        "origins": ["http://localhost:3000", "http://localhost:5000"],
    }
    cors.init_app(app, resources={r"/*": app_v1_cors}, supports_credentials=True)

    # Configure logging
    # logging.basicConfig(level=logging.DEBUG if env == 'development' else logging.INFO)
    app.logger.info(f"Starting app in '{env}' environment.")

    # Load configuration from config.json
    config_path = 'config.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file '{config_path}'.")

    # Load environment-specific configuration
    env_config_path = f'config_{env}.json'
    if os.path.exists(env_config_path):
        with open(env_config_path, 'r') as env_config_file:
            env_config = json.load(env_config_file)
        config.update(env_config)

    app.config.update(config)

    # Set up database connection
    if env == 'testing':
        app.db = get_test_db()  # Use the test database
    else:
        app.db = get_db()  # Use the main database

    # Test database connection
    try:
        app.db.command('ping')  # Test MongoDB connection
        app.logger.info("Database connection successful.")
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")
        raise

    # Set custom JSON encoder
    app.json_encoder = CustomJSONEncoder

    # Register blueprints
    blueprints = [
        ('app.routes.user_routes', 'user_bp'),
        ('app.routes.card_collection_routes', 'vocab_bp'),
        ('app.routes.user_progress_routes', 'progress_bp'),
        ('app.routes.dataset_collection_routes', 'dataset_bp'),
        ('app.routes.user_setting_routes', 'settings_bp'),
    ]

    for module_name, blueprint_name in blueprints:
        try:
            module = __import__(module_name, fromlist=[blueprint_name])
            blueprint = getattr(module, blueprint_name)
            app.register_blueprint(blueprint)
            app.logger.info(f"Registered blueprint: {blueprint_name}")
        except ImportError as e:
            app.logger.error(f"Failed to import blueprint '{blueprint_name}': {e}")
        except AttributeError as e:
            app.logger.error(f"Blueprint '{blueprint_name}' not found in module '{module_name}': {e}")

    # Ensure the database connection is closed when the app shuts down
    # @app.teardown_appcontext
    # def teardown_db(exception):
    #     close_db()

    return app