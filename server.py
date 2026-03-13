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

@app.route("/")
def home():
    return "AI Dental Receptionist API running"


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data=request.json
        text=data.get("text","")

        prompt="""
You are an AI receptionist for Om Datta Dental Clinic.

Clinic details:
Name: Om Datta Dental Clinic
Location: Ghatkopar West Mumbai
Timings: Monday to Saturday 10 AM to 1 PM and 5 PM to 9 PM

IMPORTANT:
User may speak English, Hindi or Hinglish.

Always reply in Hinglish (Hindi written in English letters).

Example replies:

User: hello
Reply: Namaste ji Om Datta Dental Clinic me aapka swagat hai. Main kaise madad kar sakta hoon?

User: mujhe tooth pain hai
Reply: Agar aapko tooth pain hai to dentist se check karwana zaroori hai. Kya aap appointment book karna chahenge?

User: I want appointment
Reply: Zaroor. Aap kis date aur time par appointment lena chahenge?

Keep answers short and natural like a receptionist.
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

        print("GROQ RESPONSE:",response.text)

        data=response.json()

        if "choices" not in data:
            return jsonify({
                "reply":"AI service error",
                "debug":data
            })

        reply=data["choices"][0]["message"]["content"]

        return jsonify({"reply":reply})


    except Exception as e:

        return jsonify({
            "reply":"Server error occurred",
            "error":str(e)
        })


if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)