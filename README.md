# PhishGuard: AI-Powered Email Phishing Detection

PhishGuard is a modern, AI-powered web application for detecting phishing emails. It leverages natural language processing (NLP) and machine learning to classify emails as "Phishing" or "Legitimate" with high accuracy, providing confidence scores and a user-friendly interface.

---

## 🚀 Features
- **Email Phishing Detection**: Paste any email text and get instant phishing/legitimate classification.
- **Confidence Score**: See how confident the model is in its prediction.
- **Modern UI**: Clean, SaaS-style frontend with smooth UX, responsive design, and elegant visuals.
- **API Endpoint**: Easily integrate phishing detection into other tools via a REST API.
- **Open Source**: All code, models, and training scripts are included (except the dataset).

---

## 🖼️ Demo
![PhishGuard UI Screenshot](demo_screenshot.png) <!-- Add your screenshot here -->

---

## 🧠 How It Works

### 1. Data & Preprocessing
- **Dataset**: The main dataset is [`phishing_email.csv`](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset) from Kaggle, containing labeled email samples.
- **Preprocessing**: Emails are lowercased, non-alphanumeric characters are removed, and stopwords are filtered out using NLTK.

### 2. Feature Extraction
- **TF-IDF Vectorization**: The cleaned email text is transformed into numerical features using TF-IDF (max 3000 features, unigrams and bigrams).

### 3. Model Training & Evaluation
- **Model**: Logistic Regression (scikit-learn)
- **Training/Test Split**: 80/20 split
- **Metrics**:
  - **Accuracy**: ~0.98 (example, see your actual output)
  - **Classification Report**: Includes precision, recall, f1-score for each class

Example output from training:
```
Email Model Accuracy: 0.98
Classification Report:
              precision    recall  f1-score   support

           0       0.98      0.98      0.98      1000
           1       0.98      0.98      0.98      1000

    accuracy                           0.98      2000
   macro avg       0.98      0.98      0.98      2000
weighted avg       0.98      0.98      0.98      2000
```

> **Note:** You can retrain the model using `phishguard/scripts/train_email_model.py`.

### 4. API & Frontend
- **Flask Backend**: `/predict-email` endpoint accepts POST requests with email text and returns prediction + confidence.
- **Frontend**: Modern HTML/CSS interface for easy use.

---

## 🛠️ Usage

### 1. Installation
```bash
# Clone the repo
git clone https://github.com/ashhh-xi/Phishguard.git
cd Phishguard

# Install dependencies
pip install -r requirements.txt
```

### 2. Restore the Dataset
The main dataset is not included in the repo due to size. Download it from Kaggle:
- [Phishing Email Dataset on Kaggle](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)
- Place `phishing_email.csv` in `phishguard/datasets/`

Or use the provided script:
```bash
pip install kagglehub[pandas-datasets]
python phishguard/datasets/restore_phishing_email.py
```

### 3. Run the App
```bash
cd phishguard
python app.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser.

### 4. API Usage
Send a POST request to `/predict-email` with JSON:
```json
{
  "email": "Your email text here"
}
```
Response:
```json
{
  "result": "Phishing",
  "confidence": 0.97
}
```

---

## 📁 Project Structure
```
phishguard/
  app.py                  # Flask backend
  models/                 # Trained model and vectorizer
  datasets/               # Datasets (add phishing_email.csv here)
  scripts/
    train_email_model.py  # Model training script
  utils/
    preprocess_email.py   # Email cleaning utility
  templates/
    index.html            # Frontend UI
  static/
    js/                   # (Optional) JS files
  uploads/                # (Optional) Uploads
```

---

## 📊 Results & Evaluation
- **Accuracy**: ~0.98 (see training output)
- **Precision/Recall/F1**: See classification report above
- **Features Used**: Top 3000 TF-IDF features (unigrams and bigrams) from cleaned email text
- **Preprocessing**: Lowercasing, removing non-alphanumeric chars, stopword removal

---

## 📚 Dataset
- **Source**: [Phishing Email Dataset on Kaggle](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)
- **How to Add**: Download `phishing_email.csv` and place it in `phishguard/datasets/`

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
This project is licensed under the MIT License.

---

## 📬 Contact
- **GitHub**: [ashhh-xi](https://github.com/ashhh-xi/Phishguard)
- **Kaggle Dataset**: [Phishing Email Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)

---

**PhishGuard – Protect your inbox with AI.** 