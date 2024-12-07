from dotenv import load_dotenv
import os
from py_clob_client.client import ClobClient
from py_clob_client.constants import POLYGON

load_dotenv()

def main():
    # Ensure correct endpoint and API key loading
    host = "https://clob.polymarket.com"
    key = os.getenv("PK")
    if not key:
        print("Private key (PK) not found in environment variables")
        return

    chain_id = POLYGON  # Polygon Mainnet ChainID
    client = ClobClient(host, key=key, chain_id=chain_id)

    try:
        # Check for existing API keys
        existing_api_keys = client.derive_api_key(nonce=0)
        if existing_api_keys:
            print("Existing API keys found:", existing_api_keys)
        else:
            # If no existing API key, try creating a new API key with different nonce
            print("No existing API keys found. Trying to create a new API key with nonce 1.")
            api_key_response = client.create_api_key(nonce=1)
            print("API Key created successfully:", api_key_response)
    except Exception as e:
        print("Failed to create API keys:", str(e))
        if hasattr(e, 'error_message'):
            print("Error message:", e.error_message)
        if hasattr(e, 'status_code'):
            print("Status code:", e.status_code)

if __name__ == "__main__":
    main()
