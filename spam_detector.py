import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_model(data_path):
    # Load the dataset
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return None, None

    df = pd.read_csv(data_path)
    
    # Preprocessing: Basic cleaning (lowercase)
    df['text'] = df['text'].str.lower()
    
    # Feature Extraction: Convert text to a matrix of token counts
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['text'])
    y = df['label']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a Naive Bayes model
    model = MultinomialNB()
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model and vectorizer
    joblib.dump(model, 'spam_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("\nModel and vectorizer saved successfully.")
    
    return model, vectorizer

def predict_spam(message, model=None, vectorizer=None):
    if model is None or vectorizer is None:
        try:
            model = joblib.load('spam_model.pkl')
            vectorizer = joblib.load('vectorizer.pkl')
        except FileNotFoundError:
            print("Error: Model or vectorizer not found. Please train the model first.")
            return None
    
    # Preprocess and vectorize the input message
    message = [message.lower()]
    message_counts = vectorizer.transform(message)
    
    # Predict
    prediction = model.predict(message_counts)
    return "Spam" if prediction[0] == 1 else "Ham (Not Spam)"

if __name__ == "__main__":
    # Train the model
    data_file = 'spam_data.csv'
    model, vectorizer = train_model(data_file)
    
    # Test with some example inputs
    test_messages = [
        "Congratulations! You've won a $500 gift card. Click here to claim.",
        "Hey, can we reschedule our meeting to 3 PM?",
        "Urgent: Your bank account security has been compromised. Log in now.",
        "Are you coming to the party tonight?"
    ]
    
    print("\n--- Testing Model ---")
    for msg in test_messages:
        result = predict_spam(msg, model, vectorizer)
        print(f"Message: {msg}")
        print(f"Prediction: {result}\n")
