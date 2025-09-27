from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import categorize_text, log_to_algorand, get_explorer_link

app = Flask(__name__)
CORS(app)  # Frontend'den cross-origin istekleri kabul etmek için

# -----------------------------
# Health check
# -----------------------------
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "Server çalışıyor!"}), 200

# -----------------------------
# Add expense endpoint
# -----------------------------
@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.get_json()
    description = data.get("description")
    amount = data.get("amount")

    if not description or amount is None:
        return jsonify({"error": "description ve amount zorunludur"}), 400

    try:
        # Kategori ve öneri
        category, suggestion = categorize_text(description)

        # Algorand blockchain'e logla
        txid = log_to_algorand(description, amount, category)

        return jsonify({
            "description": description,
            "amount": amount,
            "category": category,
            "suggestion": suggestion,
            "txid": txid,
            "explorer": get_explorer_link(txid)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
