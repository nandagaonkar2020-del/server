from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import random

app = Flask(__name__)
CORS(app)

# -------- Clinic Knowledge Base --------
clinic_info = {
    "name": "Om Datta Dental Clinic",
    "location": "Ghatkopar West, Mumbai",
    "timings": "Monday to Saturday 10 AM to 1 PM and 5 PM to 9 PM",
    "services": [
        "Root canal treatment",
        "Teeth cleaning",
        "Dental implants",
        "Braces treatment",
        "Tooth extraction"
    ]
}

# -------- Hindi Detection --------
def is_hindi(text):
    return re.search("[\u0900-\u097F]", text)

# -------- Intent Detection --------
def detect_intent(text):

    if any(word in text for word in ["appointment","book","visit","schedule","अपॉइंटमेंट"]):
        return "appointment"

    if any(word in text for word in ["pain","दर्द"]):
        return "pain"

    if any(word in text for word in ["clean","cleaning","सफाई"]):
        return "cleaning"

    if any(word in text for word in ["where","location","कहाँ"]):
        return "location"

    if any(word in text for word in ["time","hours","समय"]):
        return "timing"

    if any(word in text for word in ["service","treatment","services"]):
        return "services"

    return "general"

# -------- Chat Route --------
@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    text = data.get("text","").lower()

    hindi = is_hindi(text)
    intent = detect_intent(text)

    # -------- HINDI RESPONSES --------
    if hindi:

        if intent == "appointment":
            reply = "ज़रूर। आप किस तारीख को अपॉइंटमेंट लेना चाहेंगे?"

        elif intent == "pain":
            reply = "अगर आपको दांत में दर्द है तो डॉक्टर से तुरंत चेकअप करवाना अच्छा रहेगा। क्या आप अपॉइंटमेंट बुक करना चाहेंगे?"

        elif intent == "cleaning":
            reply = "हमारे क्लिनिक में दांतों की सफाई की सुविधा उपलब्ध है। आप कब आना चाहेंगे?"

        elif intent == "location":
            reply = f"हमारा क्लिनिक {clinic_info['location']} में स्थित है।"

        elif intent == "timing":
            reply = f"हमारा क्लिनिक {clinic_info['timings']} खुला रहता है।"

        elif intent == "services":
            reply = "हम रूट कैनाल, दांतों की सफाई, इम्प्लांट और ब्रेसेस जैसी सेवाएं प्रदान करते हैं।"

        else:
            reply = "नमस्ते। ओम दत्ता डेंटल क्लिनिक में आपका स्वागत है। मैं आपकी कैसे मदद कर सकता हूँ?"

        return jsonify({"reply": reply, "lang": "hi"})


    # -------- ENGLISH RESPONSES --------
    else:

        if intent == "appointment":
            reply = "Sure. What date would you like to book your appointment?"

        elif intent == "pain":
            reply = "Tooth pain should be checked by a dentist. Would you like to book an appointment?"

        elif intent == "cleaning":
            reply = "Teeth cleaning is available at our clinic. When would you like to visit?"

        elif intent == "location":
            reply = f"Our clinic is located in {clinic_info['location']}."

        elif intent == "timing":
            reply = f"Our clinic timings are {clinic_info['timings']}."

        elif intent == "services":
            reply = "We provide treatments like root canal, teeth cleaning, dental implants and braces."

        else:
            reply = f"Hello. Welcome to {clinic_info['name']}. How can I help you today?"

        return jsonify({"reply": reply, "lang": "en"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)