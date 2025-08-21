import os
import ecdsa
import hashlib
import base64
import json
import requests

WALLET_FILE = "wallet.json"

def generate_wallet():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    
    private_key_str = private_key.to_string().hex()
    public_key_str = public_key.to_string().hex()
    address = hashlib.sha256(public_key_str.encode()).hexdigest()
    
    wallet = {
        "private_key": private_key_str,
        "public_key": public_key_str,
        "address": address
    }
    
    with open(WALLET_FILE, "w") as f:
        json.dump(wallet, f, indent=4)
    
    print("✅ Wallet Generated!")
    print("Address:", address)
    return wallet

def load_wallet():
    if not os.path.exists(WALLET_FILE):
        return generate_wallet()
    with open(WALLET_FILE, "r") as f:
        return json.load(f)

def create_transaction(to, amount):
    wallet = load_wallet()
    tx = {
        "from": wallet["address"],
        "to": to,
        "amount": amount
    }
    return tx

def send_transaction(to, amount, node_url="http://127.0.0.1:5001"):
    tx = create_transaction(to, amount)
    res = requests.post(f"{node_url}/tx", json=tx)
    print(res.json())

if __name__ == "__main__":
    wallet = load_wallet()
    print("🔑 Your Address:", wallet["address"])
