# routes/api.py

from flask import Flask
from app.routes.user_routes import user_bp  # Import user routes
from app.routes.card_collection_routes import vocab_bp  # Import vocabulary card routes

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(vocab_bp)  # Register the vocabulary card blueprint

if __name__ == '__main__':
    app.run(debug=True)

