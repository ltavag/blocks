#! /usr/bin/python

import json
from hashlib import sha256

"""
	There are two types of transactions that should be allowed. 
	
	1. Voter registration
			Here the input transaction ID should always be signed by a trusted 
			source. The public key we can accept for input is going to be 
			baked in to our code for now. 
	
			{
				"tx":
							"tx_hash",
				"in":
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
				"in":
						{
								"reg_tx_hash"
								"signature"
						},
				"ballad_votes":
						[	

						]	
			}
"""


class Transaction(dict):
    def __init__(self,  **kwargs):
        for k, v in kwargs.iteritems():
            self[k] = v

    def finalize(self):
        tx_hash = sha256(json.dumps(self)).hexdigest()
        self['hash'] = tx_hash
        return tx_hash, self


class Registration(Transaction):
    def validate(self):
        """
                Validate that my input key is acceptable for registration
        """

        pass


class Vote(Transaction):
    def validate(self):
        """
                Validate that 
                        1. My input is a real registration transaction in earlier blocks
                        2. I've satisfied the output clause of the registration
                        3. My vote is valid for the ballot 
        """
        pass


if __name__ == '__main__':
    t = Transaction(hello=1,
                    goodbye=2)
    t.finalize()
    print t
