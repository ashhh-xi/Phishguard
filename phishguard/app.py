from flask import Flask, request, jsonify, render_template
import joblib
import os
import pandas as pd
from utils.preprocess_email import clean_email
from utils.safe_browsing import check_google_safebrowsing
import base64
from io import BytesIO
from PIL import Image
import json

# Import QR detection modules
from utils.qr_decoder import decode_qr_image
from utils.heuristics import analyze_url_heuristics
from utils.virustotal import check_virustotal

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Load email model and vectorizer
email_model = joblib.load(os.path.join(MODELS_DIR, 'phishing_email_model.pkl'))
email_vectorizer = joblib.load(os.path.join(MODELS_DIR, 'email_vectorizer.pkl'))

@app.route('/')
def home():
    """Render the main page with both email and QR detection options"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/features')
def features():
    """Features page"""
    return render_template('features.html')

@app.route('/predict-email', methods=['POST'])
def predict_email():
    """Original email prediction endpoint"""
    data = request.get_json()
    email_text = data.get('email')
    if not email_text:
        return jsonify({'error': 'No email provided'}), 400
    clean_text = clean_email(email_text)
    X = email_vectorizer.transform([clean_text])
    proba = email_model.predict_proba(X)[0]
    pred = email_model.predict(X)[0]
    phishing_conf = proba[list(email_model.classes_).index(1)]
    result = 'Phishing' if pred == 1 else 'Legitimate'
    return jsonify({
        'result': result,
        'confidence': round(float(phishing_conf), 2)
    })


@app.route('/check-url-google', methods=['POST'])
def check_url_google():
    """New Google Safe Browsing endpoint"""
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    result = google_safe_browsing_api(url)
    return jsonify(result)

# New QR detection routes
@app.route('/scan-image', methods=['POST'])
def scan_image():
    """Handle uploaded QR image and decode it"""
    try:
        if 'qr_image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['qr_image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read and decode the image
        image_data = file.read()
        image = Image.open(BytesIO(image_data))
        
        # Decode QR code
        url = decode_qr_image(image)
        
        if not url:
            return jsonify({'error': 'No QR code found in image or could not decode'}), 400
        
        return jsonify({'url': url})
    
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/check-url', methods=['POST'])
def check_url():
    """Analyze URL for phishing indicators using multiple methods"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Initialize results
        results = {
            'url': url,
            'checks': {},
            'overall_risk_score': 0,
            'verdict': 'Safe',
            'reasoning': []
        }
        
        # 1. Google Safe Browsing check
        try:
            safe_browsing_result = check_google_safebrowsing(url)
            results['checks']['google_safe_browsing'] = safe_browsing_result
            if safe_browsing_result['phishing']:
                results['overall_risk_score'] += 80
                results['reasoning'].append(f"Google Safe Browsing detected: {safe_browsing_result['threatType']}")
        except Exception as e:
            results['checks']['google_safe_browsing'] = {'error': str(e)}
        
        # 2. Heuristic analysis
        try:
            heuristic_result = analyze_url_heuristics(url)
            results['checks']['heuristics'] = heuristic_result
            results['overall_risk_score'] += heuristic_result['risk_score']
            if heuristic_result['risk_score'] > 0:
                results['reasoning'].extend(heuristic_result['warnings'])
        except Exception as e:
            results['checks']['heuristics'] = {'error': str(e)}
        
        # 3. VirusTotal check
        try:
            virustotal_result = check_virustotal(url)
            results['checks']['virustotal'] = virustotal_result
            if virustotal_result.get('malicious_votes', 0) > 0:
                results['overall_risk_score'] += 60
                results['reasoning'].append(f"VirusTotal: {virustotal_result['malicious_votes']} security vendors flagged this URL")
        except Exception as e:
            results['checks']['virustotal'] = {'error': str(e)}
        
        # Determine overall verdict
        if results['overall_risk_score'] >= 80:
            results['verdict'] = 'Phishing'
        elif results['overall_risk_score'] >= 40:
            results['verdict'] = 'Suspicious'
        else:
            results['verdict'] = 'Safe'
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing URL: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 