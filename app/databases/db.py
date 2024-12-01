# /databases/dp.py

import json
from pymongo import MongoClient
import constant

# Load config.json and update the password
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Replace <db_password> with the actual password
config['mongodb']['uri'] = config['mongodb']['uri'].replace('<db_password>', constant.MONGODB_PASSWORD)

# Save the updated config back to config.json
with open('config.json', 'w') as config_file:
    json.dump(config, config_file, indent=4)

# Connect to MongoDB using the updated config
client = MongoClient(config['mongodb']['uri'])
db = client[config['mongodb']['database']]
