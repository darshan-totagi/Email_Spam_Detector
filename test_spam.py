from spam_detector import predict_spam
import sys

def main():
    print("--- Email Spam Detector ---")
    print("Type 'exit' to quit.")
    
    while True:
        message = input("\nEnter the email message to check: ")
        
        if message.lower() == 'exit':
            break
            
        if not message.strip():
            continue
            
        result = predict_spam(message)
        
        if result:
            print(f"Result: {result}")

if __name__ == "__main__":
    main()
