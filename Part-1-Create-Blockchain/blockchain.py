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



