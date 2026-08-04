from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)

if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_id = data.get('user_id')
    user_name = data.get('user_name', 'User')
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({"status": "ignored", "message": "Empty message"}), 400

    message_lower = message.lower()
    
    # 1. Memory Save Logic
    if "home" in message_lower or "live" in message_lower:
        db.collection("group_members").document(str(user_id)).set({
            "user_name": user_name,
            "location": message,
            "last_active": firestore.SERVER_TIMESTAMP
        }, merge=True)
        
        ai_response = f"Thanks {user_name}, your location has been successfully saved."
        return jsonify({"status": "success", "reply": ai_response})

    # 2. Memory Recall Logic
    elif "where" in message_lower and "home" in message_lower:
        user_ref = db.collection("group_members").document(str(user_id)).get()
        if user_ref.exists:
            user_data = user_ref.to_dict()
            loc = user_data.get('location', 'I do not remember')
            ai_response = f"According to my memory, {loc}"
        else:
            ai_response = "I don't have any saved data about you yet. Tell me where you live!"
        
        return jsonify({"status": "success", "reply": ai_response})

    else:
        ai_response = f"I understand your point, {user_name}. Processing further..."
        return jsonify({"status": "success", "reply": ai_response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
