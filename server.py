from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "clinic.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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


@app.route("/book", methods=["POST"])
def book():

    data = request.json

    name = data.get("name")
    phone = data.get("phone")
    service = data.get("service")
    date = data.get("date")
    time = data.get("time")

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # check double booking
    c.execute(
        "SELECT * FROM appointments WHERE date=? AND time=?",
        (date, time)
    )

    exists = c.fetchone()

    if exists:
        conn.close()
        return jsonify({
            "status": "unavailable",
            "message": "Yeh time slot already booked hai. Please doosra time choose kare."
        })

    c.execute(
        "INSERT INTO appointments(name,phone,service,date,time) VALUES(?,?,?,?,?)",
        (name, phone, service, date, time)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "confirmed",
        "message": "Appointment successfully book ho gaya."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)