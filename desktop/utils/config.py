import json
import os

CONFIG_FILE = 'config.json'


def save_token(token):
    """Save authentication token to config file."""
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    
    config['token'] = token
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


def load_token():
    """Load authentication token from config file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('token')
    return None


def clear_token():
    """Clear authentication token from config file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        if 'token' in config:
            del config['token']
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
