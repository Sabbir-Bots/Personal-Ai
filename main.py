import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask

# ফ্লাস্ক অ্যাপ ইনিট করা (যাতে রেন্ডার একে ওয়েব সার্ভিস হিসেবে স্বীকৃতি দেয়)
app = Flask(__name__)

@app.route('/')
def home():
    return "Smart Group Assistant Bot is Running Successfully!"

# ফায়ারবেস ইনিশিয়ালাইজেশন
if os.path.exists("firebase_key.json"):
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)
else:
    firebase_config_str = os.environ.get("FIREBASE_CREDENTIALS")
    if firebase_config_str:
        firebase_config_dict = json.loads(firebase_config_str)
        cred = credentials.Certificate(firebase_config_dict)
        firebase_admin.initialize_app(cred)
    else:
        raise Exception("Firebase credentials not found in environment variables!")

db = firestore.client()

BANGLADESH_DISTRICTS = [
    "ঢাকা", "সিলেট", "চট্টগ্রাম", "গাজীপুর", "ময়মনসিংহ", 
    "নেত্রকোনা", "রংপুর", "বরিশাল", "খুলনা", "রাজশাহী", "কুমিল্লা",
    "Sylhet", "Dhaka", "Chittagong", "Gazipur", "Mymensingh", "Netrokona"
]

def check_district_in_message(message_text):
    for district in BANGLADESH_DISTRICTS:
        if district.lower() in message_text.lower():
            return district
    return None

def save_user_to_firestore(user_id, user_name, district):
    doc_ref = db.collection('group_members').document(str(user_id))
    doc_ref.set({
        'name': user_name,
        'district': district,
        'status': 'active'
    }, merge=True)
    print(f"Firestore Saved -> Name: {user_name} | District: {district}")

if __name__ == "__main__":
    # লোকাল টেস্টের জন্য
    app.run(host='0.0.0.0', port=5000)
