# Vote counter using a blockchain like db

### Transactions
	- There are two types of transactions here, a registration and a vote.
	- The registration transaction can be verified using the registration services public key. For now, this key is baked in to the {{key_verification}} module. 
	- Each vote transaction can be verified by checking its accompanying registration. When a registration occurs, a new RSA key is generated. This key is then used to sign the string 'valid_voter'. The public key goes in to the registration transaction, and it is used to verify the signed string that is texted to the user. 
	- By exchanging user information for a signed string, we anonymize the data when storing results. 
    - Each voter can only vote once and this can be enforced through our block chain db. 

### Elections
    - 3 types of elections are currently supported ( Simple Majority, Pick Two, Ranked election)
    - A Ballot is simply a list of elections. 
    - While there is support for write in candidates within the data structure and internal API, the web UI currently doesnt support this.

### Blockchain DB ? 
    - Transactions are pushed in to a buffer for now. To commit votes to the elections, you need to mine and commit the block.
    - Currently the datastructure allows for co-operative mining and verification, however there isn't any P2P code that would allow for it. 

### Requirements 
    - jinja2, tornado, and a recent version of pyOpenSSL. (Installing/Upgrading pyOpenSSL can be tricky, I actually had to rm the package and egg from my dist-packages file since it was using a .so file. Removing that, and doing a fresh pip install should get that package working)

### Shortcomings 
This is only a POC. A few next steps: 
1. Baking the current state of election results in to the merkle roots for each block. This will allow us to confirm not only the transactions in each block but also independent tabulation of the results.
2. Separating the DB/internal API from the external facing Web UI. 
3. Currently as a single threaded app, mining will cause the API to stop. If the difficulty is high, this can end up with requests that time out. Ideally mining should run in its own thread periodically, without affecting new incoming transactions. 
4. The signed data that is texted to the registered user is super verbose, its probably possible to use a seed phrase or something generally more memorable.
5. Currently there is no identity verification, ideally that would happen before registration.
    
