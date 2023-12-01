from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from hdwallet import BIP44HDWallet, BIP44Derivation, Bip84, Bip84Coins, Bip44Changes, Bip39SeedGenerator
import requests
import random

def shuffle_words(words_list, times):
    shuffled_list = words_list.copy()
    for _ in range(times):
        random.shuffle(shuffled_list)
    return shuffled_list

def generate_wallet_address(mnemonics_list):
    addresses = []
    for mnemonics in mnemonics_list[:12]:
        # BIP-44 derivation for BTC
        checked_wallet_bip44 = BIP44HDWallet(cryptocurrency="bitcoin")
        checked_wallet_bip44.from_mnemonic(mnemonic=mnemonics, language="english", passphrase=None)
        checked_wallet_bip44.clean_derivation()
        checked_wallet_bip44_derivation = BIP44Derivation(cryptocurrency="bitcoin", account=0, change=False, address=0)
        checked_wallet_bip44.from_path(path=checked_wallet_bip44_derivation)
        address_bip44 = checked_wallet_bip44.address()

        # BIP-84 derivation for BTC
        checked_wallet_bip84 = Bip84.FromMnemonic(mnemonics, Bip84Coins.BITCOIN)
        checked_wallet_bip84_step1 = (checked_wallet_bip84.Purpose().Coin().Account(0)).Change(Bip44Changes.CHAIN_EXT)
        checked_wallet_bip84_step2 = checked_wallet_bip84_step1.AddressIndex(0)
        address_bip84 = checked_wallet_bip84_step2.PublicKey().ToAddress()

        addresses.append((address_bip44, address_bip84))

    return addresses

def check_balance_on_blockchain(wallet_address):
    # Insert your malicious blockchain API call here
    response = requests.get(f"https://blockchain.info/rawaddr/{wallet_address}")
    return response.json()

# Your list of words
word_list = ["moon", "tower", "food", "hope", "number", "that", "will", "two", "day", "find", "this", "seed", "phrase", "picture", "subject", "only", "real", "black", "brave", "world"]

# Create 1000 shuffled mnemonics
shuffled_mnemonics = shuffle_words(word_list, 1000)

# Create 12 shuffled mnemonics
shuffled_mnemonics_12 = shuffled_mnemonics[:12]

# Execution
addresses = generate_wallet_address(shuffled_mnemonics_12)

for i, (address_bip44, address_bip84) in enumerate(addresses, start=1):
    print(f"Address {i}:")
    print(f"Wallet Address (BIP44): {address_bip44}, Balance Confirmation: {check_balance_on_blockchain(address_bip44)}")
    print(f"Wallet Address (BIP84): {address_bip84}, Balance Confirmation: {check_balance_on_blockchain(address_bip84)}")
    print()