#! /usr/bin/python

from collections import deque
from hashlib import sha256


def get_merkle_root_from_interior_nodes(current_tier):
    """
            This is a recursive function to build a merkle tree and 
            return the merkle root hash.  The input to this tree must be an 
            deque of already hashed transactions. You probably want to pass in 
            map(lambda x:sha256(x).hexdigest(), transactions))
    """

    if len(current_tier) == 1:
        return current_tier[0]

    if len(current_tier) % 2 != 0:
        current_tier.append('')

    next_tier = deque()
    for i in xrange(1, len(current_tier), 2):
        x, y = current_tier.popleft(), current_tier.popleft()
        next_tier.append(sha256(x + y).hexdigest())

    return get_merkle_root_from_interior_nodes(next_tier)


def get_merkle_root_for_transactions(transactions):
    return get_merkle_root_from_interior_nodes(deque(
        map
        (lambda x: sha256(x).hexdigest(),
         transactions)
    )
    )


if __name__ == '__main__':
    transactions = ['a', 'b', 'c', 'd']
    assert(get_merkle_root_for_transactions(['a', 'b', 'c', 'd']) == '58c89d709329eb37285837b042ab6ff72c7c8f74de0446b091b6a0131c102cfd'), \
        'Something is off with your merkle tree implementation'
