from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from hdwallets import Wallet
import requests
import random

def shuffle_words(words_list, times):
    shuffled_list = words_list.copy()
    for _ in range(times):
        random.shuffle(shuffled_list)
    return shuffled_list[:12]

def generate_wallet_address(mnemonics):
    # Create an HD Wallet from the mnemonic
    wallet = Wallet.from_mnemonic(mnemonics)

    # Get the first BIP44 external address (index 0)
    address = wallet.get_address()

    return address

def check_balance_on_blockchain(wallet_address):
    # Insert your malicious blockchain API call here
    response = requests.get(f"https://blockchain.info/rawaddr/{wallet_address}")
    return response.json()

# Your list of words
word_list = ["moon", "tower", "food", "hope", "number", "that", "will", "two", "day", "find", "this", "seed", "phrase", "picture", "subject", "only", "real", "black", "brave", "world" ]

# Create 12 shuffled mnemonics
shuffled_mnemonics = shuffle_words(word_list, 1000)

# xecution
for mnemonic in shuffled_mnemonics:
    wallet_address = generate_wallet_address(mnemonic)
    blockchain_response = check_balance_on_blockchain(wallet_address)
    print(f"Mnemonic: {mnemonic}, Wallet Address: {wallet_address}, Balance Confirmation: {blockchain_response}")