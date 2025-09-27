from algosdk.v2client import algod
import base64

ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

txid = input("TxID gir: ")
info = client.pending_transaction_info(txid)
print(info)

note_b64 = info.get("txn", {}).get("txn", {}).get("note")
if note_b64:
    print("Decoded note:", base64.b64decode(note_b64).decode())
