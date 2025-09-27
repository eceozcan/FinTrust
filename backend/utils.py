import os
import time, uuid
from dotenv import load_dotenv
import google.generativeai as genai
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.transaction import PaymentTxn, wait_for_confirmation

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

USE_API = os.getenv("USE_API", "False").lower() == "true"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ALGOD_ADDRESS = os.getenv("ALGOD_ADDRESS")
ALGOD_TOKEN = os.getenv("ALGOD_TOKEN", "")
SENDER_MNEMONIC = os.getenv("SENDER_MNEMONIC")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")

# -----------------------------
# Algorand client
# -----------------------------
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
private_key = mnemonic.to_private_key(SENDER_MNEMONIC)

# -----------------------------
# Gemini setup
# -----------------------------
if USE_API and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# -----------------------------
# Kategori & öneri
# -----------------------------
def categorize_rule_based(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["burger","kafe","yemek","starbucks","kahve"]):
        return "yiyecek", "Evde kendi kahveni hazırlayarak tasarruf edebilirsin."
    if any(w in text_lower for w in ["taxi","metro","otobüs","dolmuş"]):
        return "ulaşım", "Toplu taşıma kullanabilirsiniz."
    if any(w in text_lower for w in ["sinema","konser","netflix","oyun"]):
        return "eğlence", "Ücretsiz etkinlikleri tercih edin."
    if any(w in text_lower for w in ["eczane","doktor","hastane"]):
        return "sağlık", "Sigortanızı kontrol edin veya eczane indirimlerini kullanın."
    if any(w in text_lower for w in ["alışveriş","market","trendyol","hepsiburada"]):
        return "alışveriş", "Kampanya ve kuponları kullanın."
    return "diğer", "Harcamayı gözden geçirin."

def categorize_with_gemini(text):
    prompt = f"""
Aşağıdaki harcamayı kategoriye ayır:
"{text}"
Kategoriler: yiyecek, ulaşım, eğlence, sağlık, alışveriş, diğer
Sadece kategori adı ve kısa öneri ver, örn: 'yiyecek - kahve yerine ev yapımı alabilirsiniz.'
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    result = response.text.strip()
    if " - " in result:
        category, suggestion = result.split(" - ", 1)
    else:
        category, suggestion = result, ""
    return category.lower(), suggestion

def categorize_text(description):
    if USE_API and GEMINI_API_KEY:
        try:
            return categorize_with_gemini(description)
        except Exception as e:
            print("Gemini API hatası:", e)
            return categorize_rule_based(description)
    else:
        return categorize_rule_based(description)

# -----------------------------
# Algorand Fonksiyonları
# -----------------------------
def log_to_algorand(description, amount, category):
    note_text = f"{category}: {description} - {amount} - {uuid.uuid4()} - {int(time.time())}"
    note = note_text.encode()
    params = algod_client.suggested_params()
    txn = PaymentTxn(
        sender=SENDER_ADDRESS,
        sp=params,
        receiver=SENDER_ADDRESS,  # kendine log
        amt=0,
        note=note
    )
    signed_txn = txn.sign(private_key)
    txid = algod_client.send_transaction(signed_txn)
    wait_for_confirmation(algod_client, txid, 10)
    return txid

def get_explorer_link(txid):
    return f"https://testnet.algoexplorer.io/tx/{txid}"

# -----------------------------
# Döviz -> TL çevirici (demo, gerçek API ile güncellenebilir)
# -----------------------------
def convert_to_tl(amount, currency):
    rates = {"TL": 1, "USD": 36, "EUR": 40}  # Örnek sabit kur
    return round(amount * rates.get(currency, 1), 2)
