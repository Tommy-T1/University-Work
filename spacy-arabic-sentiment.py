import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import spacy
from sklearn.metrics import classification_report
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class ArabicSentimentAnalyzer:
    def __init__(self, data_path=None):
        try:
            self.nlp = spacy.load("ar_core_news_sm")
        except OSError:
            print("Downloading spaCy Arabic model...")
            from spacy.cli import download
            download("ar_core_news_sm")
            self.nlp = spacy.load("ar_core_news_sm")
        self.label_map = {0: "negative", 1: "neutral", 2: "positive"}
        self.vectorizer = TfidfVectorizer()
        self.classifier = LogisticRegression(max_iter=1000)
        if data_path:
            self.load_and_split_data(data_path)

    def load_and_split_data(self, data_path, test_size=0.2, random_state=42):
        print(f"\nLoading data from {data_path}...")
        try:
            data = pd.read_csv(data_path)
            required_columns = ['text', 'label']
            if not all(col in data.columns for col in required_columns):
                raise ValueError(f"Data must contain columns: {required_columns}. Found columns: {data.columns.tolist()}")
            if data['label'].dtype == 'object':
                label_to_int = {label: idx for idx, label in self.label_map.items()}
                data['label'] = data['label'].map(label_to_int)
            train_data, test_data = train_test_split(
                data,
                test_size=test_size,
                random_state=random_state,
                stratify=data['label']
            )
            self.train_texts = train_data['text'].tolist()
            self.train_labels = train_data['label'].tolist()
            self.test_texts = test_data['text'].tolist()
            self.test_labels = test_data['label'].tolist()
            print(f"Total samples: {len(data)}")
            print(f"Training samples: {len(train_data)}")
            print(f"Test samples: {len(test_data)}")
            print("\nClass distribution in training set:")
            print(pd.Series(self.train_labels).value_counts().sort_index())
            return train_data, test_data
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise

    def preprocess_arabic(self, text):
        doc = self.nlp(text)
        tokens = [token.text for token in doc if not token.is_punct and not token.is_space]
        return " ".join(tokens)

    def train(self):
        print("\nPreprocessing and vectorizing training data...")
        train_texts_clean = [self.preprocess_arabic(text) for text in tqdm(self.train_texts, desc="Train preprocess")]
        X_train = self.vectorizer.fit_transform(train_texts_clean)
        y_train = self.train_labels
        print("\nTraining classifier...")
        self.classifier.fit(X_train, y_train)

    def analyze(self, text):
        cleaned_text = self.preprocess_arabic(text)
        X = self.vectorizer.transform([cleaned_text])
        pred = self.classifier.predict(X)[0]
        confidence = max(self.classifier.predict_proba(X)[0])
        sentiment = self.label_map[pred]
        return sentiment, confidence

    def train_and_evaluate(self):
        self.train()
        print("\nEvaluating on test set...")
        test_texts_clean = [self.preprocess_arabic(text) for text in tqdm(self.test_texts, desc="Test preprocess")]
        X_test = self.vectorizer.transform(test_texts_clean)
        predictions = self.classifier.predict(X_test)
        confidences = self.classifier.predict_proba(X_test).max(axis=1)
        print("\nTest Set Classification Report:")
        report = classification_report(
            self.test_labels,
            predictions,
            target_names=self.label_map.values(),
            digits=4
        )
        print(report)
        return {
            'predictions': predictions,
            'confidences': confidences,
            'report': report
        }

    def save_model(self, path):
        import joblib
        os.makedirs(path, exist_ok=True)
        joblib.dump(self.classifier, os.path.join(path, "classifier.joblib"))
        joblib.dump(self.vectorizer, os.path.join(path, "vectorizer.joblib"))
        print(f"Model saved to {path}")

    def load_model(self, path):
        import joblib
        self.classifier = joblib.load(os.path.join(path, "classifier.joblib"))
        self.vectorizer = joblib.load(os.path.join(path, "vectorizer.joblib"))
        print(f"Model loaded from {path}")

if __name__ == "__main__":
    data_path = "/home/viavii/Desktop/my_project/Sentiment Analysis in arabic/data/sentiment_data.csv"  
    analyzer = ArabicSentimentAnalyzer(data_path=data_path)
    analyzer.train_and_evaluate()