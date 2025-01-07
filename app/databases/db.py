import json
from pymongo import MongoClient
import constant

# Load config.json and update the password
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Replace <db_password> with the actual password
config['mongodb']['uri'] = config['mongodb']['uri'].replace('<db_password>', constant.MONGODB_PASSWORD)
config['mongodb']['test_uri'] = config['mongodb']['test_uri'].replace('<db_password>', constant.MONGODB_PASSWORD)

# Global variables for client and database
_client = None
_db = None

def get_db():
    """Get the database connection."""
    global _client, _db
    if _db is None:
        _client = MongoClient(config['mongodb']['uri'])
        _db = _client[config['mongodb']['database']]
    return _db

def get_test_db():
    """Get the test database connection."""
    global _client, _db
    if _db is None:
        _client = MongoClient(config['mongodb']['test_uri'])
        _db = _client[config['mongodb']['test_database']]
    return _db

def close_db():
    """Close the database connection."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None

# Export the database connection and test initialization function
__all__ = ['get_db', 'get_test_db', 'close_db']