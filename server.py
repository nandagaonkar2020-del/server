
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import dateparser

app = Flask(__name__)
CORS(app)

MONGO_URI = "mongodb+srv://clinic:b9moA024SGH2HqOf@clinic.ni0hhkz.mongodb.net/?appName=clinic"

client = MongoClient(MONGO_URI)
db = client["clinic"]
appointments = db["appointments"]


def parse_date(text):
    d = dateparser.parse(text)
    if d:
        return d.strftime("%Y-%m-%d")
    return None


@app.route("/")
def home():
    return "AI Receptionist Running"


@app.route("/book", methods=["POST"])
def book():
    data = request.json

    name = data.get("name")
    phone = data.get("phone")
    service = data.get("service")
    date_text = data.get("date")
    time = data.get("time")

    date = parse_date(date_text)

    if not date:
        return jsonify({"status":"error","message":"Invalid date"})

    exists = appointments.find_one({"date":date,"time":time})

    if exists:
        return jsonify({
        "status":"unavailable",
        "message":"Time slot already booked"
        })

    appointments.insert_one({
    "name":name,
    "phone":phone,
    "service":service,
    "date":date,
    "time":time
    })

    return jsonify({"status":"confirmed"})


@app.route("/appointments")
def all():
    data = list(appointments.find({},{"_id":0}))
    return jsonify(data)


@app.route("/delete", methods=["POST"])
def delete():
    phone = request.json["phone"]
    appointments.delete_one({"phone":phone})
    return {"status":"deleted"}


@app.route("/update", methods=["POST"])
def update():
    data = request.json

    appointments.update_one(
    {"phone":data["phone"]},
    {"$set":{
    "date":data["date"],
    "time":data["time"]
    }}
    )

    return {"status":"updated"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
