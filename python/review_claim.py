
# Review insurance claims using an authorized insurer

from pathlib import Path
from web3 import Web3
from solcx import compile_source, install_solc

GANACHE_URL = "http://127.0.0.1:7545"
SOLIDITY_VERSION = "0.8.20"

# Use the same contract address from Commit 8
CONTRACT_ADDRESS = "0x68353A118390056876527AF9f6cC7728bc15f6B4"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_FILE = PROJECT_ROOT / "solidity" / "InsuranceClaims.sol"


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

    return web3.eth.contract(
        address=Web3.to_checksum_address(CONTRACT_ADDRESS),
        abi=contract_data["abi"]
    )

# Command to approve or reject a claim
def review_claim(web3, contract, claim_id, decision):

    insurer_account = web3.eth.accounts[0]

    if decision == "approve":
        transaction = contract.functions.approveClaim(claim_id)
    elif decision == "reject":
        transaction = contract.functions.rejectClaim(claim_id)
    else:
        raise ValueError("Decision must be approve or reject.")

    transaction_hash = transaction.transact({
        "from": insurer_account
    })

    receipt = web3.eth.wait_for_transaction_receipt(
        transaction_hash,
        timeout=120
    )

    if receipt.status != 1:
        raise RuntimeError("Claim review transaction failed.")

    print(f"Transaction hash: {transaction_hash.hex()}")
    print("Claim review completed successfully!")

# Connecting to ganache
def main():

    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

    if not web3.is_connected():
        raise ConnectionError("Could not connect to Ganache.")

    if not Web3.is_address(CONTRACT_ADDRESS):
        raise ValueError("Set a valid deployed contract address.")

    contract = load_contract(web3)

    if not web3.eth.get_code(contract.address):
        raise RuntimeError("No deployed contract found at this address.")

    insurer_account = web3.eth.accounts[0]
    contract_insurer = contract.functions.insurer().call()

    if insurer_account.lower() != contract_insurer.lower():
        raise RuntimeError(
            "Account 0 is not the insurer for this contract."
        )

    print("Connected to Ganache!")
    print(f"Insurer: {insurer_account}")

    # Select a claim submitted
    claim_id = 1

    claim_before = contract.functions.getClaim(claim_id).call()
    print(f"Status before: {claim_before[5]}")

    if claim_before[5] != "Pending":
        raise RuntimeError("The selected claim is not pending.")

    # Change to "reject" to test the other decision
    decision = "approve"

    review_claim(web3, contract, claim_id, decision)

    claim_after = contract.functions.getClaim(claim_id).call()
    print(f"Status after: {claim_after[5]}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Application error: {error}")
        raise SystemExit(1)
