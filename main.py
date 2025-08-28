import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, accuracy_score
from sentiment import ArabicSentimentAnalyzer

def map_labels(label):
    """Map text labels to numeric values"""
    if isinstance(label, str):
        label = label.lower()
        if label == 'positive':
            return 2
        elif label == 'negative':
            return 0
        else:  # neutral
            return 1
    return label

def check_duplicates(data, text_column='text'):
    """Check for duplicate texts in the dataset"""
    duplicates = data[data.duplicated([text_column], keep=False)]
    if not duplicates.empty:
        print(f"\nWarning: Found {len(duplicates)} duplicate texts")
    return duplicates

def print_class_distribution(data, label_column='label', name=""):
    """Print detailed class distribution statistics"""
    print(f"\n=== {name} Statistics ===")
    print(f"Total samples: {len(data)}")
    
    # Map numeric labels to text for display
    label_names = {0: "Negative", 1: "Neutral", 2: "Positive"}
    
    print("\nClass Distribution:")
    dist = data[label_column].value_counts()
    percentages = data[label_column].value_counts(normalize=True) * 100
    
    for label, count in dist.items():
        sentiment = label_names.get(label, str(label))
        print(f"{sentiment}: {count} samples ({percentages[label]:.2f}%)")
    
    print("\nSample texts per class:")
    for label in sorted(data[label_column].unique()):
        sentiment = label_names.get(label, str(label))
        samples = data[data[label_column] == label]['text'].head(2)
        print(f"\n{sentiment} examples:")
        for idx, text in enumerate(samples, 1):
            print(f"{idx}. {text[:100]}...")

def main():
    # Load Sheet1 dataset
    print("\nLoading Sheet1 dataset...")
    sheet1_path = "/home/tt/Desktop/NLP project/Sheet1.csv"
    data = pd.read_csv(sheet1_path)
    
    # Check structure of Sheet1 dataset
    print(f"Sheet1 dataset shape: {data.shape}")
    print(f"Sheet1 columns: {data.columns.tolist()}")
    
    # Adjust column names if needed
    text_column = 'Text' if 'Text' in data.columns else 'text'
    label_column = 'Polarity' if 'Polarity' in data.columns else 'label'
    
    # Rename columns for consistency
    data = data.rename(columns={text_column: 'text', label_column: 'label'})
    
    # Check and clean data
    data.dropna(subset=['text', 'label'], inplace=True)
    check_duplicates(data)
    
    # Map labels to numeric values
    data['label'] = data['label'].apply(map_labels)
    
    # Display class distribution
    print_class_distribution(data, name="Sheet1 Dataset")

    # Split data into train and test sets ONLY - NO VALIDATION
    X = data['text']
    y = data['label']
    
    # Simple 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create DataFrames
    train_data = pd.DataFrame({'text': X_train, 'label': y_train}).reset_index(drop=True)
    test_data = pd.DataFrame({'text': X_test, 'label': y_test}).reset_index(drop=True)

    # Print split distributions
    print_class_distribution(train_data, name="Training Set")
    print_class_distribution(test_data, name="Test Set")

    # Calculate class weights
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_data['label']),
        y=train_data['label']
    )
    class_weight_dict = dict(zip(range(len(class_weights)), class_weights))
    print("\nClass weights:", class_weight_dict)

    # Initialize and train model
    print("\nInitializing Arabic Sentiment Analyzer...")
    analyzer = ArabicSentimentAnalyzer(num_labels=3)
    
    test_accuracy = analyzer.train_and_evaluate(
        train_texts=train_data['text'].tolist(),
        train_labels=train_data['label'].tolist(),
        test_texts=test_data['text'].tolist(),
        test_labels=test_data['label'].tolist(),
        epochs=5,
        batch_size=16,
        learning_rate=2e-5,
        class_weights=class_weight_dict
    )
    
    # Detailed evaluation on test set
    print("\n=== Detailed Evaluation on Test Set ===")
    test_predictions = [pred for pred, _ in analyzer.predict(test_data['text'].tolist())]
    
    # Get unique classes that actually appear in the test data
    test_labels = test_data['label'].tolist()
    unique_classes = sorted(set(test_labels + test_predictions))
    
    # Create target names dynamically based on present classes
    label_names = {0: "Negative", 1: "Neutral", 2: "Positive"}
    target_names = [label_names[cls] for cls in unique_classes]
    
    report = classification_report(
        test_labels, 
        test_predictions,
        target_names=target_names,
        labels=unique_classes
    )
    
    print("\nClassification Report:")
    print(report)
    
    # Sample predictions - updated to handle potential index errors
    print("\nSample predictions from Test Set:")
    for i in range(min(5, len(test_data))):
        pred_index = test_predictions[i]
        true_index = test_data['label'].iloc[i]
        predicted_sentiment = label_names.get(pred_index, f"Unknown-{pred_index}")
        true_sentiment = label_names.get(true_index, f"Unknown-{true_index}")
        print(f"\nText: {test_data['text'].iloc[i][:100]}...")
        print(f"True: {true_sentiment}, Predicted: {predicted_sentiment}")
    
    # Interactive mode for user input
    print("\n=== Interactive Mode ===")
    print("Enter Arabic text to analyze sentiment (type 'exit' to quit):")
    
    while True:
        user_input = input("\nText: ")
        
        if user_input.lower() == 'exit':
            break
        
        if not user_input.strip():
            print("Please enter some text.")
            continue
        
        # Analyze user input
        prediction, confidence = analyzer.predict([user_input])[0]
        predicted_sentiment = ["Negative", "Neutral", "Positive"][prediction]
        
        print(f"Sentiment: {predicted_sentiment} (Confidence: {confidence:.2f})")
    
    print("\nAnalysis complete!")
    analyzer.cleanup()

if __name__ == "__main__":
    main()