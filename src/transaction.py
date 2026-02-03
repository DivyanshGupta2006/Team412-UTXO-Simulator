
import time
import random
from typing import List, Dict, Any

def generate_tx_id() -> str:
    return f"tx_{int(time.time())}_{random.randint(1000000, 9999999)}"

class Transaction:
    def __init__(self):
        self.transaction_details = {
            "tx_id": generate_tx_id(),
            "inputs": [],
            "outputs": []
        }
        self.fee = 0.0

    @staticmethod
    def create_transaction(inputs: List[Dict], outputs: List[Dict]) -> 'Transaction':
        """Factory method to create a transaction from lists of inputs and outputs."""
        tx = Transaction()
        for inp in inputs:
            tx.add_input(inp["prev_tx"], inp["index"], inp["owner"])  
        for out in outputs:
            tx.add_output(out["amount"], out["address"]) 
        return tx

    def add_input(self, prev_tx: str, index: int, owner: str):
        new_input = {
            "prev_tx": prev_tx,
            "index": index,
            "owner": owner
        }
        self.transaction_details["inputs"].append(new_input)

    def add_output(self, amount: float, address: str):
        new_output = {
            "amount": amount,
            "address": address
        }
        self.transaction_details["outputs"].append(new_output)

    def get_input_info(self) -> List[Dict]:
        return self.transaction_details["inputs"]
    
    # Enable dictionary-like access
    def __getitem__(self, key: str) -> Any:
        return self.transaction_details[key]

    def __setitem__(self, key: str, value: Any):
        self.transaction_details[key] = value

    def get_total_input(self, utxo_manager) -> float:
        total_input = 0.0
        for utxo in self.transaction_details["inputs"]:
            prev_tx = utxo["prev_tx"]
            index = utxo["index"]
            
            if utxo_manager.exists(prev_tx, index):
                total_input += utxo_manager.get_value_of_utxo(prev_tx, index)
            else:
                # Handled later by validator
                pass
        return total_input

    def get_total_output(self, utxo_manager=None) -> float:
        total_output = 0.0
        for output in self.transaction_details["outputs"]:
            total_output += output["amount"]
        return total_output

    def get_fees(self, utxo_manager) -> float:
        return self.get_total_input(utxo_manager) - self.get_total_output(utxo_manager)