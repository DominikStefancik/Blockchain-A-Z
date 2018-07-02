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

