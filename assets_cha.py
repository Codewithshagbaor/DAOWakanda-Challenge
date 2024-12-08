import json
import os
from algosdk import account, mnemonic, transaction
from algosdk.v2client import algod
from dotenv import load_dotenv

load_dotenv()

# Configuration
ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

creator_address = os.getenv("WALLET_ADDRESS")
creator_private_key = os.getenv("WALLET_PRIVATE_KEY")

def create_account():
    private_key, address = account.generate_account()
    print(f"Account Address: {address}")
    print(f"Account Mnemonic: {mnemonic.from_private_key(private_key)}")
    return private_key, address

def fund_account(receiver, amount):
    params = client.suggested_params()
    txn = transaction.PaymentTxn(creator_address, params, receiver, amount)
    signed_txn = txn.sign(creator_private_key)
    txid = client.send_transaction(signed_txn)
    print(f"Funding transaction sent with ID: {txid}")
    transaction.wait_for_confirmation(client, txid)


def create_asa(manager_address, manager_private_key):
    params = client.suggested_params()
    txn = transaction.AssetConfigTxn(
        sender=manager_address,
        sp=params,
        total=1000,
        default_frozen=False,
        unit_name="MyASA",
        asset_name="MyAlgorandAsset",
        manager=manager_address,
        reserve=manager_address,
        freeze=manager_address,
        clawback=manager_address,
        decimals=0,
    )
    signed_txn = txn.sign(manager_private_key)
    txid = client.send_transaction(signed_txn)
    print(f"ASA creation transaction sent with ID: {txid}")
    transaction.wait_for_confirmation(client, txid)
    response = client.pending_transaction_info(txid)
    asset_id = response["asset-index"]
    print(f"Created ASA with Asset ID: {asset_id}")
    return asset_id

def opt_in_to_asa(account_address, account_private_key, asset_id):
    params = client.suggested_params()
    txn = transaction.AssetTransferTxn(
        sender=account_address, sp=params, receiver=account_address, amt=0, index=asset_id
    )
    signed_txn = txn.sign(account_private_key)
    txid = client.send_transaction(signed_txn)
    print(f"Opt-in transaction sent with ID: {txid}")
    transaction.wait_for_confirmation(client, txid)

def transfer_asa(sender_address, sender_private_key, receiver_address, asset_id, amount):
    params = client.suggested_params()
    txn = transaction.AssetTransferTxn(
        sender=sender_address,
        sp=params,
        receiver=receiver_address,
        amt=amount,
        index=asset_id,
    )
    signed_txn = txn.sign(sender_private_key)
    txid = client.send_transaction(signed_txn)
    print(f"ASA transfer transaction sent with ID: {txid}")
    transaction.wait_for_confirmation(client, txid)

def freeze_asa(freeze_account, freeze_private_key, target_account, asset_id, freeze_state=True):
    params = client.suggested_params()
    txn = transaction.AssetFreezeTxn(
        sender=freeze_account,
        sp=params,
        index=asset_id,
        target=target_account,
        new_freeze_state=freeze_state,
    )
    signed_txn = txn.sign(freeze_private_key)
    txid = client.send_transaction(signed_txn)
    print(f"Freeze transaction sent with ID: {txid}")
    transaction.wait_for_confirmation(client, txid)

if __name__ == "__main__":
    if not creator_address or not creator_private_key:
        raise Exception("Creator account not properly configured in .env file.")

    # Step 1: Create two accounts
    print("Creating Account A...")
    private_key_a, address_a = create_account()

    print("Creating Account B...")
    private_key_b, address_b = create_account()

    # Step 2: Fund the two accounts
    print("Funding Account A with 10 ALGOs...")
    fund_account(address_a, 10_000_000)

    print("Funding Account B with 10 ALGOs...")
    fund_account(address_b, 10_000_000)

    # Step 3: Create an ASA using Account A
    print("Creating ASA with Account A...")
    asset_id = create_asa(address_a, private_key_a)

    # Step 4: Opt Account B into the ASA
    print("Opting Account B into the ASA...")
    opt_in_to_asa(address_b, private_key_b, asset_id)

    # Step 5: Transfer 1 unit of ASA from Account A to Account B
    print("Transferring 1 unit of ASA from Account A to Account B...")
    transfer_asa(address_a, private_key_a, address_b, asset_id, 1)

    # Step 6: Freeze the ASA in Account B
    print("Freezing ASA in Account B...")
    freeze_asa(address_a, private_key_a, address_b, asset_id)

    print("Script execution completed.")
