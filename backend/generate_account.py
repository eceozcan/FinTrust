from algosdk import account, mnemonic

private_key, address = account.generate_account()
mn = mnemonic.from_private_key(private_key)

print("Address:", address)
print("Mnemonic (25 words):", mn)
