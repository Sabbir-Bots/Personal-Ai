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
    "Rangpur", "Dinajpur", "Gaibandha", "Kurigram", "Nilfamari", "Panchagarh", "Thakurgaon",

    # ময়মনসিংহ বিভাগ
    "ময়মনসিংহ", "নেত্রকোনা", "জামালপুর", "শেরপুর",
    "Mymensingh", "Netrokona", "Jamalpur", "Sherpur"
]

def check_district_in_message(message_text):
    """মেসেজ থেকে ৬৪ জেলার যেকোনো একটি খুঁজে বের করার রুল"""
    for district in BANGLADESH_DISTRICTS:
        if district.lower() in message_text.lower():
            return district
    return None

def process_rule_engine(user_id, user_name, message_text):
    """
    রুল ইঞ্জিন: মেসেজ বিশ্লেষণ করে ডেটাবেজে সেভ বা কুয়েরি করার মূল ফাংশন
    """
    message_lower = message_text.lower()
    
    # ১. জেলা চেক করা এবং সেভ করা (যেমন: "আমার বাসা নেত্রকোনা" বা শুধু "নেত্রকোনা")
    district = check_district_in_message(message_text)
    if district:
        doc_ref = db.collection('group_members').document(str(user_id))
        doc_ref.set({
            'name': user_name,
            'district': district,
            'status': 'active'
        }, merge=True)
        print(f"[Rule Engine Saved] User: {user_name} | District: {district}")
        return f"ধন্যবাদ {user_name}, আপনার জেলা ({district}) সফলভাবে সেভ করা হয়েছে।"

    # ২. এডমিট কার্ড সংক্রান্ত রুল
    if "এডমিট কার্ড" in message_lower or "admit card" in message_lower:
        if "পাইনি" in message_lower or "আসেনি" in message_lower or "missing" in message_lower:
            doc_ref = db.collection('group_members').document(str(user_id))
            doc_ref.set({
                'name': user_name,
                'admit_card': False
            }, merge=True)
            print(f"[Rule Engine Saved] User: {user_name} | Admit Card: False")
            return f"{user_name}, আপনার এডমিট কার্ড না পাওয়ার বিষয়টি রেকর্ড করা হয়েছে।"

    # ৩. কেউ যদি জেলা দিয়ে কাউকে খুঁজতে চায় (যেমন: "নেত্রকোনার কে কে আছো?")
    if "কে কে আছো" in message_lower or "কে আছো" in message_lower or "কেঁ কে আছেন" in message_lower:
        target_district = check_district_in_message(message_text)
        if target_district:
            users_ref = db.collection('group_members')
            query = users_ref.where('district', '==', target_district).stream()
            
            matched_names = []
            for doc in query:
                data = doc.to_dict()
                if doc.id != str(user_id):  ზი (নিজেকে বাদ দিয়ে)
                    matched_names.append(data.get('name', 'User'))
            
            if matched_names:
                names_str = ", ".join(matched_names)
                return f"@{user_name}, {target_district} থেকে এরা আছেন: {names_str}"
            else:
                return f"@{user_name}, {target_district} থেকে আর কেউ লিস্টে নেই।"

    return None

# টেস্ট লজিক
if __name__ == "__main__":
    print("Rule Engine script is running...")
    # টেস্ট মেসেজ ১: জেলা সেভ করা
    # process_rule_engine("user_001", "Rahim", "আমার বাসা নেত্রকোনা")
    
    # টেস্ট মেসেজ ২: কাউকে খোঁজা
    # response = process_rule_engine("user_002", "Karim", "নেত্রকোনার কে কে আছো?")
    # print("Bot Response:", response)
    
