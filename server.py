from flask import Flask, request, jsonify
import whisper
import uuid

app = Flask(__name__)

model = whisper.load_model("base")

@app.route("/voice", methods=["POST"])
def voice():

    audio = request.files["audio"]
    filename = f"input_{uuid.uuid4()}.webm"
    audio.save(filename)

    result = model.transcribe(filename)
    text = result["text"].lower()

    if "appointment" in text:
        reply = "Sure. What date would you like to book your appointment?"
    elif "pain" in text:
        reply = "I’m sorry to hear that. Would you like to book an urgent appointment?"
    elif "cleaning" in text:
        reply = "Teeth cleaning is available. When would you like to visit?"
    else:
        reply = "Hello. How can I help you today?"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)