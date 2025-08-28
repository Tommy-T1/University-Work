import os
import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from spacy.pipeline import TextCategorizer
import random

class ArabicSentimentAnalyzer:
    def __init__(self, model_dir='models', num_labels=3):
        """Initialize the analyzer with spaCy model for Arabic text"""
        self.model_dir = model_dir
        self.num_labels = num_labels
        
        # Create model directory if it doesn't exist
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        try:
            # Create a blank Arabic spaCy model or load existing
            self.nlp = spacy.blank("ar")
            
            # Add text categorizer to the pipeline
            if "textcat" not in self.nlp.pipe_names:
                self.textcat = self.nlp.add_pipe("textcat")
                
                # Add sentiment categories
                self.textcat.add_label("NEGATIVE")
                self.textcat.add_label("NEUTRAL")
                self.textcat.add_label("POSITIVE")
            else:
                self.textcat = self.nlp.get_pipe("textcat")
                
            print("SpaCy model initialized successfully")
            
        except Exception as e:
            print(f"Error initializing model: {str(e)}")
            raise

    def train_and_evaluate(self, train_texts, train_labels, test_texts, test_labels, epochs=10, batch_size=16,
                         learning_rate=0.001, class_weights=None):
        """Train and evaluate the model using spaCy"""
        # Convert labels to spaCy format (0=NEG, 1=NEU, 2=POS)
        label_dict = {0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"}
        
        # Prepare training data
        train_data = []
        for text, label in zip(train_texts, train_labels):
            cats = {"NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0}
            cats[label_dict[label]] = 1
            train_data.append((text, {"cats": cats}))
        
        # Set up optimizer
        optimizer = self.nlp.begin_training()
        
        # Training settings
        if class_weights:
            # Apply class weights in loss calculation
            loss_weights = {"textcat": class_weights}
        else:
            loss_weights = {}
        
        # Create Examples
        train_examples = []
        for text, annotations in train_data:
            doc = self.nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            train_examples.append(example)
        
        # Start training
        print(f"Training the model...")
        for epoch in range(epochs):
            # Shuffle the training data
            random.shuffle(train_examples)
            losses = {}
            
            # Batch the examples and iterate over them
            batches = minibatch(train_examples, size=compounding(4., 32., 1.001))
            for batch in batches:
                self.nlp.update(
                    batch,
                    drop=0.2,
                    losses=losses,
                    sgd=optimizer
                )
            
            # Evaluate on training data
            train_accuracy = self.evaluate_spacy(train_examples[:min(100, len(train_examples))])
            
            print(f"\nEpoch {epoch+1}/{epochs}")
            print(f"Losses: {losses}")
            print(f"Train accuracy: {train_accuracy:.4f}")
        
        # Save the final model
        self.save_model(os.path.join(self.model_dir, 'arabic_sentiment_model'))
        
        # Prepare test data
        test_examples = []
        for text, label in zip(test_texts, test_labels):
            cats = {"NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0}
            cats[label_dict[label]] = 1
            doc = self.nlp.make_doc(text)
            example = Example.from_dict(doc, {"cats": cats})
            test_examples.append(example)
            
        test_accuracy = self.evaluate_spacy(test_examples)
        print(f"\nFinal test accuracy: {test_accuracy:.4f}")
        
        return test_accuracy

    def evaluate_spacy(self, examples):
        """Evaluate the model on examples"""
        correct = 0
        for example in examples:
            pred = self.nlp(example.text)
            # Fix: use example.reference.cats instead of get_reference
            gold_cats = example.reference.cats
            pred_cat = max(pred.cats.items(), key=lambda x: x[1])[0]
            gold_cat = max(gold_cats.items(), key=lambda x: x[1])[0]
            if pred_cat == gold_cat:
                correct += 1
        return correct / len(examples) if examples else 0

    def predict(self, texts):
        """Make predictions for a list of texts"""
        predictions = []
        
        for text in texts:
            doc = self.nlp(text)
            scores = doc.cats
            
            # Convert scores to numeric labels (0=NEG, 1=NEU, 2=POS)
            pred_label = -1
            confidence = 0
            
            if scores["NEGATIVE"] >= scores["NEUTRAL"] and scores["NEGATIVE"] >= scores["POSITIVE"]:
                pred_label = 0
                confidence = scores["NEGATIVE"]
            elif scores["NEUTRAL"] >= scores["NEGATIVE"] and scores["NEUTRAL"] >= scores["POSITIVE"]:
                pred_label = 1
                confidence = scores["NEUTRAL"]
            else:
                pred_label = 2
                confidence = scores["POSITIVE"]
            
            predictions.append((pred_label, confidence))
        
        return predictions

    def save_model(self, path):
        """Save spaCy model"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            self.nlp.to_disk(path)
            print(f"✅ Model saved to {path}")
            return True
        except Exception as e:
            print(f"⚠️ Error saving model: {str(e)}")
            return False
        
    def load_model(self, path):
        """Load spaCy model"""
        if not os.path.exists(path):
            print(f"⚠️ Model directory not found: {path}")
            return False
        
        try:
            self.nlp = spacy.load(path)
            self.textcat = self.nlp.get_pipe("textcat")
            print(f"✅ Model loaded from {path}")
            return True
        except Exception as e:
            print(f"⚠️ Error loading model: {str(e)}")
            return False

    def cleanup(self):
        """Release resources if needed"""
        pass  # spaCy handles memory management well, no explicit cleanup needed