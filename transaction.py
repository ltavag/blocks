#! /usr/bin/python

import json
from hashlib import sha256
import key_verification
import uuid

"""
	There are two types of transactions that should be allowed. 
	
	1. Voter registration
			Here the input transaction ID should always be signed by a trusted 
			source. The public key we can accept for input is going to be 
			baked in to our code for now. 
	
			{
				"tx":
							"tx_hash",
				"input":
						{
									"register_id":"",
									"signed_register_id":""
						},
				"out":
						{
									"pub_key":
						}
			}

	2. Voting
			The input transaction ID should be that of voter registration. 
			The output will just be a JSON of the vote

			{
				"tx":
							"tx_hash",
				"input":
						{
								"reg_tx_hash"
								"signature"
						},
				"ballot_votes":
						[	

						]	
			}
"""


class InvalidTransactionException(Exception):
    def __init__(self, message):
        self.message = message


class Transaction(dict):
    def __init__(self,  **kwargs):
        for k, v in kwargs.iteritems():
            self[k] = v

    def finalize(self):
        tx_hash = sha256(json.dumps(self)).hexdigest()
        self['hash'] = tx_hash
        return tx_hash, self


class RegistrationTransaction(Transaction):
    def __init__(self):
        """
                        Initialize a registration transaction that allows people
                        to vote. You'll have to pull off the signature and send it 
                        to the voter.
        """

        register_id = str(uuid.uuid4())
        signed_register_id = key_verification.sign_with_private_key(
            register_id)
        pub_key, signed_data = key_verification.create_new_voter()
        super(RegistrationTransaction, self).__init__(input={
            "register_id": register_id, "signed_register_id": signed_register_id}, out={"pub_key": pub_key})
        self.signed_data = signed_data

    def validate(self,
                 current_transaction_array,
                 block_chain):
        """
                Validate that my input key is acceptable for registration.
                                                                We are confirming that the registration was obtained with 
                                                                the correct private key.
        """

        if not key_verification.verify_register_key(self['input']['signed_register_id'],
                                                    self['input']['register_id']):

            raise InvalidTransactionException, 'The Registration transaction wasnt signed by an accepted key'


class VoteTransaction(Transaction):
    def validate(self,
                 current_transaction_array,
                 block_chain):
        """
                Validate that 
                        1. My input is a real registration transaction in earlier blocks
                        2. I've satisfied the output clause of the registration
                        3. My vote is valid for the ballot 
        """
        input_transaction_id = self['input']['reg_tx_hash']

        def reverse_traverse_transactions(current_transaction_array, chain):
            for i in xrange(len(current_transaction_array) - 1, -1, -1):
                yield current_transaction_array[i]
            for i in xrange(len(chain) - 1, 1, -1):
                current_transaction_array = chain[i]['tx']
                for i in xrange(len(current_transaction_array) - 1, -1, -1):
                    yield current_transaction_array[i]
            raise InvalidTransactionException, "There is no registration affiliated with this vote"

        # We will break out of this loop once we find our vote's valid registration transaction
        for tx in reverse_traverse_transactions(current_transaction_array, block_chain):
            if tx['input'].get('reg_tx_hash') == self['input']['reg_tx_hash']:
                raise InvalidTransactionException, "This registration has already voted "

            if tx['hash'] == self['input']['reg_tx_hash']:
                if not key_verification.verify_voter(tx['out']['pub_key'], self['input']['signature']):
                    raise InvalidTransactionException, "The signature cannot be verified with the public key"
                else:
                    break

        # Here we verify that all votes on the ballot are valid
        for i, vote in enumerate(self['ballot_votes']):
            block_chain.ballot[i].validate_vote(vote)

        # Here we commit those votes to the Election Results
        for i, vote in enumerate(self['ballot_votes']):
            block_chain.ballot[i] += vote


if __name__ == '__main__':
    t = Transaction(hello=1,
                    goodbye=2)
    t.finalize()
    print t
