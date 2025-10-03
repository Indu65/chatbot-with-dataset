from flask import Flask, request, jsonify, render_template_string
from chatbot import load_dataset, chatbot_response

app = Flask(__name__)
qa_pairs = load_dataset("dataset.txt")

# Serve index.html directly
@app.route("/")
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return render_template_string(f.read())

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    reply = chatbot_response(user_message, qa_pairs)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
