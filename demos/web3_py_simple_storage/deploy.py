import json
from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

private_key = os.getenv("PRIVATE_KEY")
infura_id = os.getenv("WEB3_INFURA_PROJECT_ID")
my_address = os.getenv("MY_ADDRESS")

with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

solc_version = "0.8.7"

# Compilează contractul
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}}
        },
    },
    solc_version=solc_version,
)


with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


#how to deploy
#get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi
abi= compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


alchemy_url = os.getenv("ALCHEMY_URL")
w3 = Web3(Web3.HTTPProvider(alchemy_url))
chain_id = 11155111  # Sepolia chain ID



#create the contract in python 
simple_storage = w3.eth.contract(abi=abi, bytecode=bytecode)
#get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)


# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = simple_storage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gas": 3000000,
        "gasPrice": w3.to_wei("20", "gwei"),
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

#Send this signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")
#Working with the contract , you always need:
#Contract Adress
#Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


# .call(): folosit pentru a citi date din contract fara a modifica blockchain-ul (nu costa gaz)
# .transact(): folosit pentru a trimite tranzactii care modifica starea contractului (costă gaz)

store_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
        "gas": 300000,
        "gasPrice": w3.to_wei("20", "gwei"),  # <-- forțează tranzacția legacy
    }
)


signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())
