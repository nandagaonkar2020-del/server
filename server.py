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

    prompt=f"""
You are an AI dental clinic receptionist.

Clinic name: Om Datta Dental Clinic
Location: Ghatkopar West Mumbai
Languages: Hindi and English.

If user speaks Hindi respond in Hindi.
If English respond in English.

Help patients with:
- appointment booking
- clinic timings
- services
- location
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