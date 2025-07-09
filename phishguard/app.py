from flask import Flask, request, jsonify, render_template
import joblib
import os
import pandas as pd
from phishguard.utils.preprocess_email import clean_email

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Load email model and vectorizer
email_model = joblib.load(os.path.join(MODELS_DIR, 'phishing_email_model.pkl'))
email_vectorizer = joblib.load(os.path.join(MODELS_DIR, 'email_vectorizer.pkl'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict-email', methods=['POST'])
def predict_email():
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

if __name__ == '__main__':
    app.run(debug=True) 