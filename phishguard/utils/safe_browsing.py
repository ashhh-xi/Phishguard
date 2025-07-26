import os
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the phishguard directory
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")
LOG_FILE = os.path.join(os.path.dirname(__file__), "google_checked_urls.log")

def check_browsing(url, api_key=API_KEY):
    """
    Check URL against Google Safe Browsing API
    """
    if not api_key:
        return {
            'phishing': False,
            'threatType': 'None',
            'error': 'Google Safe Browsing API key not configured'
        }
    try:
        endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
        payload = {
            "client": {
                "clientId": "phishguard-qr-app",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE", 
                    "SOCIAL_ENGINEERING", 
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        response = requests.post(endpoint, json=payload, timeout=10)
        if response.status_code != 200:
            return {
                'phishing': False,
                'threatType': 'None',
                'error': f'API request failed with status {response.status_code}: {response.text}'
            }
        data = response.json()
        # Log the checked URL and timestamp
        try:
            with open(LOG_FILE, "a", encoding='utf-8') as f:
                f.write(f"{datetime.utcnow().isoformat()}\t{url}\t{data}\n")
        except Exception as e:
            print(f"Warning: Could not log to file: {e}")
        if "matches" in data and data["matches"]:
            threat_type = data["matches"][0]["threatType"]
            return {
                'phishing': True,
                'threatType': threat_type,
                'confidence': 'high'
            }
        else:
            return {
                'phishing': False,
                'threatType': 'None',
                'confidence': 'high'
            }
    except requests.exceptions.Timeout:
        return {
            'phishing': False,
            'threatType': 'None',
            'error': 'Request timeout'
        }
    except requests.exceptions.RequestException as e:
        return {
            'phishing': False,
            'threatType': 'None',
            'error': f'Network error: {str(e)}'
        }
    except Exception as e:
        return {
            'phishing': False,
            'threatType': 'None',
            'error': f'Unexpected error: {str(e)}'
        }

def check_google_safebrowsing(url):
    return check_browsing(url)