# 🛡️ PhishGuard QR - QR Code Phishing Detection System

A Flask-based web application that detects phishing URLs embedded in QR codes using a hybrid detection system combining Google Safe Browsing API, heuristic analysis, and VirusTotal integration.

## ✨ Features

### 🔍 Dual QR Input Modes
- **📷 Real-time QR Scanning**: Use your device camera to scan QR codes instantly
- **📁 Image Upload**: Upload QR code images from your device or desktop

### 🛡️ Multi-Layer Phishing Detection
- **Google Safe Browsing API**: Real-time blacklist checking against Google's threat database
- **Heuristic Analysis**: Pattern-based detection using URL analysis, domain checks, and suspicious indicators
- **VirusTotal Integration**: Multi-engine security vendor scanning

### 🎨 Modern UI/UX
- Responsive design that works on desktop and mobile devices
- Real-time camera access with HTML5 QR Code scanner
- Beautiful gradient design with intuitive user interface
- Detailed analysis results with risk scoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Web browser with camera access (for live scanning)
- API keys for enhanced detection (optional but recommended)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "PHISHING DETECTION/phishguard"
   ```

2. **Install dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Set up API keys (optional but recommended)**
   
   Create a `.env` file in the phishguard directory:
   ```bash
   # Google Safe Browsing API (Free tier available)
   GOOGLE_SAFE_BROWSING_API_KEY=your_google_api_key_here
   
   # VirusTotal API (Free tier available)
   VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 API Key Setup

### Google Safe Browsing API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the "Safe Browsing API"
4. Create credentials (API key)
5. Add the key to your `.env` file

### VirusTotal API
1. Sign up at [VirusTotal](https://www.virustotal.com/)
2. Go to your profile and generate an API key
3. Add the key to your `.env` file

## 📱 Usage

### Method 1: Upload QR Image
1. Click the "📁 Upload QR Image" option
2. Click "Choose QR Image File"
3. Select a QR code image from your device
4. Wait for analysis results

### Method 2: Live Camera Scan
1. Click the "📷 Scan with Camera" option
2. Click "Start Camera" and allow camera access
3. Point your camera at a QR code
4. The system will automatically detect and analyze the URL

### Understanding Results

The system provides a comprehensive analysis including:

- **🔍 Extracted URL**: The URL found in the QR code
- **🛡️ Verdict**: Safe / Suspicious / Phishing
- **📊 Risk Score**: 0-100 scale indicating threat level
- **📋 Analysis Details**: Breakdown of each security check

## 🏗️ Architecture

### Backend Structure
```
phishguard/
├── app.py                 # Main Flask application
├── utils/
│   ├── qr_decoder.py      # QR code decoding functionality
│   ├── heuristics.py      # URL pattern analysis
│   ├── safe_browsing.py   # Google Safe Browsing integration
│   └── virustotal.py      # VirusTotal API integration
├── templates/
│   └── index.html         # Main web interface
└── static/                # Static assets
```

### Detection Methods

#### 1. Google Safe Browsing
- Real-time threat database checking
- Detects malware, social engineering, and unwanted software
- High confidence results

#### 2. Heuristic Analysis
- **Domain Analysis**: Suspicious patterns, brand impersonation
- **URL Structure**: Length, suspicious keywords, path analysis
- **Security Indicators**: HTTPS usage, IP addresses, URL shorteners
- **TLD Analysis**: Suspicious top-level domains

#### 3. VirusTotal Integration
- Multi-engine security vendor scanning
- Community-based threat detection
- Detailed scan reports

## 🔒 Security Features

### Risk Scoring System
- **0-39**: Safe (Green)
- **40-79**: Suspicious (Yellow)
- **80-100**: Phishing (Red)

### Detection Capabilities
- ✅ Brand impersonation detection
- ✅ Suspicious domain patterns
- ✅ URL shortener identification
- ✅ IP address usage detection
- ✅ Suspicious TLD detection
- ✅ Keyword-based analysis
- ✅ HTTPS enforcement checking

## 🛠️ Technical Details

### Dependencies
- **Flask**: Web framework
- **pyzbar**: QR code decoding
- **Pillow**: Image processing
- **requests**: HTTP client
- **tldextract**: Domain parsing
- **python-whois**: WHOIS lookups
- **html5-qrcode**: Browser-based QR scanning

### Browser Compatibility
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

### Mobile Support
- iOS Safari
- Android Chrome
- Progressive Web App compatible

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables
```bash
export FLASK_ENV=production
export GOOGLE_SAFE_BROWSING_API_KEY=your_key
export VIRUSTOTAL_API_KEY=your_key
```

## 🔧 Configuration

### File Upload Limits
- Maximum file size: 16MB
- Supported formats: JPG, PNG, GIF, BMP

### API Rate Limits
- Google Safe Browsing: 10,000 requests/day (free tier)
- VirusTotal: 4 requests/minute (free tier)

### Customization
You can modify detection rules in `utils/heuristics.py`:
- Add new suspicious keywords
- Adjust risk scoring weights
- Customize brand detection lists

## 🐛 Troubleshooting

### Common Issues

**Camera not working:**
- Ensure HTTPS is used in production
- Check browser permissions
- Try refreshing the page

**QR code not detected:**
- Ensure image is clear and well-lit
- Check if QR code is damaged
- Try different image formats

**API errors:**
- Verify API keys are correct
- Check API quotas and limits
- Ensure internet connectivity

### Error Messages
- "No QR code found": Image doesn't contain a readable QR code
- "API key not configured": Missing or invalid API keys
- "Network error": Connection issues with external services

## 📈 Performance

### Optimization Tips
- Use compressed images for faster uploads
- Implement caching for repeated URL checks
- Consider CDN for static assets in production

### Monitoring
- Check API usage and quotas
- Monitor error logs
- Track detection accuracy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Safe Browsing API for threat detection
- VirusTotal for multi-engine scanning
- HTML5-QRCode library for browser-based scanning
- PyZBar for server-side QR decoding

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Open an issue on GitHub

---

**⚠️ Disclaimer**: This tool is for educational and security research purposes. Always use responsibly and in accordance with applicable laws and regulations. 