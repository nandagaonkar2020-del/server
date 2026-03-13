from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import sqlite3
import os

app = Flask(__name__)
CORS(app)

GROQ_API = os.environ.get("GROQ_API_KEY")

DB="clinic.db"

def init_db():
    conn=sqlite3.connect(DB)
    c=conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT,
    service TEXT,
    date TEXT,
    time TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/chat",methods=["POST"])
def chat():

    text=request.json.get("text")

    prompt = f"""
You are an AI receptionist for Om Datta Dental Clinic.

Clinic details:
Name: Om Datta Dental Clinic
Location: Ghatkopar West, Mumbai
Working hours: Monday to Saturday, 10 AM to 1 PM and 5 PM to 9 PM.

IMPORTANT LANGUAGE RULE:
Users may speak in English, Hindi, or Hinglish.
Always reply in Hinglish (Hindi words written using English letters).

Examples:
User: Hello
Reply: Namaste ji, Om Datta Dental Clinic me aapka swagat hai. Main kaise madad kar sakta hoon?

User: Mujhe tooth pain hai
Reply: Agar aapko tooth pain hai to dentist se check karwana zaroori hai. Kya aap appointment book karna chahenge?

User: I want appointment
Reply: Zaroor. Aap kis date aur time par appointment lena chahenge?

Your job is to help patients with:
- booking appointments
- clinic timings
- available services
- clinic location

When booking an appointment follow this flow:
1. Ask patient's name.
2. Ask phone number.
3. Ask which dental service they need (cleaning, root canal, braces, etc).
4. Ask preferred date and time.
5. Confirm appointment politely.

Rules:
- Be friendly and polite.
- Speak like a human receptionist.
- Keep responses short and conversational.
- Always respond in Hinglish.
"""

    response=requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization":f"Bearer {GROQ_API}",
            "Content-Type":"application/json"
        },
        json={
            "model":"llama3-8b-8192",
            "messages":[
                {"role":"system","content":prompt},
                {"role":"user","content":text}
            ]
        }
    )

    reply=response.json()["choices"][0]["message"]["content"]

    return jsonify({"reply":reply})
    

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)