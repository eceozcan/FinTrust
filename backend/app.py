from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import categorize_text, log_to_algorand, get_explorer_link, convert_to_tl

app = Flask(__name__)
CORS(app)

# Türkçe -> İngilizce kategori çevirisi
category_map = {
    "yiyecek": "food",
    "alışveriş": "shopping",
    "ulaşım": "transportation",
    "eğlence": "entertainment",
    "fatura": "bills",
    "diğer": "other"
}

# Türkçe -> İngilizce öneri çevirisi
suggestion_map = {
    "evde yapmayı düşünebilirsiniz.": "You may consider making it at home.",
    "ihtiyaç mı, istek mi ayırın.": "Consider whether it is a need or a want.",
    "yiyecek israfını önleyin.": "Avoid wasting food.",
    "harcamalarınızı takip edin.": "Track your expenses."
}

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "Server is running!"}), 200

@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.get_json()
    description = data.get("description")
    amount = data.get("amount")
    currency = data.get("currency", "TL")

    if not description or amount is None:
        return jsonify({"error": "description and amount are required"}), 400

    try:
        # Orijinal Türkçe kategori ve öneriyi al
        original_category, original_suggestion = categorize_text(description)

        # İngilizce çeviriye dönüştür
        category = category_map.get(original_category.lower(), original_category)
        suggestion = suggestion_map.get(original_suggestion.lower(), original_suggestion)

        # TL karşılığını hesapla
        amount_tl = convert_to_tl(amount, currency)

        # Algorand blockchain'e kaydet
        txid = log_to_algorand(description, amount, category)

        return jsonify({
            "description": description,
            "amount": amount,
            "currency": currency,
            "amount_tl": amount_tl,
            "category": category,
            "suggestion": suggestion,
            "txid": txid,
            "explorer": get_explorer_link(txid)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
