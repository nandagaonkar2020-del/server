from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Detect Hindi characters
def is_hindi(text):
    return re.search("[\u0900-\u097F]", text)

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    text = data.get("text","").lower()

    hindi = is_hindi(text)

    # ---------------- HINDI RESPONSES ----------------
    if hindi:

        if "नमस्ते" in text or "hello" in text:
            reply = "नमस्ते। ओम दत्ता डेंटल क्लिनिक में आपका स्वागत है। मैं आपकी कैसे मदद कर सकता हूँ?"

        elif "दर्द" in text:
            reply = "क्या आपको दांत में दर्द हो रहा है? अगर आप चाहें तो मैं आपके लिए अपॉइंटमेंट बुक कर सकता हूँ।"

        elif "अपॉइंटमेंट" in text:
            reply = "आप किस तारीख और समय पर अपॉइंटमेंट लेना चाहेंगे?"

        elif "सफाई" in text or "क्लीनिंग" in text:
            reply = "दांतों की सफाई हमारे क्लिनिक में उपलब्ध है। आप कब आना चाहेंगे?"

        elif "कहाँ" in text or "लोकेशन" in text:
            reply = "हमारा क्लिनिक घाटकोपर वेस्ट, मुंबई में स्थित है।"

        elif "समय" in text or "टाइम" in text:
            reply = "हम सोमवार से शनिवार सुबह 10 से 1 और शाम 5 से 9 बजे तक खुले रहते हैं।"

        else:
            reply = "मैं आपकी मदद करने के लिए यहाँ हूँ। क्या आप अपॉइंटमेंट बुक करना चाहते हैं?"

        return jsonify({"reply": reply, "lang": "hi"})


    # ---------------- ENGLISH RESPONSES ----------------
    else:

        if "hello" in text or "hi" in text:
            reply = "Hello. Welcome to Om Datta Dental Clinic. How can I help you today?"

        elif "pain" in text or "tooth pain" in text:
            reply = "I’m sorry to hear that. Would you like to book an urgent dental appointment?"

        elif "appointment" in text or "book" in text:
            reply = "Sure. What date and time would you like to book your appointment?"

        elif "cleaning" in text:
            reply = "Teeth cleaning is available at our clinic. When would you like to visit?"

        elif "location" in text or "where" in text:
            reply = "Our clinic is located in Ghatkopar West, Mumbai."

        elif "time" in text or "hours" in text:
            reply = "Our clinic is open Monday to Saturday from 10 AM to 1 PM and 5 PM to 9 PM."

        else:
            reply = "Hello. How can I help you today?"

        return jsonify({"reply": reply, "lang": "en"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)