# 🚀 HamzaCoin (Custom Blockchain)

HamzaCoin is a simple Proof-of-Work (PoW) blockchain built in Python — inspired by Bitcoin.

---

## 🔧 Installation
```bash
git clone https://github.com/your-username/hamzacoin.git
cd hamzacoin
pip install -r requirements.txt

▶️ Run a Node
python node.py 5001


Open another terminal and start a 2nd node:

python node.py 5002

⛏️ Start Mining
python miner.py

👛 Create Wallet
python wallet.py


This will generate a wallet file (wallet.json) with:

private_key

public_key

address

💸 Send Transaction
python -c "import wallet; wallet.send_transaction('RECEIVER_ADDRESS', 10)"

🌍 Connect Multiple Nodes

Each node can sync with others:

curl http://127.0.0.1:5001/chain

⚡ Config Options

Edit config.json:

BLOCK_REWARD → Mining reward

DIFFICULTY → Hash difficulty

MAX_SUPPLY → Total supply

BLOCK_TIME → Target block time (seconds)

✅ Features

Proof-of-Work mining

Wallet system

Transactions

Genesis block

Multi-node support

⚡ By default this runs locally. For real use, you’ll need:

Secure networking

Peer discovery

Advanced consensus

Blockchain explorer
