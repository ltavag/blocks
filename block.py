#! /usr/bin/python

import merkle
import json
import sys
import struct
import hashlib

"""
	From https://blockchain.info/api/blockchain_api, 
	heres how a block looks in their API 
	
	{
    "hash":"0000000000000bae09a7a393a8acded75aa67e46cb81f7acaa5ad94f9eacd103",
    "ver":1,
    "prev_block":"00000000000007d0f98d9edca880a6c124e25095712df8952e0439ac7409738a",
    "mrkl_root":"935aa0ed2e29a4b81e0c995c39e06995ecce7ddbebb26ed32d550a72e8200bf5",
    "time":1322131230,
    "bits":437129626,
    "nonce":2964215930,
    "n_tx":22,
    "size":9195,
    "block_index":818044,
    "main_chain":true,
    "height":154595,
    "received_time":1322131301,
    "relayed_by":"108.60.208.156",
    "tx":[--Array of Transactions--]
{
"""


def swap_order(x):
    x = x[::-1]
    return ''.join([x[i + 1] + x[i] for i in xrange(0, len(x) - 1, 2)])


def little_endian(x):
    return struct.pack('<i', x).encode('hex')


def build_hash(**kwargs):
    parts = ''.join([
        little_endian(kwargs['ver']),
        swap_order(kwargs['prev_block']),
        swap_order(kwargs['mrkl_root']),
        little_endian(kwargs['time']),
        little_endian(kwargs['bits']),
        little_endian(kwargs['nonce'])
    ]).decode('hex')
    h = hashlib.sha256(hashlib.sha256(parts).digest()).digest()
    return kwargs['nonce'], h[::-1].encode('hex_codec')


if __name__ == '__main__':
    '''
            Ensure that you are able to build the hash correctly 
            by running the following line 
            curl 'https://blockchain.info/rawblock/000000000000000000165fab1959a2575748085b635d867f4840f888d8f24e76' | python block.py 
    '''
    block_data = json.loads(sys.stdin.read())
    assert build_hash(
        **block_data) == (block_data['nonce'], block_data['hash']), 'The hash doesnt check out'
