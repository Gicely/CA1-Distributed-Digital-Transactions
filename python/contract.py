
# This code is to do a deploy a Solidity contract to Ganache

from pathlib import Path
from web3 import Web3
from solcx import compile_source, install_solc


# Local Ganache blockchain address
GANACHE_URL = "http://127.0.0.1:7545"

# Solidity compiler version
SOLIDITY_VERSION = "0.8.20"

# Locate the Solidity file inside the project
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
CONTRACT_FILE = PROJECT_FOLDER / "solidity" / "InsuranceClaims.sol"


def compile_contract():
    
    print("Installing Solidity compiler if needed...")

    # Install the required Solidity compiler version
    install_solc(SOLIDITY_VERSION)

    # Read the Solidity source code
    source_code = CONTRACT_FILE.read_text(encoding="utf-8")

    # Compile the smart contract
    compiled = compile_source(
        source_code,
        output_values=["abi", "bin"],
        solc_version=SOLIDITY_VERSION,
        evm_version="paris"

    )

    # Select the InsuranceClaims contract
    contract_data = next(
        data
        for name, data in compiled.items()
        if name.endswith(":InsuranceClaims")
    )

    print("Smart contract compiled successfully!")

    return contract_data["abi"], contract_data["bin"]


def deploy_contract(web3, abi, bytecode):
    
    # Use the first account as the insurer
    insurer_account = web3.eth.accounts[0]

    print(f"Insurer account: {insurer_account}")

    # Create a contract deployment object
    contract = web3.eth.contract(
        abi=abi,
        bytecode=bytecode
    )

    # Send the deployment transaction to Ganache
    transaction_hash = contract.constructor().transact({
        "from": insurer_account
    })

    print(f"Transaction hash: {transaction_hash.hex()}")

    # Wait for the transaction to be confirmed
    receipt = web3.eth.wait_for_transaction_receipt(
        transaction_hash,
        timeout=120
    )

    # Check whether the transaction succeeded
    if receipt.status != 1:
        raise RuntimeError("Contract deployment failed.")

    print("Smart contract deployed successfully!")
    print(f"Contract address: {receipt.contractAddress}")
    print(f"Block number: {receipt.blockNumber}")

    return receipt.contractAddress


def main():
    
    print("Insurance Smart Contract Deployment")

    # Connect to the local Ganache blockchain
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

    if not web3.is_connected():
        print("Error: Could not connect to Ganache.")
        return

    print("Connected to Ganache!")

    # Compile the Solidity smart contract
    abi, bytecode = compile_contract()

    # Deploy the smart contract
    contract_address = deploy_contract(
        web3,
        abi,
        bytecode
    )

    # Create a Python object for the deployed contract
    deployed_contract = web3.eth.contract(
        address=contract_address,
        abi=abi
    )

    # Verify the insurer address stored on the blockchain
    insurer = deployed_contract.functions.insurer().call()

    print("\n--- Contract Verification ---")
    print(f"Insurer: {insurer}")
    print(f"Total claims: {deployed_contract.functions.claimCount().call()}")


if __name__ == "__main__":

    try:
        main()

    except Exception as error:
        print(f"Deployment error: {error}")
