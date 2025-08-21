import os
import ecdsa
import hashlib
import base64
import json
import requests

WALLET_FILE = "wallet.json"
NODE_URL = os.environ.get("NODE_URL", "http://127.0.0.1:5001")

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

def get_price():
    try:
        r = requests.get(f"{NODE_URL}/price", timeout=3)
        return float(r.json().get("price_usd", 0.0))
    except Exception:
        return 0.0

def get_balance(address):
    r = requests.get(f"{NODE_URL}/balance/{address}", timeout=5)
    return r.json()

def create_transaction(to, amount):
    wallet = load_wallet()
    tx = {
        "from": wallet["address"],
        "to": to,
        "amount": float(amount)
    }
    return tx

def send_transaction(to, amount):
    tx = create_transaction(to, amount)
    res = requests.post(f"{NODE_URL}/tx", json=tx, timeout=5)
    print(res.json())

if __name__ == "__main__":
    wallet = load_wallet()
    addr = wallet["address"]
    price = get_price()
    bal_info = get_balance(addr)
    print("🔑 Address:", addr)
    print("💰 Balance:", bal_info.get("balance"), "HMC")
    print("💵 Price (USD):", price)
    print("≈ USD Value:", bal_info.get("balance_usd"))
