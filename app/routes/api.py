# routes/api.py

from flask import Flask
from app.routes.user_routes import user_bp  # Import user routes

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
