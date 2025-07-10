import re
import tldextract
import whois
from urllib.parse import urlparse, parse_qs
import socket
import ssl
from datetime import datetime, timedelta

def analyze_url_heuristics(url):
    """
    Analyze URL for phishing indicators using heuristic rules
    
    Args:
        url: URL to analyze
        
    Returns:
        dict: Analysis results with risk score and warnings
    """
    risk_score = 0
    warnings = []
    try:
        # Parse URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        path = parsed_url.path.lower()
        query = parsed_url.query.lower()
        # Extract domain components
        extracted = tldextract.extract(url)
        domain_name = extracted.domain
        subdomain = extracted.subdomain
        suffix = extracted.suffix
        TRUSTED_DOMAINS = [
            "google.com", "github.com", "amazon.com", "microsoft.com", "paypal.com",
            "linkedin.com", "facebook.com", "apple.com", "netflix.com"
        ]
        # If trusted, skip heuristics
        netloc = urlparse(url).netloc.lower()
        if any(trusted in netloc for trusted in TRUSTED_DOMAINS):
            return {
                'risk_score': 0,
                'warnings': ["Domain is trusted, skipped heuristic checks"],
                'domain_info': {
                    'domain': netloc,
                    'subdomain': tldextract.extract(url).subdomain,
                    'tld': tldextract.extract(url).suffix
                }
            }
        # 1. Check for suspicious domain patterns
        risk_score, warnings = check_domain_patterns(domain, domain_name, subdomain, risk_score, warnings)
        # 2. Check for suspicious keywords in URL
        risk_score, warnings = check_suspicious_keywords(url, domain, path, query, risk_score, warnings)
        # 3. Check for URL shorteners
        risk_score, warnings = check_url_shorteners(domain, risk_score, warnings)
        # 4. Check for IP addresses instead of domains
        risk_score, warnings = check_ip_addresses(domain, risk_score, warnings)
        # 5. Check for suspicious TLDs
        risk_score, warnings = check_suspicious_tlds(suffix, risk_score, warnings)
        # 6. Check for excessive subdomains
        risk_score, warnings = check_subdomain_depth(subdomain, risk_score, warnings)
        # 7. Check for brand impersonation
        risk_score, warnings = check_brand_impersonation(domain, domain_name, risk_score, warnings)
        # 8. Check for HTTPS usage
        risk_score, warnings = check_https_usage(parsed_url.scheme, risk_score, warnings)
        # 9. Check for suspicious path patterns
        risk_score, warnings = check_suspicious_paths(path, risk_score, warnings)
        # 10. Check for excessive URL length
        risk_score, warnings = check_url_length(url, risk_score, warnings)
        # 11. Check for domain age (recently registered domains)
        risk_score, warnings = check_domain_age(domain, risk_score, warnings)
        # 12. Check for SSL certificate validity
        risk_score, warnings = check_ssl_certificate(domain, risk_score, warnings)
        # 13. Check for '@' symbol in URL
        risk_score, warnings = check_at_symbol(url, risk_score, warnings)
        # 14. Check for multiple '//' in path
        risk_score, warnings = check_multiple_slashes(path, risk_score, warnings)
        # 15. Check for uncommon ports
        risk_score, warnings = check_uncommon_ports(parsed_url, risk_score, warnings)
        # 16. Check for hex/percent-encoded characters in path
        risk_score, warnings = check_encoded_chars(path, risk_score, warnings)
        # 17. Check for suspicious query parameters
        risk_score, warnings = check_suspicious_query(query, risk_score, warnings)
        return {
            'risk_score': risk_score,
            'warnings': warnings,
            'domain_info': {
                'domain': domain,
                'subdomain': subdomain,
                'tld': suffix
            }
        }
    except Exception as e:
        warnings.append(f"Error during heuristic analysis: {str(e)}")
        return {
            'risk_score': risk_score,
            'warnings': warnings,
            'error': str(e)
        }

def check_domain_patterns(domain, domain_name, subdomain, risk_score, warnings):
    """Check for suspicious domain patterns"""
    
    # Check for numbers in domain (common in phishing)
    if re.search(r'\d', domain_name):
        risk_score += 10
        warnings.append("Domain contains numbers (suspicious pattern)")
    
    # Check for excessive hyphens
    if domain.count('-') > 2:
        risk_score += 15
        warnings.append("Domain contains excessive hyphens")
    
    # Check for lookalike characters
    lookalike_patterns = [
        (r'[0o]', '0/o confusion'),
        (r'[1l]', '1/l confusion'),
        (r'[5s]', '5/s confusion'),
        (r'[8b]', '8/b confusion')
    ]
    
    for pattern, description in lookalike_patterns:
        if re.search(pattern, domain):
            risk_score += 5
            warnings.append(f"Domain contains {description}")
    
    return risk_score, warnings

def check_suspicious_keywords(url, domain, path, query, risk_score, warnings):
    """Check for suspicious keywords in URL"""
    
    suspicious_keywords = [
        'login', 'signin', 'account', 'verify', 'secure', 'update', 'confirm',
        'banking', 'paypal', 'amazon', 'ebay', 'facebook', 'google', 'microsoft',
        'apple', 'netflix', 'spotify', 'instagram', 'twitter', 'linkedin',
        'password', 'credential', 'security', 'alert', 'warning', 'suspended',
        'limited', 'restricted', 'verify', 'confirm', 'validate', 'authenticate'
    ]
    
    url_lower = url.lower()
    found_keywords = []
    
    for keyword in suspicious_keywords:
        if keyword in url_lower:
            found_keywords.append(keyword)
    
    if found_keywords:
        risk_score += len(found_keywords) * 5
        warnings.append(f"Suspicious keywords found: {', '.join(found_keywords)}")
    
    return risk_score, warnings

def check_url_shorteners(domain, risk_score, warnings):
    """Check for URL shortener services"""
    
    shorteners = [
        'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'v.gd', 'ow.ly',
        'short.to', 'adf.ly', 'sh.st', 'adfly.com', 'bitly.com', 'tiny.cc'
    ]
    
    if domain in shorteners:
        risk_score += 20
        warnings.append("URL uses a URL shortener service (potential hiding of destination)")
    
    return risk_score, warnings

def check_ip_addresses(domain, risk_score, warnings):
    """Check for IP addresses instead of domain names"""
    
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    
    if re.match(ip_pattern, domain):
        risk_score += 25
        warnings.append("Domain is an IP address (suspicious)")
    
    return risk_score, warnings

def check_suspicious_tlds(suffix, risk_score, warnings):
    """Check for suspicious top-level domains"""
    
    suspicious_tlds = [
        '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club', '.online',
        '.site', '.website', '.space', '.tech', '.digital', '.click'
    ]
    
    if suffix in suspicious_tlds:
        risk_score += 15
        warnings.append(f"Suspicious TLD detected: {suffix}")
    
    return risk_score, warnings

def check_subdomain_depth(subdomain, risk_score, warnings):
    """Check for excessive subdomain depth"""
    
    if subdomain and subdomain.count('.') > 2:
        risk_score += 10
        warnings.append("Excessive subdomain depth detected")
    
    return risk_score, warnings

def check_brand_impersonation(domain, domain_name, risk_score, warnings):
    """Check for potential brand impersonation"""
    
    popular_brands = [
        'google', 'facebook', 'amazon', 'microsoft', 'apple', 'netflix',
        'paypal', 'ebay', 'twitter', 'instagram', 'linkedin', 'spotify',
        'youtube', 'whatsapp', 'telegram', 'discord', 'slack', 'zoom'
    ]
    
    for brand in popular_brands:
        if brand in domain_name and domain_name != brand:
            risk_score += 30
            warnings.append(f"Potential brand impersonation: {brand}")
            break
    
    return risk_score, warnings

def check_https_usage(scheme, risk_score, warnings):
    """Check if HTTPS is used"""
    
    if scheme != 'https':
        risk_score += 10
        warnings.append("URL does not use HTTPS (insecure)")
    
    return risk_score, warnings

def check_suspicious_paths(path, risk_score, warnings):
    """Check for suspicious path patterns"""
    
    suspicious_paths = [
        '/login', '/signin', '/account', '/verify', '/secure', '/update',
        '/confirm', '/password', '/credential', '/security', '/alert'
    ]
    
    for suspicious_path in suspicious_paths:
        if suspicious_path in path:
            risk_score += 5
            warnings.append(f"Suspicious path detected: {suspicious_path}")
    
    return risk_score, warnings

def check_url_length(url, risk_score, warnings):
    """Check for excessive URL length"""
    
    if len(url) > 200:
        risk_score += 10
        warnings.append("URL is excessively long")
    
    return risk_score, warnings 

def check_domain_age(domain, risk_score, warnings):
    """Check if domain is recently registered (less than 6 months old)"""
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age = (datetime.utcnow() - creation_date).days
            if age < 180:
                risk_score += 20
                warnings.append("Domain is very new (registered < 6 months ago)")
    except Exception:
        warnings.append("Could not determine domain age")
    return risk_score, warnings

def check_ssl_certificate(domain, risk_score, warnings):
    """Check SSL certificate validity (expired/self-signed)"""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(3)
            s.connect((domain, 443))
            cert = s.getpeercert()
            not_after = cert.get('notAfter')
            if not_after:
                expire_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                if expire_date < datetime.utcnow():
                    risk_score += 15
                    warnings.append("SSL certificate is expired")
    except Exception:
        warnings.append("Could not verify SSL certificate")
    return risk_score, warnings

def check_at_symbol(url, risk_score, warnings):
    if '@' in url:
        risk_score += 10
        warnings.append("URL contains '@' symbol (obfuscation attempt)")
    return risk_score, warnings

def check_multiple_slashes(path, risk_score, warnings):
    if path.count('//') > 0:
        risk_score += 5
        warnings.append("URL path contains multiple '//' (obfuscation)")
    return risk_score, warnings

def check_uncommon_ports(parsed_url, risk_score, warnings):
    port = parsed_url.port
    if port and port not in [80, 443]:
        risk_score += 10
        warnings.append(f"URL uses uncommon port: {port}")
    return risk_score, warnings

def check_encoded_chars(path, risk_score, warnings):
    if re.search(r'%[0-9a-fA-F]{2}', path) or re.search(r'\\x[0-9a-fA-F]{2}', path):
        risk_score += 5
        warnings.append("Path contains hex or percent-encoded characters")
    return risk_score, warnings

def check_suspicious_query(query, risk_score, warnings):
    # Check for long tokens or base64-like parameters
    for k, v in parse_qs(query).items():
        for val in v:
            if len(val) > 50:
                risk_score += 5
                warnings.append(f"Suspiciously long query parameter: {k}")
            if re.fullmatch(r'[A-Za-z0-9+/=]{32,}', val):
                risk_score += 5
                warnings.append(f"Query parameter {k} looks like base64-encoded data")
    return risk_score, warnings 