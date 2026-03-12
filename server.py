from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime
import re

app = Flask(__name__)
CORS(app)

DB="clinic.db"

# ---------- DATABASE INIT ----------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT,
    email TEXT,
    address TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    service TEXT,
    date TEXT,
    time TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS chats(
    id INTEGER PRIMARY KEY,
    message TEXT,
    response TEXT,
    timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- LANGUAGE DETECT ----------
def is_hindi(text):
    return re.search("[\u0900-\u097F]", text)

# ---------- CHECK SLOT ----------
def is_slot_available(date,time):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
    "SELECT * FROM appointments WHERE date=? AND time=?",
    (date,time)
    )

    result = c.fetchone()
    conn.close()

    return result is None


# ---------- CHAT ROUTE ----------
@app.route("/chat",methods=["POST"])
def chat():

    data = request.json
    text = data.get("text","").lower()

    hindi = is_hindi(text)

    if "appointment" in text or "अपॉइंटमेंट" in text:

        reply = "Please tell your name."

    elif "name" in text:

        reply = "Please provide your phone number."

    elif "phone" in text:

        reply = "Which service do you need? Cleaning, root canal or braces?"

    elif "clean" in text or "सफाई" in text:

        reply = "What date would you like to visit?"

    elif "tomorrow" in text:

        date = str(datetime.date.today()+datetime.timedelta(days=1))
        time="18:00"

        if is_slot_available(date,time):
            reply = f"Your appointment is available tomorrow at 6 pm. Should I confirm?"
        else:
            reply = "That slot is already booked. Please choose another time."

    else:

        if hindi:
            reply="नमस्ते। ओम दत्ता डेंटल क्लिनिक में आपका स्वागत है।"
        else:
            reply="Hello welcome to Om Datta Dental Clinic. How can I help you?"

    conn=sqlite3.connect(DB)
    c=conn.cursor()

    c.execute(
    "INSERT INTO chats(message,response,timestamp) VALUES(?,?,?)",
    (text,reply,str(datetime.datetime.now()))
    )

    conn.commit()
    conn.close()

    return jsonify({"reply":reply,"lang":"hi" if hindi else "en"})


if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)