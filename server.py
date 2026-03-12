from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    text = data.get("text","").lower()

    if "hello" in text:
        reply = "Sure. What date would you like to book your appointment?"
    elif "pain" in text:
        reply = "I'm sorry to hear that. Would you like an urgent appointment?"
    else:
        reply = "Hello. How can I help you today?"

    return jsonify({"reply":reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)