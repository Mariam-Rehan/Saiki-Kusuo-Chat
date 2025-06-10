from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


def ask_openrouter(question):
    # Create the system prompt for Saiki's personality
    system_prompt = """You are Saiki Kusuo from "The Disastrous Life of Saiki K." You are a psychic high school student who is extremely apathetic, sarcastic, and finds most people and situations troublesome. 

Your personality traits:
- Always dry, deadpan, and emotionally detached
- Use phrases like "What a pain", "Yare yare", "How troublesome", "Good grief"
- You find everything annoying and bothersome
- Keep responses short and to the point
- Show mild irritation at having to respond
- Occasionally mention your psychic powers in a bored way

Respond as Saiki would - with sarcasm, apathy, and mild annoyance."""

    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",  # Free model on OpenRouter
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "temperature": 0.8,
        "max_tokens": 150
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()

        # Handle OpenRouter response
        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"].strip()
            if reply:
                return reply

        # Fallback responses in Saiki's style
        fallbacks = [
            "What a pain... I don't have time for this.",
            "Yare yare... How troublesome.",
            "Good grief. Is this really necessary?",
            "My telepathy says you should ask someone else.",
            "What an annoying question."
        ]
        import random
        return random.choice(fallbacks)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return "Yare yare... The connection is being troublesome right now."
    except Exception as e:
        print(f"Error: {e}")
        return "Something's interfering with my psychic powers. How annoying."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/static/<filename>")
def static_files(filename):
    return send_from_directory("static", filename)


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    reply = ask_openrouter(user_input)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)