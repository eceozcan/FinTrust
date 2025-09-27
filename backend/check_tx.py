# # check_tx.py
# from algosdk.v2client import algod
# import base64

# ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
# ALGOD_TOKEN = ""   # algonode için boş bırak

# client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

# txid = input("TxID gir: ").strip()
# info = client.pending_transaction_info(txid)
# print("\nRAW INFO:\n", info)

# note_b64 = info.get("txn", {}).get("txn", {}).get("note")
# if note_b64:
#     try:
#         note = base64.b64decode(note_b64).decode("utf-8", errors="ignore")
#     except Exception as e:
#         note = f"Note decode hatası: {e}"
# else:
#     note = None

# print("\nDecoded note:", note)
# print("Confirmed round:", info.get("confirmed-round"))


from utils import get_transaction_info

txid = "YTV3CQ66GJW35HQQBOBIZYTQU5T6B7IO572BA267PXY7DDYDQMSQ"
info = get_transaction_info(txid)
print(info.get("decoded_note", "Note yok"))  # Note alanını görürsün
print(info)  # Tüm transaction bilgisi
