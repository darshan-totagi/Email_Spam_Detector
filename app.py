from flask import Flask, render_template, request, jsonify
from spam_detector import predict_spam
from mail_fetcher import fetch_latest_emails
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
        
    result = predict_spam(message)
    return jsonify({'result': result})

@app.route('/fetch_mail', methods=['POST'])
def fetch_mail():
    data = request.get_json()
    imap_server = data.get('imap_server')
    email_user = data.get('email')
    email_pass = data.get('password')
    
    if not all([imap_server, email_user, email_pass]):
        return jsonify({'error': 'Missing credentials'}), 400
        
    mail_data = fetch_latest_emails(imap_server, email_user, email_pass)
    
    if 'error' in mail_data:
        return jsonify({'error': mail_data['error']}), 500
        
    # Analyze each fetched email
    for email_item in mail_data['emails']:
        email_item['prediction'] = predict_spam(email_item['body'])
        
    return jsonify(mail_data)

if __name__ == '__main__':
    # Ensure templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True, port=5000)
