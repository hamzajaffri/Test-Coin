import hashlib
import json
import time
import argparse
from flask import Flask, request, jsonify
import requests

# Load config
with open("config.json", "r") as f:
    CONFIG = json.load(f)

DIFFICULTY = CONFIG["DIFFICULTY"]
BLOCK_REWARD = CONFIG["BLOCK_REWARD"]

# Load genesis
with open("genesis.json", "r") as f:
    GENESIS_BLOCK = json.load(f)

# Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [GENESIS_BLOCK]
        self.pending_tx = []
        self.peers = set()

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, block):
        if self.is_valid_block(block, self.get_last_block()):
            self.chain.append(block)
            return True
        return False

    def is_valid_block(self, block, prev_block):
        if block["previous_hash"] != prev_block["hash"]:
            return False
        if not block["hash"].startswith("0" * DIFFICULTY):
            return False
        return True

    def create_block(self, nonce, miner_address):
        block = {
            "index": len(self.chain),
            "timestamp": int(time.time()),
            "transactions": self.pending_tx + [{
                "from": "network",
                "to": miner_address,
                "amount": BLOCK_REWARD
            }],
            "previous_hash": self.get_last_block()["hash"],
            "nonce": nonce,
            "hash": ""
        }
        block["hash"] = self.hash(block)
        self.pending_tx = []
        return block

    @staticmethod
    def hash(block):
        temp = block.copy()
        temp_str = json.dumps(temp, sort_keys=True)
        return hashlib.sha256(temp_str.encode()).hexdigest()

# Flask app
app = Flask(__name__)
blockchain = Blockchain()

@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(blockchain.chain)

@app.route("/height", methods=["GET"])
def get_height():
    return jsonify(len(blockchain.chain))

@app.route("/tx", methods=["POST"])
def add_tx():
    data = request.get_json()
    blockchain.pending_tx.append(data)
    return jsonify({"message": "Transaction added!"})

@app.route("/mine", methods=["POST"])
def mine():
    miner_address = request.json.get("miner")
    nonce = 0
    while True:
        block = blockchain.create_block(nonce, miner_address)
        if block["hash"].startswith("0" * DIFFICULTY):
            blockchain.add_block(block)
            return jsonify(block)
        nonce += 1

@app.route("/balance/<address>", methods=["GET"])
def get_balance(address):
    balance = 0
    for block in blockchain.chain:
        for tx in block["transactions"]:
            if tx["to"] == address:
                balance += tx["amount"]
            if tx["from"] == address:
                balance -= tx["amount"]
    return jsonify(balance)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5001)
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port)
