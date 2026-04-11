import json
import os

VAULT_FILE = '.void_vault'

def get_credentials():
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, 'r') as f:
            return json.load(f)
    
    print(" [!] VOIDSTAMP: SECURITY CREDENTIALS NOT FOUND")
    api_id = input(" [+] ENTER API_ID: ").strip()
    api_hash = input(" [+] ENTER API_HASH: ").strip()
    
    data = {'api_id': api_id, 'api_hash': api_hash}
    
    with open(VAULT_FILE, 'w') as f:
        json.dump(data, f)
    
    return data
