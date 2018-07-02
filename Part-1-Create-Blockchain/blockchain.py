"""
Created on Mon Jul  2 18:05:41 2018

@author: Dominik Stefancik
"""

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = [] # represents a chain of blocks
        self.create_block(proof = 1, previous_hash = "0") # creates a genesis block

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()), # timestamp when the block was mined
            "proof": proof,
            "previous_hash": previous_hash
        }
        
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1] # return the last block of the chain
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash = self.get_hash_sha256(previous_proof, new_proof)
            if self.is_hash_valid(hash):
                check_proof = True
            else:
                new_proof += 1
                
        return new_proof        

    def get_block_hash(self, block):
        # we have to encode the block for sha256 function
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self):
        for index, block in enumerate(self.chain[1:]):
            previous_block = self.chain[index - 1]
            
            # check of previous hash matches
            if block["previous_hash"] != self.get_block_hash(previous_block):
                return False
            
            previous_proof = previous_block["proof"]
            current_proof = block["proof"]
            hash = self.get_hash_sha256(previous_proof, current_proof)
            # check if proof of work is valid
            if not self.is_hash_valid(hash):
                return False
            
        return True
    
    def get_hash_sha256(self, previous_proof, current_proof):
        asymetrical_operation = current_proof**2 - previous_proof**2
        # the argument of the function here has to be a non-symetrical operation
        # e.g. new_proof + previous_proof cannot be used, because it is a symetrical operation
        # encoding is required for sha256 method
        return hashlib.sha256(str(asymetrical_operation).encode()).hexdigest()
    
    def is_hash_valid(hash):
        return hash[:4] == "0000"
        
        
