
# This code is to submit and retrieve an insurance claim

from pathlib import Path
from web3 import Web3
from solcx import compile_source, install_solc

GANACHE_URL = "http://127.0.0.1:7545"
SOLIDITY_VERSION = "0.8.20"

# Replace this value with your deployed contract address
CONTRACT_ADDRESS = "0x68353A118390056876527AF9f6cC7728bc15f6B4"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_FILE = PROJECT_ROOT / "solidity" / "InsuranceClaims.sol"

# Compile Solidity source abd load a contract
def load_contract(web3):

    install_solc(SOLIDITY_VERSION)

    source_code = CONTRACT_FILE.read_text(encoding="utf-8")

    compiled = compile_source(
        source_code,
        output_values=["abi"],
        solc_version=SOLIDITY_VERSION,
        evm_version="paris"
    )

    contract_data = next(
        data
        for name, data in compiled.items()
        if name.endswith(":InsuranceClaims")
    )

    abi = contract_data["abi"]

    return web3.eth.contract(
        address=Web3.to_checksum_address(CONTRACT_ADDRESS),
        abi=abi
    )

# Submit an insurance claim
def submit_claim(web3, contract):

    # Account 0 is the insurer; Account 1 is the customer
    customer_account = web3.eth.accounts[1]

    policy_number = "POL-1001"
    description = "Vehicle damage after a minor accident"

    # Claim amount is stored in euro cents
    claim_amount = 150000

    print(f"Customer account: {customer_account}")
    print(f"Policy number: {policy_number}")
    print(f"Claim amount: {claim_amount / 100:.2f} EUR")

    transaction_hash = contract.functions.submitClaim(
        policy_number,
        description,
        claim_amount
    ).transact({
        "from": customer_account
    })

    receipt = web3.eth.wait_for_transaction_receipt(
        transaction_hash,
        timeout=120
    )

    if receipt.status != 1:
        raise RuntimeError("Claim submission failed.")

    print("Insurance claim submitted successfully!")
    print(f"Transaction hash: {transaction_hash.hex()}")

    return receipt

# Retrieve an insurance claim from the blockchain
def display_claim(contract, claim_id):

    claim = contract.functions.getClaim(claim_id).call()

    print("\n--- Insurance Claim Details ---")
    print(f"Claim ID: {claim[0]}")
    print(f"Customer address: {claim[1]}")
    print(f"Policy number: {claim[2]}")
    print(f"Description: {claim[3]}")
    print(f"Claim amount: {claim[4] / 100:.2f} EUR")
    print(f"Status: {claim[5]}")

# Connection with the ganache
def main():

    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

    if not web3.is_connected():
        raise ConnectionError("Could not connect to Ganache.")

    print("Connected to Ganache!")

    if not Web3.is_address(CONTRACT_ADDRESS):
        raise ValueError("Set a valid deployed contract address.")

    contract = load_contract(web3)

    # Verify that the address contains contract bytecode
    if not web3.eth.get_code(contract.address):
        raise RuntimeError(
            "No contract found at this address. "
            "Check Ganache and the deployed contract address."
        )

    # Read the number of claims before submitting a new one
    previous_count = contract.functions.claimCount().call()

    print(f"Claims before submission: {previous_count}")

    submit_claim(web3, contract)

    # The contract increments the claim counter after submission
    new_count = contract.functions.claimCount().call()

    print(f"Claims after submission: {new_count}")

    if new_count != previous_count + 1:
        raise RuntimeError("Claim counter did not increase as expected.")

    display_claim(contract, new_count)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Application error: {error}")
        raise SystemExit(1)
