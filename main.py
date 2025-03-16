import json
import time
import hashlib
import os
def isChainValid(blockchain):
    for i in range(1, len(blockchain)):
        current = blockchain[i]
        previous = blockchain[i - 1]
        b = block(current["index"], current["transactions"], current["previous_hash"])
        b.timestamp = current["timestamp"]
        b.nonce = current["nonce"]
        # Recreate hash of the current block
        recalculated_hash = b.calculateHash()

        # Check hash integrity
        if current["hash"] != recalculated_hash:
            print(f"Block {i} has invalid hash!")
            return False

        # Check chain linkage
        if current["previous_hash"] != previous["hash"]:
            print(f"Block {i} has invalid previous hash linkage!")
            return False

    print("Blockchain is valid!")
    return True

class block:
    def __init__(parent, index, transactions, previous_hash):
        parent.index = index
        parent.timestamp = time.time() # From time lib
        parent.transactions = transactions
        parent.previous_hash = previous_hash
        parent.nonce = 0
        parent.hash = ""

    def toDictionary(parent):
        return {
            "index": parent.index,
            "timestamp": parent.timestamp,
            "transactions": parent.transactions,
            "previous_hash": parent.previous_hash,
            "nonce": parent.nonce,
            "hash": parent.hash
        }

    def calculateHash(parent):
        blockString = json.dumps({
            "index": parent.index,
            "timestamp": parent.timestamp,
            "transactions": parent.transactions,
            "previous_hash": parent.previous_hash,
            "nonce": parent.nonce
        }, sort_keys = True).encode()
        return hashlib.sha256(blockString).hexdigest()
    
    def mineBlock(parent, difficulty):
        print(f"Mining block {parent.index}...")
        start = time.time()
        target = "0" * difficulty # String multiplication == "0" * 2 = "00"
        while True:
            parent.hash = parent.calculateHash()
            if parent.hash.startswith(target):
                break
            else:
                parent.nonce += 1
        end = time.time()
        elapsed = end - start
        print(f"Block mined: {parent.hash}")
        print(f"Time taken: {elapsed:.2f} seconds")

prev = 0
index = 0

# Check existing JSON validity before execution
if os.stat("chain.json").st_size == 0:
    print(f"chain.json is empty. Creating a new blockchain...")
    loaded = []
else:
    with open("chain.json", "r") as file:
        loaded = json.load(file)
    print(f"Loaded blockchain from local file: chain.json")
    lastBlock = loaded[-1]
    index = lastBlock["index"] + 1
    prev = lastBlock["hash"]

if (isChainValid(loaded) or not loaded):
    difficulty = int(input("Enter desired difficulty: "))

    while True:
        transactions = input("Enter transaction details: ")
        if transactions == "#":
            break
        b = block(index, transactions, prev)
        b.mineBlock(difficulty)
        prev = b.hash
        loaded.append(b.toDictionary())
        index += 1
    with open("chain.json", "w") as file:
            json.dump(loaded, file, indent = 4)