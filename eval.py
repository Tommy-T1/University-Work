import sys
import os

# Add only vendor directories to sys.path
external_libs_path = "/home/viavii/Desktop/my_project/Sentiment Analysis in arabic/external_libs"
vendor_libs = ["spacy", "sklearn", "tqdm", "pandas", "matplotlib", "seaborn"]

for lib in vendor_libs:
    lib_path = os.path.join(external_libs_path, lib)
    if os.path.isdir(lib_path):
        sys.path.insert(0, lib_path)
    else:
        print(f"Warning: {lib_path} not found.")

import pandas as pd
from spacy_arabic_sentiment import ArabicSentimentAnalyzer
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

def evaluate_model(model, test_data):
    predictions = []
    confidences = []
    # Convert numeric labels to string labels using model's label_map
    actuals = [model.label_map[label] for label in test_data['label'].tolist()]
    
    for text in tqdm(test_data['text'], desc="Evaluating"):
        pred, conf = model.analyze(text)
        predictions.append(pred)  # pred is already a string
        confidences.append(conf)
    
    print("\nClassification Report:")
    print(classification_report(actuals, predictions, target_names=["negative", "neutral", "positive"]))
    
    cm = confusion_matrix(actuals, predictions, labels=["negative", "neutral", "positive"])
    plt.figure(figsize=(10,8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig('confusion_matrix.png')
    plt.close()
    
    return pd.DataFrame({
        'text': test_data['text'],
        'actual': actuals,
        'predicted': predictions,
        'confidence': confidences
    })

def main():
    # Replace with your actual dataset path
    data_path = "/home/viavii/Desktop/my_project/Sentiment Analysis in arabic/data/sentiment_data.csv"
    
    # Initialize model and load data
    model = ArabicSentimentAnalyzer(data_path=data_path)
    
    # Train and evaluate (no epochs/batch_size/learning_rate for spaCy+sklearn)
    model.train_and_evaluate()
    
    # Evaluate on test set
    test_data = pd.DataFrame({
        'text': model.test_texts,
        'label': model.test_labels
    })
    results = evaluate_model(model, test_data)
    results.to_csv('evaluation_results.csv', index=False)
    print("\nResults saved to evaluation_results.csv")

if __name__ == "__main__":
    main()