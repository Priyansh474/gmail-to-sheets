import json
import os

# Use an absolute path to the processed IDs file in the project root
STATE_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'processed_ids.json')
)


def load_processed_ids():
    """
    Load the set of already processed email IDs from a local file
    """
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return set(json.load(f))
    return set()


def save_processed_id(email_id):
    """
    Add an email ID to the processed list and save to file
    """
    processed_ids = load_processed_ids()
    processed_ids.add(email_id)
    
    with open(STATE_FILE, 'w') as f:
        json.dump(list(processed_ids), f)
