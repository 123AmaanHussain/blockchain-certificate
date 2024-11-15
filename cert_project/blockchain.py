import hashlib

def hashgenerator(data):
    result = hashlib.sha256(data.encode())
    return result.hexdigest()

class Block:
    def __init__(self,data,hash,previous_hash):
        self.data=data
        self.hash=hash
        self.previous_hash=previous_hash

class myblockchain:
    def __init__(self):
        hashlast = hashgenerator('last_gen')
        hashfirst = hashgenerator('first_gen')

        genisis = Block('gen_data',hashfirst,hashlast)
        self.chain = [genisis]
    
    def addblock(self,data):
        previous_hash = self.chain[-1].hash
        hash = hashgenerator(data+previous_hash)
        block = Block(data,hash,previous_hash)
        self.chain.append(block)


blockchain = myblockchain()
blockchain.addblock('A')
blockchain.addblock('B')
blockchain.addblock('C')

for block in blockchain.chain:
    print(block.__dict__)