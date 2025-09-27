# send_note.py
from algosdk.transaction import PaymentTxn
from algosdk.v2client import algod
from algosdk import mnemonic
from dotenv import load_dotenv
import os

load_dotenv()

ALGOD_ADDRESS = os.getenv("ALGOD_ADDRESS")
ALGOD_TOKEN = os.getenv("ALGOD_TOKEN", "")
SENDER_MNEMONIC = os.getenv("SENDER_MNEMONIC")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
private_key = mnemonic.to_private_key(SENDER_MNEMONIC)

params = algod_client.suggested_params()
receiver = SENDER_ADDRESS
amount = 1000
note = "Test harcama logu".encode()

txn = PaymentTxn(SENDER_ADDRESS, params, receiver, amount, note=note)
signed_txn = txn.sign(private_key)
txid = algod_client.send_transaction(signed_txn)
print("Transaction sent with ID:", txid)
