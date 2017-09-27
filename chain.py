#! /usr/bin/python

from block import BlockMiner
from hashlib import sha256
import pprint


class BlockChain(list):
    def __init__(self):
        self.append({
            'name': 'GENESISBLOCK',
            'hash': sha256('GENESISBLOCK').hexdigest()
        })


transactions = ['vote1', 'vote2', 'vote3']
chain = BlockChain()

chain.append(
    BlockMiner(
        transactions,
        chain[-1]['hash']
    ).mine()
)

chain.append(
    BlockMiner(
        transactions,
        chain[-1]['hash']
    ).mine()
)

pprint.pprint(chain)
