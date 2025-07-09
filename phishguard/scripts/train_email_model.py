import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

def clean_email(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS]
    return ' '.join(tokens)

def main():
    # Load dataset (using phishing_email.csv as main, can be adjusted)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    phishguard_dir = os.path.abspath(os.path.join(script_dir, '..'))
    dataset_path = os.path.join(phishguard_dir, 'datasets', 'phishing_email.csv')
    model_dir = os.path.join(phishguard_dir, 'models')

    df = pd.read_csv(dataset_path)
    if 'text_combined' not in df.columns or 'label' not in df.columns:
        raise ValueError("CSV must have 'text_combined' and 'label' columns.")

    # Clean and preprocess
    df['clean_text'] = df['text_combined'].apply(clean_email)

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1,2))
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['label'].values

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Logistic Regression
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f'Email Model Accuracy: {acc:.4f}')
    print('Classification Report:')
    print(classification_report(y_test, y_pred))

    # Save model and vectorizer
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, 'phishing_email_model.pkl'))
    joblib.dump(vectorizer, os.path.join(model_dir, 'email_vectorizer.pkl'))
    print(f'Model saved to {os.path.join(model_dir, "phishing_email_model.pkl")}')
    print(f'Vectorizer saved to {os.path.join(model_dir, "email_vectorizer.pkl")}')

if __name__ == '__main__':
    main() 