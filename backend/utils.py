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
# Categorization & Suggestions (English)
# -----------------------------
def categorize_rule_based(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["burger", "cafe", "food", "coffee", "starbucks"]):
        return "food", "You could save money by preparing it at home."
    if any(w in text_lower for w in ["taxi", "metro", "bus"]):
        return "transportation", "Consider using public transport."
    if any(w in text_lower for w in ["cinema", "concert", "netflix", "game"]):
        return "entertainment", "Look for free or low-cost alternatives."
    if any(w in text_lower for w in ["pharmacy", "doctor", "hospital"]):
        return "health", "Check your insurance or explore discounts."
    if any(w in text_lower for w in ["shopping", "market", "amazon"]):
        return "shopping", "Consider comparing prices or using coupons."
    return "other", "Review whether this expense is necessary."

def categorize_with_gemini(text):
    prompt = f"""
Classify the expense below:
"{text}"
Categories: food, transportation, entertainment, health, shopping, other
Respond with: category - suggestion
Example: food - You could save money by preparing it at home.
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
            print("Gemini API error:", e)
            return categorize_rule_based(description)
    else:
        return categorize_rule_based(description)

# -----------------------------
# Algorand Functions
# -----------------------------
def log_to_algorand(description, amount, category):
    note_text = f"{category}: {description} - {amount} - {uuid.uuid4()} - {int(time.time())}"
    note = note_text.encode()
    params = algod_client.suggested_params()
    txn = PaymentTxn(
        sender=SENDER_ADDRESS,
        sp=params,
        receiver=SENDER_ADDRESS,  # logging to self
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
# Currency → TL (sample conversion)
# -----------------------------
def convert_to_tl(amount, currency):
    rates = {"TL": 1, "USD": 36, "EUR": 40}  # Example static rates
    return round(amount * rates.get(currency, 1), 2)
