from web3 import Web3
from solcx import compile_standard, install_solc
import json
import os
from solcx import install_solc
# Install Solidity compiler
install_solc('0.8.0')
install_solc('0.8.19')
# Besu Local RPC URL (Free gas network URL)
BESU_URL = "http://127.0.0.1:8545"  # Change this to your Besu node URL if different

# Connect to the Besu free gas network
w3 = Web3(Web3.HTTPProvider(BESU_URL))

# Check connection
if not w3.is_connected():
    print("Failed to connect to Besu. Ensure the URL is correct and the Besu node is running.")
    exit()

print(f"Connected to Besu at {BESU_URL}")

# Load and compile the Solidity contract
CONTRACT_PATH = 'contracts/Voting.sol'
if not os.path.exists(CONTRACT_PATH):
    print(f"Contract file not found at {CONTRACT_PATH}")
    exit()

with open(CONTRACT_PATH, 'r') as file:
    contract_source_code = file.read()

compiled_contract = compile_standard({
    "language": "Solidity",
    "sources": {
        "Voting.sol": {
            "content": contract_source_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode"]
            }
        }
    }
})

# Extract ABI and Bytecode
abi = compiled_contract['contracts']['Voting.sol']['VotingSystem']['abi']
bytecode = compiled_contract['contracts']['Voting.sol']['VotingSystem']['evm']['bytecode']['object']

# Print basic contract info for debugging
print("Contract compiled successfully!")
print(f"Contract Bytecode (first 50 chars): {bytecode[:50]}...")
print(f"Contract ABI: {abi[:2]}...")

# Besu account details (make sure this account is unlocked on Besu node)
account = "0x2DFBde5603b82fb8196EBdFa6A8675616236576a"  # Replace with your Besu account address
private_key = "0x5a0efc86deb424d1821269c812d7b120ab156d90b235cb27c1183fc4e58bd6bc"  # Replace with your Besu account private key

# Build the contract instance
VotingSystem = w3.eth.contract(abi=abi, bytecode=bytecode)

# Build the transaction for deploying the contract
transaction = VotingSystem.constructor().build_transaction({
    'from': account,
    'gas': 12000000,  # Ensure enough gas for deployment (based on Besu settings)
    'gasPrice': 0,    # Zero gas price for free gas network
    'nonce': w3.eth.get_transaction_count(account),
    'value': 0        # No ether sent with the transaction
})

# Sign the transaction
signed_tx = w3.eth.account.sign_transaction(transaction, private_key)

# Deploy the contract
try:
    print("Deploying the contract...")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transaction hash: {tx_hash.hex()}")

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    print(f"Contract successfully deployed at address: {contract_address}")

    # Verify bytecode at the address
    deployed_bytecode = w3.eth.get_code(contract_address)
    if deployed_bytecode == b'':  # If no bytecode is deployed
        print("Error: No bytecode found at contract address. Deployment failed.")
    else:
        print(f"Deployed Contract Bytecode: {deployed_bytecode[:50]}...")

    # Save the deployed contract's details (ABI and address) to a file
    DEPLOYMENT_DETAILS_PATH = 'contract_details.json'
    deployment_details = {
        "abi": abi,
        "contract_address": contract_address
    }

    try:
        with open(DEPLOYMENT_DETAILS_PATH, 'w') as file:
            json.dump(deployment_details, file, indent=4)
        print(f"Contract deployment details saved to {DEPLOYMENT_DETAILS_PATH}")
    except Exception as e:
        print(f"Error saving deployment details: {e}")

except Exception as e:
    print(f"Error during contract deployment: {e}")
    if hasattr(e, 'args'):
        print("Error details:", e.args)
