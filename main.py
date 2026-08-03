import firebase_admin
from firebase_admin import credentials, db

# ১. ফায়ারবেস ইনিশিয়ালাইজেশন (আপনার ফায়ারবেস ক্রেডেনশিয়াল ফাইল দিয়ে কানেক্ট করতে হবে)
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'আপনার_ফায়ারবেসের_রিয়েলটাইম_ইউআরএল_এখানে_দিন'
})

# বাংলাদেশের কিছু প্রধান জেলার লিস্ট (যা মেসেজে খুঁজবে)
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

def save_user_data_to_firebase(user_id, user_name, district):
    """ফায়ারবেসে ইউজারের তথ্য নিজে নিজেই সেভ বা আপডেট করার ফাংশন"""
    ref = db.reference(f'group_members/{user_id}')
    ref.set({
        'name': user_name,
        'district': district,
        'status': 'active'
    })
    print(f"Saved: {user_name} - District: {district}")

# --- টেস্ট কেস ---
# কেউ মেসেজ দিলে সেটি এখানে প্রসেস হবে:
incoming_message = "সিলেট থেকে কে কে যাবেন ভাই, আমি সিলেট থাকি।"
sender_name = "Raju Ahmed"
sender_id = "raju_12345"

detected_district = check_district_in_message(incoming_message)
if detected_district:
    print(f"জেলা পাওয়া গেছে: {detected_district}")
    save_user_data_to_firebase(sender_id, sender_name, detected_district)
else:
    print("কোনো জেলা পাওয়া যায়নি।")
  
