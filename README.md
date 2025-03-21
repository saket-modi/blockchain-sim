# BlockChain Simulation
This is a simple project that utilizes Python3 to create and maintain a blockchain in a JSON file, using the Proof-of-Work algorithm. The code (in main.py) has the following features:
- Keep updating the blockchain by reading data from chain.json - data is not overwritten for future iterations of running main.py, instead, it is added on to the JSON file while maintaining formatting;
- BlockChain validation: detects any abnormalities by checking the assigned hash and previous hash of each block (maintains order).

## Future
- Addition of a "BlockChain Correction" feature. Identifies chain tampering (loss in hash integrity) and fixes it according to blockString values (index, transactions, nonces, etc.).