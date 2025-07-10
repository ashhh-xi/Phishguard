from pyzbar.pyzbar import decode
from PIL import Image
import re

def decode_qr_image(image):
    """
    Decode QR code from PIL Image and extract URL
    
    Args:
        image: PIL Image object
        
    Returns:
        str: Extracted URL or None if no QR code found
    """
    try:
        # Decode QR codes from the image
        decoded_objects = decode(image)
        
        if not decoded_objects:
            return None
        
        # Get the first decoded QR code
        qr_data = decoded_objects[0].data.decode('utf-8')
        
        # Check if the QR code contains a URL
        url = extract_url_from_qr_data(qr_data)
        
        return url
        
    except Exception as e:
        print(f"Error decoding QR code: {str(e)}")
        return None

def extract_url_from_qr_data(qr_data):
    """
    Extract URL from QR code data
    
    Args:
        qr_data: Raw QR code data
        
    Returns:
        str: Extracted URL or None if no URL found
    """
    # URL pattern matching
    url_patterns = [
        r'https?://[^\s<>"{}|\\^`\[\]]+',  # HTTP/HTTPS URLs
        r'www\.[^\s<>"{}|\\^`\[\]]+',     # WWW URLs
    ]
    
    for pattern in url_patterns:
        matches = re.findall(pattern, qr_data, re.IGNORECASE)
        if matches:
            url = matches[0]
            # Ensure URL has proper scheme
            if url.startswith('www.'):
                url = 'http://' + url
            return url
    
    # If no URL pattern found, check if the entire data looks like a URL
    if qr_data.startswith(('http://', 'https://', 'www.')):
        if qr_data.startswith('www.'):
            qr_data = 'http://' + qr_data
        return qr_data
    
    return None

def is_valid_url(url):
    """
    Basic URL validation
    
    Args:
        url: URL string to validate
        
    Returns:
        bool: True if URL appears valid
    """
    if not url:
        return False
    
    # Basic URL validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url)) 