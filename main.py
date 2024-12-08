import json
from algosdk import account, mnemonic, transaction
from algosdk.v2client import algod
from dotenv import load_dotenv
import os

load_dotenv()

# Get address from .env file
creator_address = os.getenv('WALLET_ADDRESS')
creator_private_key = os.getenv('WALLET_PRIVATE_KEY')

# Connect to the Algorand localnet
ALGOD_ADDRESS = "http://localhost:4001"  # Replace with your localnet address
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  # Default token for localnet
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def create_account():
    private_key, address = account.generate_account()
    print(f"Account Address: {address}")
    print(f"Account Mnemonic: {mnemonic.from_private_key(private_key)}")
    return private_key, address

def fund_account(receiver, amount):
    sender = creator_address
    sender_private_key = creator_private_key
    account_info = client.account_info(sender)
    current_balance = account_info['amount']
    
    print(f"Current balance of {sender}: {current_balance}")
    
    if current_balance < amount + 1000:  # Ensuring minimum balance
        print(f"Insufficient balance. Cannot transfer {amount}")
        return None
    ## Fund the account using a already funded account(Creator account)
    try:
        params = client.suggested_params()
        unsigned_txn  = transaction.PaymentTxn(sender, params, receiver, amount, note=b"Funding Account",)
        signed_txn = unsigned_txn.sign(sender_private_key)
        txid = client.send_transaction(signed_txn)
        print("Successfully submitted transaction with txID: {}".format(txid))
        txn_result = transaction.wait_for_confirmation(client, txid)
        print(f"Transaction information: {json.dumps(txid, indent=4)}")
        return txn_result
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


def rekey_account(account_a, account_b, private_key_a):
    try:
        params = client.suggested_params()
        txn = transaction.PaymentTxn(account_a, params, account_a, 0, rekey_to=account_b)
        signed_txn = txn.sign(private_key_a)
        txid = client.send_transaction(signed_txn)
        print(f"Rekey transaction sent with ID: {txid}")
        txn_result = transaction.wait_for_confirmation(client, txid)
        print(f"Transaction information: {json.dumps(txn_result, indent=4)}")
        return txn_result
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def transfer_algos(from_account, to_account, private_key):
    # First, check the balance of the source account
    account_info = client.account_info(from_account)
    current_balance = account_info['amount']
    
    # Ensure transfer leaves at least the minimum balance
    min_balance = 100_000  # Minimum required balance
    fee = 1_000  # Transaction fee
    transfer_amount = current_balance - (min_balance + fee)
    
    print(f"Current balance of {from_account}: {current_balance}")
    print(f"Transfer amount: {transfer_amount}")
    
    if transfer_amount <= 0:  # Check if there’s enough balance to transfer
        print(f"Insufficient balance to transfer after retaining minimum balance.")
        return None
    
    try:
        params = client.suggested_params()
        txn = transaction.PaymentTxn(from_account, params, to_account, transfer_amount)
        signed_txn = txn.sign(private_key)
        txid = client.send_transaction(signed_txn)
        print(f"Transfer transaction sent with ID: {txid}")
        return transaction.wait_for_confirmation(client, txid)
    except Exception as e:
        print(f"Error in transfer: {e}")
        return None


if __name__ == "__main__":
    if not creator_address or not creator_private_key:
        raise Exception("No creator address provided")
    # Step 1: Create two accounts, A and B
    print("Creating Account A...")
    private_key_a, address_a = create_account()

    print("\nCreating Account B...")
    private_key_b, address_b = create_account()

    # Step 2: Fund the two accounts with 10 algos each
    print("\nFunding Account A...")
    fund_account(address_a, 10_000_000)
    account_a_info = client.account_info(address_a)
    print(f"Account A balance after funding: {account_a_info['amount']}")
    
    print("\nFunding Account B...")
    fund_account(address_b, 10_000_000)
    account_b_info = client.account_info(address_b)
    print(f"Account B balance after funding: {account_b_info['amount']}")
    
    # Step 3: Rekey Account A to Account B
    print("\nRekeying Account A to Account B...")
    rekey_account(address_a, address_b, private_key_a)
    account_a_balance = client.account_info(address_a)['amount']
    
    # Step 4: Transfer all algos from Account A to Account B (authorized by B)
    print("\nTransferring all algos from Account A to Account B...")
    account_a_balance = client.account_info(address_a)["amount"]
    transfer_algos(address_a, address_b, private_key_b)  # Account A needs to retain a minimum balance of 0.1 ALGO
