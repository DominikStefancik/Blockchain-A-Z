"""
Created on Sat Jul 14 2018

@author: Dominik Stefancik
"""

from flask import Flask, jsonify
from hadcoin import Blockchain
from uuid import uuid4

# Part 2 - Mining our Blockchain
# here we need to distinguish two types of transactions:
#   1. transactions which go to the newly mined block
#   2. transactions for the miner as a reward for mining a new block

# the address is needed for the miner to receive Hadcoins for mining a block
node_address = str(uuid4()).replace("-", "")

blockchain = Blockchain()

# creates a new server
app = Flask(__name__)

@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block["proof"])
    
    # the receiver is the miner who receives reward for mining a block
    # amount is the amount of Hadcoins the receiver gets for mining the block
    blockchain.add_transaction(sender = node_address, receiver = "Dominik", amount = 1)
    previous_hash = blockchain.get_block_hash(previous_block)
    
    new_block = blockchain.create_block(proof, previous_hash)
    response = {
            "message": "Congratulations, you just mined a block!",
            "index": new_block["index"],
            "timestamp": new_block["timestamp"],
            "proof": new_block["proof"],
            "transactions": new_block["transactions"],
            "previous_hash": new_block["previous_hash"]
    }
    
    return jsonify(response), 200 # return response in a json format + http status code


@app.route("/blockchain", methods=["GET"])
def get_blockchain():
    response = {
        "blockchain": blockchain.chain,
        "length": len(blockchain.chain)         
    }
    
    return jsonify(response), 200

@app.route("/is_valid", methods=["GET"])
def is_valid_blockchain():
    response = {
        "isValid": blockchain.is_chain_valid(),        
    }
    
    return jsonify(response), 200

# adding a transaction to a newly mined block
@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    transactionData = request.get_json()
    transaction_keys = ["sender", "receiver", "amount"]
    if not all (key in  transactionData for key in transaction_keys):
        return  "Some elements of transaction are missing", 400
    
    block_index = blockchain.add_transaction(
            transactionData["sender"], transactionData["receiver"], transactionData["amount"])
    response = {"message": f"Transaction added to the block with index {block_index}"}
    
    return jsonify(response), 201


app.run(host = "0.0.0.0", port = 5000)