import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# ফায়ারবেস ইনিশিয়ালাইজেশন (রেন্ডারের এনভায়রনমেন্ট ভ্যারিয়েবল থেকে)
firebase_config_str = os.environ.get("FIREBASE_CREDENTIALS")
if firebase_config_str:
    firebase_config_dict = json.loads(firebase_config_str)
    cred = credentials.Certificate(firebase_config_dict)
    firebase_admin.initialize_app(cred)
else:
    raise Exception("Firebase credentials not found in environment variables!")

# ফায়ারস্টোর ডাটাবেজ ক্লায়েন্ট
db = firestore.client()

# বাংলাদেশের প্রধান জেলাগুলোর লিস্ট
BANGLADESH_DISTRICTS = [
    "ঢাকা", "সিলেট", "চট্টগ্রাম", "গাজীপুর", "ময়মনসিংহ", 
    "নেত্রকোনা", "রংপুর", "বরিশাল", "খুলনা", "রাজশাহী", "কুমিল্লা"
]

def check_district_in_message(message_text):
    """মেসেজ থেকে জেলা খুঁজে বের করার ফাংশন"""
    for district in BANGLADESH_DISTRICTS:
        if district in message_text:
            return district
    return None

def save_user_to_firestore(user_id, user_name, district):
    """ফায়ারস্টোরে ইউজারের তথ্য সেভ করার ফাংশন"""
    doc_ref = db.collection('group_members').document(str(user_id))
    doc_ref.set({
        'name': user_name,
        'district': district,
        'status': 'active'
    }, merge=True)
    print(f"Firestore Saved -> Name: {user_name} | District: {district}")

# টেস্ট লজিক (এটি স্ক্রিপ্ট রান করার জন্য)
if __name__ == "__main__":
    print("Script.py is running...")
    incoming_message = "আমি সিলেট থেকে যাচ্ছি।"
    district = check_district_in_message(incoming_message)
    if district:
        save_user_to_firestore("12345", "Sabbir", district)
      
