from btclib import bip32, bip44

import requests
import random

class WalletGenerator:
    def __init__(self, mnemonics_list):
        self.mnemonics_list = mnemonics_list

    def shuffle_words(self, words_list, times):
        shuffled_list = words_list.copy()
        for _ in range(times):
            random.shuffle(shuffled_list)
        return shuffled_list

    def generate_wallet_address(self):
        addresses = []
        for mnemonics in self.mnemonics_list[:12]:
            # BIP-44 derivation for BTC
            bip32_root_key = bip32.from_mnemonic(mnemonics)
            bip44_account_key = bip44.derive(bip32_root_key, bip44_path="m/44'/0'/0'/0/0")
            address_bip44 = bip44.address(bip44_account_key)

            # BIP-84 derivation for BTC
            bip84_account_key = bip44.derive(bip32_root_key, bip44_path="m/84'/0'/0'/0/0")
            address_bip84 = bip44.address(bip84_account_key)

            addresses.append((address_bip44, address_bip84))

        return addresses

    def check_balance_on_blockchain(self, wallet_address):
        # Insert your malicious blockchain API call here
        response = requests.get(f"https://blockchain.info/rawaddr/{wallet_address}")
        return response.json()

# Your list of words
word_list = [
    "moon", "tower", "food", "hope", "number", "that", "will", "two", "day", "find", 
    "this", "seed", "phrase", "picture", "subject", "only",
    "real", "black", "brave", "world"]

# Create 1000 shuffled mnemonics
shuffled_mnemonics = random.sample(word_list, k=1000)
# Create 12 shuffled mnemonics
shuffled_mnemonics_12 = shuffled_mnemonics[:12]

# Create instance of WalletGenerator
wallet_generator_instance = WalletGenerator(shuffled_mnemonics_12)

    # Execution
addresses = wallet_generator_instance.generate_wallet_address()
for i, (address_bip44, address_bip84) in enumerate(addresses, start=1):
            print(f"Address {i}:")
            print(f"Wallet Address (BIP44): {address_bip44}, Balance Confirmation: {wallet_generator_instance.check_balance_on_blockchain(address_bip44)}")
            print(f"Wallet Address (BIP84): {address_bip84}, Balance Confirmation: {wallet_generator_instance.check_balance_on_blockchain(address_bip84)}")
            print()
