from flask import Flask, request, jsonify
from flask_cors import CORS

from appointment import create_appointment, cancel_appointment
from date_parser import parse_date

app = Flask(__name__)
CORS(app)


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
        return jsonify({
            "status": "error",
            "message": "Invalid date"
        })

    result = create_appointment(name, phone, service, date, time)

    return jsonify(result)


@app.route("/cancel", methods=["POST"])
def cancel():

    data = request.json

    phone = data.get("phone")

    result = cancel_appointment(phone)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)