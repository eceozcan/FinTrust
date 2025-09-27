import os
import base64
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
# AI & Kategori Fonksiyonları
# -----------------------------
def categorize_with_gemini(text):
    """
    Gemini API ile kategori ve öneri üretir.
    """
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

def categorize_rule_based(text):
    """
    Basit kural tabanlı kategori ve öneri
    """
    text_lower = text.lower()
    if any(w in text_lower for w in ["burger","kafe","yemek","starbucks","kahve"]):
        return "yiyecek", "Öneri: Daha ucuz alternatifleri deneyin."
    if any(w in text_lower for w in ["taxi","metro","otobüs","dolmuş"]):
        return "ulaşım", "Öneri: Toplu taşıma kullanabilirsiniz."
    if any(w in text_lower for w in ["sinema","konser","netflix","oyun"]):
        return "eğlence", "Öneri: Ücretsiz etkinlikleri tercih edin."
    if any(w in text_lower for w in ["eczane","doktor","hastane"]):
        return "sağlık", "Öneri: Sigortanızı kontrol edin veya eczane indirimlerini kullanın."
    if any(w in text_lower for w in ["alışveriş","market","trendyol","hepsiburada"]):
        return "alışveriş", "Öneri: Kampanya ve kuponları kullanın."
    return "diğer", "Öneri: Harcamayı gözden geçirin."

def categorize_text(description):
    """
    Harcama açıklamasını kategoriye ayırır.
    Gemini API varsa gerçek zamanlı, yoksa rule-based.
    Döner: category, suggestion
    """
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
    """
    Harcama bilgisini Algorand Testnet'e loglar.
    amount: Algos cinsinden (float)
    Döner: txid (string)
    """
    note = f"{category}: {description} - {amount}".encode()
    params = algod_client.suggested_params()

    txn = PaymentTxn(
        sender=SENDER_ADDRESS,
        sp=params,
        receiver=SENDER_ADDRESS,  # kendine log için
        amt=0,  # demo için transfer yok, sadece note alanı
        note=note
    )
    signed_txn = txn.sign(private_key)
    txid = algod_client.send_transaction(signed_txn)

    # İşlemin ağa düşmesini bekle
    wait_for_confirmation(algod_client, txid, 10)

    # Opsiyonel debug: txinfo yazdır
    info = algod_client.pending_transaction_info(txid)
    print("Algorand transaction info:", info)

    return txid

def get_explorer_link(txid):
    """
    Algorand Testnet Explorer linki (resmi)
    """
    return f"https://testnet.algoexplorer.io/tx/{txid}"

def get_transaction_info(txid):
    """
    TxID ile Algorand transaction bilgisini döner.
    Note alanını çözer ve explorer linki oluşturur.
    """
    info = algod_client.pending_transaction_info(txid)
    note_b64 = info.get("txn", {}).get("txn", {}).get("note")
    decoded_note = base64.b64decode(note_b64).decode() if note_b64 else None
    explorer_link = f"https://testnet.algoexplorer.io/tx/{txid}"
    return {
        "txid": txid,
        "decoded_note": decoded_note,
        "explorer_link": explorer_link,
        "raw_info": info
    }
