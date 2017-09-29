#! /usr/bin/python

from hashlib import sha256
import pprint
import json

from block import BlockMiner
from election import Election
from transaction import RegistrationTransaction, VoteTransaction
import key_verification


class VoteChain(list):
    def __init__(self, ballot):
        """
                Lets initialize our block chain with its genesis block,
                we'll also attach the shape of the ballad to the vote.
        """
        self.ballot = ballot
        self.append({
            'name': 'GENESISBLOCK',
            'hash': sha256('GENESISBLOCK').hexdigest()
        })


if __name__ == '__main__':

    # Initialize the election
    CommanderInIceCream = Election(
        'RANK', ['ReeseWithoutASpoon', 'ChocoChipDough', 'MagicBrowny'])
    DairyQueenSecondTerm = Election('MAJORITY', ['yes', 'no'])
    StateDistrictMM = Election(
        'PICKTWO', ['PnutButter', 'CreamCKol', 'MarshMallow'])
    CountyVanilla = Election('MAJORITY', ['yes', 'no'])
    ballot = [
        CommanderInIceCream,
        DairyQueenSecondTerm,
        StateDistrictMM,
        CountyVanilla
    ]
    chain = VoteChain(ballot)

    # Register a few voters
    voters = []
    tx = []
    for i in range(0, 4):
        t = RegistrationTransaction()
        t.finalize()
        voters.append((t.signed_data, t['hash']))
        tx.append(t)

    # Have some people vote
    for v in voters:
        t = VoteTransaction(input={
            "reg_tx_hash": v[1],
            "signature": v[0],
        },
            ballot_votes=[
            {
                'ReeseWithoutASpoon': 1,
                'ChocoChipDough': 2
            },
            {'yes': 1},
            {
                'PnutButter': 1,
                'MrWriteIn': 1,
            },
            {'yes': 1}
        ])
        t.finalize()
        tx.append(t)

    # Tally the votes, mine the block
    # TODO Probably good to add the current state of the results in to the MerkleRoot / Block Hash
    chain.append(
        BlockMiner(
            tx,
            chain[-1]['hash']
        ).mine_for(chain)
    )

    print "=====================BLOCKCHAIN========================"
    print json.dumps(chain, indent=2)

    print "=====================RESULTS==========================="
    for election in chain.ballot:
        print json.dumps(election.results(), indent=2)
