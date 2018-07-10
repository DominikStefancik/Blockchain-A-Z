"""
Created on Fri Jul 6 2018

@author: Dominik Stefancik
"""

import datetime
import hashlib
import json
import logging

# Part 3 - Building a Cryptocurrency

# Class representing a specific blockchain containing transactions so it can represent a cryptocurrency
class Blockchain:
    
    def __init__(self):
        self.chain = [] # represents a chain of blocks
        self.transactions = [] # represents a list of transactions which are added to a newly mined block
        self.create_block(proof = 1, previous_hash = "0") # creates a genesis block

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()), # timestamp when the block was mined
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": self.transactions
        }
        
        # everytime a list of transactions is added to a new block, make sure that the very same list
        # is NOT added to the next block
        self.transactions = []
        logging.info("New block created: ", block)
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1] # return the last block of the chain
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        is_proof_valid = False
        while not is_proof_valid:
            hash = self.get_hash_sha256(previous_proof, new_proof)
            if self.is_proof_of_work_valid(hash):
                logging.info("Proof of work found. Previous proof: ", previous_proof, ", new proof: ", new_proof)
                is_proof_valid = True
            else:
                new_proof += 1
                
        return new_proof        

    def get_block_hash(self, block):
        # we have to encode the block for sha256 function
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self):
        for index, block in enumerate(self.chain[1:], start=1):
            previous_block = self.chain[index - 1]
            
            # check of previous hash matches
            if block["previous_hash"] != self.get_block_hash(previous_block):
                logging.error("Hash to a previous block doesn't match. Block index: ", block["index"],
                              ", previous hash: ", block["previous_hash"])
                return False
            
            previous_proof = previous_block["proof"]
            current_proof = block["proof"]
            hash = self.get_hash_sha256(previous_proof, current_proof)
            # check if proof of work is valid
            if not self.is_proof_of_work_valid(hash):
                logging.error("Proof of work of the block is not valid. Block index: ", block["index"],
                              ", proof of work: ", block["proof"])
                return False
            
        return True
    
    def get_hash_sha256(self, previous_proof, current_proof):
        asymetrical_operation = current_proof**2 - previous_proof**2
        # the argument of the function here has to be a non-symetrical operation
        # e.g. new_proof + previous_proof cannot be used, because it is a symetrical operation
        # encoding is required for sha256 method
        return hashlib.sha256(str(asymetrical_operation).encode()).hexdigest()
    
    def is_proof_of_work_valid(self, hash):
        return hash[:4] == "0000"
        
    def add_transaction(self, sender, receiver, coinsAmount):
        self.transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": coinsAmount
        })
            
        # return an index of a block which will contain the list of transactions
        return len(self.chain) + 1