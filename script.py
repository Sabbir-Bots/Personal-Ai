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

# বাংলাদেশের ৬৪টি জেলার পূর্ণাঙ্গ লিস্ট (বাংলা এবং ইংরেজি নামসহ)
BANGLADESH_DISTRICTS = [
    # ঢাকা বিভাগ
    "ঢাকা", "গাজীপুর", "নারায়ণগঞ্জ", "টাঙ্গাইল", "কিশোরগঞ্জ", "মানিকগঞ্জ", 
    "মুন্সিগঞ্জ", "রাজবাড়ী", "মাদারীপুর", "ফরিদপুর", "শরিয়তপুর",
    "Dhaka", "Gazipur", "Narayanganj", "Tangail", "Kishoreganj", "Manikganj", 
    "Munshiganj", "Rajbari", "Madaripur", "Faridpur", "Shariatpur",

    # চট্টগ্রাম বিভাগ
    "চট্টগ্রাম", "কক্সবাজার", "রাঙ্গামাটি", "বান্দরবান", "খাগড়াছড়ি", 
    "নোয়াখালী", "লক্ষ্মীপুর", "ফেনী", "কুমিল্লা", "ব্রাহ্মণবাড়িয়া", "চাঁদপুর",
    "Chittagong", "Cox's Bazar", "Rangamati", "Bandarban", "Khagrachhari", 
    "Noakhali", "Lakshmipur", "Feni", "Comilla", "Brahmanbaria", "Chandpur",

    # রাজশাহী বিভাগ
    "রাজশাহী", "বগুড়া", "পাবনা", "সিরাজগঞ্জ", "নওগাঁ", "নাটোর", "চাঁপাইনবাবগঞ্জ", "জয়পুরহাট",
    "Rajshahi", "Bogura", "Pabna", "Sirajganj", "Naogaon", "Natore", "Chapainawabganj", "Joypurhat",

    # খুলনা বিভাগ
    "খুলনা", "যশোর", "সাতক্ষীরা", "মেহেরপুর", "নড়াইল", "চুয়াডাঙ্গা", "কুষ্টিয়া", "মাগুরা", "বাগেরহাট", "ঝিনাইদহ",
    "Khulna", "Jessore", "Satkhira", "Meherpur", "Narail", "Chuadanga", "Kushtia", "Magura", "Bagerhat", "Jhenaidah",

    # সিলেট বিভাগ
    "সিলেট", "মৌলভীবাজার", "হবিগঞ্জ", "সুনামগঞ্জ",
    "Sylhet", "Moulvibazar", "Habiganj", "Sunamganj",

    # বরিশাল বিভাগ
    "বরিশাল", "ভোলা", "পটুয়াখালী", "পিরোজপুর", "বরগুনা", "ঝালকাঠি",
    "Barisal", "Bhola", "Patuakhali", "Pirojpur", "Barguna", "Jhalokati",

    # রংপুর বিভাগ
    "রংপুর", "দিনাজপুর", "বগুড়া", "গাইবান্ধা", "কুড়িগ্রাম", "নীলফামারী", "পঞ্চগড়", "ঠাকুরগাঁও",
    "Rangpur", "Dinajpur", "Gaibandha", "Kurigram", "Nilphamari", "Panchagarh", "Thakurgaon",

    # ময়মনসিংহ বিভাগ
    "ময়মনসিংহ", "নেত্রকোনা", "জামালপুর", "শেরপুর",
    "Mymensingh", "Netrokona", "Jamalpur", "Sherpur"
]

def check_district_in_message(message_text):
    """মেসেজ থেকে ৬৪ জেলার যেকোনো একটি খুঁজে বের করার ফাংশন"""
    for district in BANGLADESH_DISTRICTS:
        if district.lower() in message_text.lower():
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

# টেস্ট লজিক
if __name__ == "__main__":
    print("Script.py with 64 districts is ready...")
    incoming_message = "আমার বাসা পঞ্চগড়।"
    district = check_district_in_message(incoming_message)
    if district:
        save_user_to_firestore("12345", "Sabbir", district)
        
