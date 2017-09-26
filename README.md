Voting platform that uses a blockchain. 

P2P Client / Miner
	-> For now, I can use a hardcoded list of IP and port combinations, this isn't an easy problem on its own. 
	-> API spec
		-> On startup, the client establishes which peers are up, and opens connections to them ( Ping / Pong ) 
		-> It asks each server for the latest hash available, and how many blocks past local chain ( getblocks ) 
		-> 


Block Chain basics: 
	-> Each block is a merkle tree
	-> The root is given the nonce to meet block hash requirements ( mining ) 
	-> Each transaction is broadcast with 


Identity verification 

