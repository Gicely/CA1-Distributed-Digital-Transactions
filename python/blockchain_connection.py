# This code is to connect the blockchain between Python and Ganache

from web3 import Web3

# The port that Ganache is using on the app
GANACHE_URL = "http://127.0.0.1:7545"


def connect_to_blockchain():
    
    # Creating a connection using the Ganache RPC server
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

    # Checking if the connection was successful
    if web3.is_connected():
        print("Successfully connected to Ganache!")
        return web3

    # Displaying an error if the connection fails
    print("Error: Could not connect to Ganache.")
    return None


def display_blockchain_info(web3):
   
    # Getting the blockchain chain ID
    chain_id = web3.eth.chain_id

    # Getting the latest block number
    block_number = web3.eth.block_number

    print("\n--- Blockchain Information ---")
    print(f"Chain ID: {chain_id}")
    print(f"Latest Block: {block_number}")


def display_accounts(web3):
   
    # Getting the accounts created by Ganache
    accounts = web3.eth.accounts

    print("\n--- Ethereum Accounts ---")

    # Displaying the first three accounts
    for index, account in enumerate(accounts[:3]):

        # Geting the account balance in Wei
        balance_wei = web3.eth.get_balance(account)

        # Convertting the balance from Wei to ETH
        balance_eth = web3.from_wei(balance_wei, "ether")

        print(f"\nAccount {index + 1}: {account}")
        print(f"Balance: {balance_eth} ETH")

# Main program
if __name__ == "__main__":

    print("Insurance Blockchain Application")
    print("Connecting to Ganache...")

    try:
        # Connecting Python to Ganache
        web3 = connect_to_blockchain()

        # Continue only if the connection is successful
        if web3 is not None:

            # Display blockchain information
            display_blockchain_info(web3)

            # Display Ethereum accounts
            display_accounts(web3)

    except Exception as error:
        # Display an error if something goes wrong
        print(f"Blockchain error: {error}")
