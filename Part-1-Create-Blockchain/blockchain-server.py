"""
Created on Mon Jul 2 2018

@author: Dominik Stefancik
"""

from flask import Flask, jsonify
from blockchain import Blockchain

# Part 2 - Mining our Blockchain

blockchain = Blockchain()

# creates a new server
app = Flask(__name__)

@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block["proof"])
    previous_hash = blockchain.get_block_hash(previous_block)
    
    new_block = blockchain.create_block(proof, previous_hash)
    response = {
            "message": "Congratulations, you just mined a block!",
            "index": new_block["index"],
            "timestamp": new_block["timestamp"],
            "proof": new_block["proof"],
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

app.run(host = "0.0.0.0", port = 5000)
