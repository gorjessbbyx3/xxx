
"""
Cryptocurrency transaction analyzer with wallet generation and address analysis
"""
import re
from typing import Dict, List, Optional
import requests
from web3 import Web3, Account
from mnemonic import Mnemonic
from bip32utils import BIP32Key
import hashlib
import os
from eth_account.messages import encode_defunct

class CryptoAnalyzer:
    """Advanced cryptocurrency analysis and wallet management"""
    
    def __init__(self):
        self.patterns = {
            'bitcoin': r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}',
            'ethereum': r'0x[a-fA-F0-9]{40}',
            'monero': r'4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}',
            'ripple': r'r[0-9a-zA-Z]{24,34}',
            'litecoin': r'[LM][a-km-zA-HJ-NP-Z1-9]{26,33}',
            'dogecoin': r'D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}',
            'dash': r'X[1-9A-HJ-NP-Za-km-z]{33}',
            'solana': r'[1-9A-HJ-NP-Za-km-z]{32,44}'
        }
        self.mnemo = Mnemonic("english")
        self.w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

    def generate_seed_phrase(self, strength: int = 256) -> str:
        """Generate a BIP39 seed phrase"""
        return self.mnemo.generate(strength=strength)

    def verify_seed_phrase(self, seed_phrase: str) -> bool:
        """Verify if a seed phrase is valid"""
        return self.mnemo.check(seed_phrase)

    def seed_to_private_key(self, seed_phrase: str, path: str = "m/44'/60'/0'/0/0") -> str:
        """Convert seed phrase to private key"""
        seed = self.mnemo.to_seed(seed_phrase)
        root_key = BIP32Key.fromEntropy(seed)
        derived_key = root_key.ChildKey(44).ChildKey(60).ChildKey(0).ChildKey(0).ChildKey(0)
        return derived_key.PrivateKey().hex()

    def generate_wallet(self, type: str = "ethereum", strength: int = 256) -> Dict:
        """Generate a new cryptocurrency wallet"""
        try:
            if type == "ethereum":
                account = Account.create()
                return {
                    "address": account.address,
                    "private_key": account.key.hex(),
                    "type": "ethereum"
                }
            elif type == "bitcoin":
                seed = self.mnemo.generate(strength=strength)
                seed_bytes = self.mnemo.to_seed(seed)
                root_key = BIP32Key.fromEntropy(seed_bytes)
                # Derive Bitcoin address using BIP44
                child_key = root_key.ChildKey(44).ChildKey(0).ChildKey(0).ChildKey(0).ChildKey(0)
                return {
                    "address": child_key.Address(),
                    "private_key": child_key.WalletImportFormat(),
                    "seed_phrase": seed,
                    "type": "bitcoin"
                }
            else:
                return {"error": "Unsupported wallet type"}
        except Exception as e:
            return {"error": str(e)}

    def analyze_wallet(self, address: str, network: str = "ethereum") -> Dict:
        """Analyze a cryptocurrency wallet"""
        try:
            if network == "ethereum":
                balance = self.w3.eth.get_balance(address)
                code = self.w3.eth.get_code(address)
                nonce = self.w3.eth.get_transaction_count(address)
                
                return {
                    "balance": self.w3.from_wei(balance, 'ether'),
                    "is_contract": len(code) > 0,
                    "transaction_count": nonce,
                    "network": network
                }
            elif network == "bitcoin":
                response = requests.get(f"https://blockchain.info/rawaddr/{address}")
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "total_received": data.get("total_received"),
                        "total_sent": data.get("total_sent"),
                        "balance": data.get("final_balance"),
                        "transaction_count": data.get("n_tx"),
                        "network": network
                    }
            return {"error": "Unsupported network"}
        except Exception as e:
            return {"error": str(e)}

    def sign_message(self, private_key: str, message: str) -> Dict:
        """Sign a message with a private key"""
        try:
            account = Account.from_key(private_key)
            message_hash = encode_defunct(text=message)
            signed_message = account.sign_message(message_hash)
            
            return {
                "message": message,
                "signature": signed_message.signature.hex(),
                "signer": account.address
            }
        except Exception as e:
            return {"error": str(e)}

    def verify_signature(self, message: str, signature: str, address: str) -> Dict:
        """Verify a signed message"""
        try:
            message_hash = encode_defunct(text=message)
            recovered_address = Account.recover_message(message_hash, signature=signature)
            
            return {
                "is_valid": recovered_address.lower() == address.lower(),
                "recovered_address": recovered_address
            }
        except Exception as e:
            return {"error": str(e)}

    def extract_addresses(self, content: str) -> Dict[str, List[str]]:
        """Extract cryptocurrency addresses from text"""
        results = {}
        for currency, pattern in self.patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                results[currency] = list(set(matches))
        return results
