import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# ১. ফায়ারবেস ইনিশিয়ালাইজেশন (রেন্ডার বা লোকাল এনভায়রনমেন্ট হ্যান্ডলিং)
# যদি লোকাল পিসিতে থাকেন তবে 'firebase_key.json' ফাইল থেকে পড়বে, 
# আর রেন্ডারে থাকলে এনভায়রনমেন্ট ভ্যারিয়েবল থেকে পড়বে।
if os.path.exists("firebase_key.json"):
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)
else:
    # রেন্ডারের এনভায়রনমেন্ট ভ্যারিয়েবল থেকে জেসন ডাটা লোড করার সিস্টেম
    firebase_config_str = os.environ.get("FIREBASE_CREDENTIALS")
    if firebase_config_str:
        firebase_config_dict = json.loads(firebase_config_str)
        cred = credentials.Certificate(firebase_config_dict)
        firebase_admin.initialize_app(cred)
    else:
        raise Exception("Firebase credentials not found in environment variables or local files!")

# ফায়ারস্টোর ডাটাবেজ ক্লায়েন্ট ইনিট করা
db = firestore.client()

# বাংলাদেশের প্রধান জেলাগুলোর লিস্ট
BANGLADESH_DISTRICTS = [
    "ঢাকা", "সিলেট", "চট্টগ্রাম", "গাজীপুর", "ময়মনসিংহ", 
    "নেত্রকোনা", "রংপুর", "বরিশাল", "খুলনা", "রাজশাহী", "কুমিল্লা",
    "Sylhet", "Dhaka", "Chittagong", "Gazipur", "Mymensingh", "Netrokona"
]

def check_district_in_message(message_text):
    """মেসেজ থেকে জেলা খুঁজে বের করার ফাংশন"""
    for district in BANGLADESH_DISTRICTS:
        # কেস-ইনসেন্সিটিভ খোঁজার জন্য লোয়ারকেস করে চেক করতে পারেন
        if district.lower() in message_text.lower():
            return district
    return None

def save_user_to_firestore(user_id, user_name, district):
    """ফায়ারস্টোরে ইউজারের তথ্য সেভ বা আপডেট করার ফাংশন"""
    doc_ref = db.collection('group_members').document(str(user_id))
    doc_ref.set({
        'name': user_name,
        'district': district,
        'status': 'active'
    }, merge=True)
    print(f"Firestore Saved -> Name: {user_name} | District: {district}")

# --- টেস্ট বা রানিং লজিক ---
if __name__ == "__main__":
    # গ্রুপ থেকে পাওয়া কোনো একটি মেসেজ এখানে টেস্ট করা হচ্ছে
    incoming_message = "সিলেট থেকে কে কে যাবেন ভাই, আমি সিলেট থাকি।"
    sender_name = "Raju Ahmed"
    sender_id = "raju_12345"

    detected_district = check_district_in_message(incoming_message)
    if detected_district:
        print(f"জেলা পাওয়া গেছে: {detected_district}")
        save_user_to_firestore(sender_id, sender_name, detected_district)
    else:
        print("কোনো জেলা পাওয়া যায়নি।")
