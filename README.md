# 🛡️ PhishGuard - AI-Powered Phishing Detection

A comprehensive web application that protects users from phishing attacks through multiple detection methods: AI-powered email analysis, QR code scanning, and direct URL analysis.

## ✨ Features

### 📧 Email Phishing Detection
- **AI-Powered Analysis**: Advanced machine learning algorithms trained on extensive phishing datasets
- **High Accuracy**: 98%+ detection rate using TF-IDF vectorization and logistic regression
- **Real-time Processing**: Instant analysis with confidence scoring
- **Pattern Recognition**: Detects urgency, suspicious language, and phishing indicators

### 📱 QR Code Scanning
- **Live Camera Scanning**: Real-time QR code detection using device camera
- **Image Upload**: Support for uploading QR code images (JPG, PNG, GIF, BMP)
- **Multi-format Support**: Handles various QR code formats and standards
- **Mobile Optimized**: Responsive design for mobile devices

### 🔗 Manual URL Detection
- **Direct URL Input**: Paste any URL for instant phishing analysis
- **Real-time Validation**: Immediate URL format and accessibility checks
- **Comprehensive Security**: Multi-layer threat detection using multiple APIs
- **Detailed Reporting**: Complete analysis with risk scoring and explanations

### 🛡️ Multi-Layer Security Analysis
- **Google Safe Browsing API**: Real-time checking against Google's threat database
- **VirusTotal Integration**: Multi-engine scanning using 70+ security vendors
- **Heuristic Analysis**: Pattern-based detection using URL analysis and domain checks
- **Domain Reputation**: SSL certificate validation and domain age analysis

## 📧 Email Phishing Detection Model

PhishGuard uses a dedicated machine learning model to detect phishing emails with high accuracy and speed. Below are the details of the email prediction pipeline:

### Model Architecture
- **TF-IDF Vectorizer**: Converts email text into numerical feature vectors based on term frequency-inverse document frequency.
- **Logistic Regression Classifier**: Trained to distinguish between phishing and legitimate emails using the TF-IDF features.

### Training Datasets
- **Sources**: Public phishing and legitimate email datasets, including:
  - CEAS 2008
  - Enron
  - Ling
  - Nazario
  - Nigerian Fraud
  - Phishing Email
  - SpamAssassin
- **Size**: Over 50,000 labeled email samples (phishing and legitimate)

### Feature Engineering
- **Text Preprocessing**: Lowercasing, stopword removal, punctuation stripping, tokenization
- **Feature Extraction**: 1000+ TF-IDF features per email
- **Pattern Recognition**: Additional features for urgency, suspicious language, and phishing indicators

### Model Performance
- **Accuracy**: 98%+ on validation/test sets
- **Metrics**: Precision, recall, F1-score, ROC-AUC
- **Speed**: <1 second per prediction

### Usage in the App
1. **User Input**: User pastes or uploads email content via the web interface
2. **Preprocessing**: Email is cleaned and vectorized using the trained TF-IDF model
3. **Prediction**: Logistic Regression model outputs a phishing probability/confidence score
4. **Result Display**: The app shows the verdict (phishing/legitimate) and the confidence score to the user

### Limitations & Notes
- The model is trained on English-language emails
- May not detect highly novel or obfuscated phishing attempts
- No user data is stored; all analysis is performed in-memory and in real-time

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API keys for Google Safe Browsing and VirusTotal (optional but recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/phishguard.git
   cd phishguard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the `phishguard` directory:
   ```env
   GOOGLE_SAFE_BROWSING_API_KEY=your_google_api_key_here
   VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
   ```

4. **Run the application**
   ```bash
   cd phishguard
   python start_app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`

## 📖 Usage

### Email Detection
1. Click on "Analyze Email" from the main dashboard
2. Paste the email content you want to analyze
3. Click "Analyze Email" to get instant results
4. View the confidence score and phishing verdict

### QR Code Scanning
1. Click on "Scan QR Code" from the main dashboard
2. Choose between:
   - **Upload Image**: Select a QR code image file
   - **Use Camera**: Scan QR codes with your device camera
3. The system will automatically extract and analyze the URL
4. View comprehensive security analysis results

### Manual URL Detection
1. Click on "Check URL" from the main dashboard
2. Paste any URL you want to analyze (must start with http:// or https://)
3. Click "Check URL" for instant analysis
4. Review detailed security assessment and risk scoring

## 🔧 Technology Stack

### Backend
- **Flask**: Web framework for API endpoints
- **Python**: Core programming language
- **Scikit-learn**: Machine learning for email analysis
- **PyZBar**: QR code decoding
- **PIL/Pillow**: Image processing

### Frontend
- **HTML5/CSS3**: Modern, responsive design
- **JavaScript**: Interactive user interface
- **HTML5-QRCode**: Real-time camera scanning

### Security APIs
- **Google Safe Browsing**: Threat database integration
- **VirusTotal**: Multi-engine security scanning
- **Heuristic Analysis**: Custom pattern detection

### Deployment
- **Render**: Cloud deployment platform
- **Docker**: Containerization support

## 📊 Detection Methods

### Email Analysis
- **TF-IDF Vectorization**: Text feature extraction
- **Logistic Regression**: Phishing classification
- **Pattern Recognition**: Suspicious language detection
- **Confidence Scoring**: Probability-based results

### URL Analysis
- **Domain Analysis**: TLD extraction and validation
- **SSL Certificate Check**: Security protocol verification
- **Suspicious Keywords**: Phishing indicator detection
- **URL Structure Analysis**: Malicious pattern identification

### QR Code Processing
- **Image Decoding**: Multi-format QR code support
- **URL Extraction**: Automatic link detection
- **Real-time Scanning**: Live camera integration
- **Error Handling**: Robust processing capabilities

## 🔑 API Configuration

### Google Safe Browsing API
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Safe Browsing API
3. Create credentials and get your API key
4. Add to `.env` file: `GOOGLE_SAFE_BROWSING_API_KEY=your_key`

### VirusTotal API
1. Sign up at [VirusTotal](https://www.virustotal.com/)
2. Get your API key from your account settings
3. Add to `.env` file: `VIRUSTOTAL_API_KEY=your_key`

## 📁 Project Structure

```
phishguard/
├── app.py                 # Main Flask application
├── start_app.py          # Application startup script
├── requirements.txt      # Python dependencies
├── templates/
│   ├── index.html       # Main application interface
│   ├── about.html       # About page
│   └── features.html    # Features page
├── utils/
│   ├── preprocess_email.py      # Email preprocessing
│   ├── check_google_safebrowsing.py  # Safe Browsing API
│   └── google_checked_urls.log  # API call logging
├── models/
│   ├── email_vectorizer.pkl     # Email TF-IDF vectorizer
│   ├── phishing_email_model.pkl # Email classification model
│   └── phishing_url_model.pkl   # URL classification model
├── scripts/
│   └── train_email_model.py     # Model training script
└── datasets/
    ├── CEAS_08.csv
    ├── Enron.csv
    ├── Ling.csv
    ├── Nazario.csv
    ├── Nigerian_Fraud.csv
    ├── phishing_email.csv
    └── SpamAssasin.csv
```

## 🎯 Detection Capabilities

### Email Phishing Detection
- **Accuracy**: 98%+ detection rate
- **Speed**: < 1 second processing time
- **Features**: 1000+ text features analyzed
- **Datasets**: Trained on 50,000+ email samples

### URL Security Analysis
- **Multi-API**: Google Safe Browsing + VirusTotal
- **Heuristics**: Custom pattern detection
- **Real-time**: Live threat intelligence
- **Comprehensive**: 70+ security vendors

### QR Code Processing
- **Formats**: All standard QR code formats
- **Speed**: Instant decoding and analysis
- **Mobile**: Optimized for mobile devices
- **Reliability**: Robust error handling

## 🔒 Privacy & Security

- **No Data Storage**: Analysis performed in real-time, no data retention
- **Secure APIs**: All external API calls use HTTPS
- **Local Processing**: Email analysis performed locally
- **Privacy First**: No personal information collected or stored

## 🚀 Deployment

### Render Deployment
1. Create a free account at [Render](https://render.com/)
2. Click "New Web Service" and connect your GitHub repository
3. Set the build and start commands:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python start_app.py`
4. Set environment variables in the Render dashboard:
   - `GOOGLE_SAFE_BROWSING_API_KEY`
   - `VIRUSTOTAL_API_KEY`
5. Choose a Python environment (3.8+ recommended)
6. Deploy and access your app at the generated Render URL

### Docker Deployment
1. Build the Docker image:
   ```bash
   docker build -t phishguard .
   or
   ```
    docker-compose build --no-cache
    docker-compose up 
2. Run the container:
   ```bash
   docker run -p 5000:5000 phishguard

   ```


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Safe Browsing API** for threat intelligence
- **VirusTotal** for multi-engine security scanning
- **HTML5-QRCode** for camera scanning capabilities
- **Scikit-learn** for machine learning capabilities

## 📞 Support

- **Email**: contact@phishguard.com
- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/phishguard/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/phishguard/wiki)

---

**🛡️ Stay safe online with PhishGuard!** 