from flask import Flask, request, jsonify
from script import process_rule_engine

app = Flask(__name__)

@app.route('/')
def home():
    return "Personal AI Bot Server is Live and Connected!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    এই রাউটে মেসেজ পাঠানো হলে রুল ইঞ্জিন সেটা প্রসেস করবে 
    এবং ফায়ারবেসে সেভ বা কুয়েরি করে উত্তর রিটার্ন করবে।
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    user_id = data.get("user_id")
    user_name = data.get("user_name")
    message_text = data.get("message")
    
    if not user_id or not message_text:
        return jsonify({"error": "user_id and message are required"}), 400
    
    # script.py থেকে রুল ইঞ্জিন কল করা
    response_message = process_rule_engine(user_id, user_name, message_text)
    
    if response_message:
        return jsonify({"status": "success", "reply": response_message})
    else:
        return jsonify({"status": "ignored", "message": "No matching rule found."})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
