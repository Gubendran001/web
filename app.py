import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None

@app.route("/")
def index():
    return render_template("index.html", chatbot_title="Web Development AI")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "Please enter a study question."}), 400

    if not client:
        return jsonify({"reply": "Gemini API key is not configured. Add it to the .env file."}), 500

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f"{SYSTEM_PROMPT}\\n\\nStudent question: {message}"
        )
        return jsonify({"reply": response.text or "I could not generate a response."})
    except Exception:
        return jsonify({"reply": "Something went wrong while contacting Gemini. Please check your API key and configuration."}), 500

if __name__ == "__main__":
    app.run()
