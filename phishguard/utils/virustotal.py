import os
import requests
import hashlib
import time
from urllib.parse import urlparse

API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")

def check_virustotal(url, api_key=API_KEY):
    """
    Check URL against VirusTotal API
    
    Args:
        url: URL to check
        api_key: VirusTotal API key
        
    Returns:
        dict: Results with malicious votes and scan details
    """
    if not api_key:
        return {
            'malicious_votes': 0,
            'total_votes': 0,
            'error': 'VirusTotal API key not configured'
        }
    
    try:
        # First, submit the URL for scanning if not already scanned
        submit_url = "https://www.virustotal.com/vtapi/v2/url/scan"
        submit_params = {
            'apikey': api_key,
            'url': url
        }
        
        submit_response = requests.post(submit_url, data=submit_params, timeout=10)
        
        if submit_response.status_code != 200:
            return {
                'malicious_votes': 0,
                'total_votes': 0,
                'error': f'Failed to submit URL for scanning: {submit_response.status_code}'
            }
        
        # Wait a moment for the scan to complete
        time.sleep(2)
        
        # Now get the scan results
        report_url = "https://www.virustotal.com/vtapi/v2/url/report"
        report_params = {
            'apikey': api_key,
            'resource': url
        }
        
        report_response = requests.get(report_url, params=report_params, timeout=10)
        
        if report_response.status_code != 200:
            return {
                'malicious_votes': 0,
                'total_votes': 0,
                'error': f'Failed to get scan report: {report_response.status_code}'
            }
        
        data = report_response.json()
        
        # Extract scan results
        if 'positives' in data and 'total' in data:
            malicious_votes = data['positives']
            total_votes = data['total']
            
            # Get detailed scan results
            scans = data.get('scans', {})
            scan_details = {}
            
            for vendor, result in scans.items():
                if result.get('detected', False):
                    scan_details[vendor] = {
                        'detected': True,
                        'result': result.get('result', 'Unknown')
                    }
            
            return {
                'malicious_votes': malicious_votes,
                'total_votes': total_votes,
                'scan_date': data.get('scan_date'),
                'scan_details': scan_details,
                'permalink': data.get('permalink'),
                'confidence': 'high' if total_votes > 0 else 'low'
            }
        else:
            return {
                'malicious_votes': 0,
                'total_votes': 0,
                'error': 'No scan results available',
                'response_code': data.get('response_code', 0)
            }
            
    except requests.exceptions.Timeout:
        return {
            'malicious_votes': 0,
            'total_votes': 0,
            'error': 'Request timeout'
        }
    except requests.exceptions.RequestException as e:
        return {
            'malicious_votes': 0,
            'total_votes': 0,
            'error': f'Network error: {str(e)}'
        }
    except Exception as e:
        return {
            'malicious_votes': 0,
            'total_votes': 0,
            'error': f'Unexpected error: {str(e)}'
        }

def get_url_hash(url):
    """
    Get SHA-256 hash of URL for VirusTotal API
    
    Args:
        url: URL to hash
        
    Returns:
        str: SHA-256 hash of the URL
    """
    return hashlib.sha256(url.encode()).hexdigest()

def is_valid_virustotal_response(data):
    """
    Check if VirusTotal response is valid
    
    Args:
        data: Response data from VirusTotal
        
    Returns:
        bool: True if response is valid
    """
    return (
        isinstance(data, dict) and
        'response_code' in data and
        data['response_code'] == 1
    ) 