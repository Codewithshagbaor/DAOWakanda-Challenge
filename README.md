# DAOWakanda-Challenge (Transfer of Ownership)
Using the Algorand Python SDK or the AlgorandJavascript SDK, write a script that performs the following actions:
- Create two accounts, A & B
-Fund the two accounts with 10 algos each
- Rekey account A to account B (This would make account B able to authorize transactions on behalf of account A)
- Transfer all the algos in account A to account B (The transaction should be authorized by account B)

Your script should run on the localnet. To submit, provide the link to the GitHub repository your submission was pushed to. Ensure that your repository is public. Best of luck!

# Solution
Solution Overview
This script demonstrates key functionalities of the Algorand blockchain using the Algorand Python SDK. It performs the following actions on a local Algorand network (localnet):

Creates two accounts, A and B, using the Algorand SDK's account generation feature.
Funds both accounts with 10 ALGOs each from a pre-funded creator account, ensuring they meet the Algorand blockchain's minimum balance requirements of 0.1 ALGO.
Rekeys Account A to Account B, allowing Account B to authorize transactions on behalf of Account A while retaining Account A's public address.
Transfers all ALGOs from Account A to Account B, except for the minimum balance required to keep Account A active. The transaction is authorized by Account B to validate the rekeying.
The script is designed to maintain minimum balance constraints and account for transaction fees to ensure compliance with Algorand network rules while demonstrating advanced features like rekeying and multi-account interaction.
## Requirements

1. Algorand localnet running on your machine.
2. Python 3.12+ installed.
3. Install required dependencies:
```
   pip install py-algorand-sdk python-dotenv
```
### Setup
Clone the repository:
```
git clone <repository_url>
cd <repository_name>
```

Create a .env file in the project root and add the following details:
```
WALLET_ADDRESS=<Your Creator Account Address>
WALLET_PRIVATE_KEY=<Your Creator Private Key>
```
Please ensure your localnet is running and the creator account has enough balance.

Setup Sandbox

Make sure the docker daemon is running and docker-compose is installed.

Open a terminal and run:
In whatever local directory the sandbox should reside. Then:

```bash
cd sandbox
./sandbox up
```

This will run the `sandbox` shell script with the default configuration. See the [Basic Configuration](#basic-configuration) for other options.

Execution
Run the script:
```
python main.py
```
Notes
Ensure the creator account has at least 22 Algos to cover funding and transaction fees.
