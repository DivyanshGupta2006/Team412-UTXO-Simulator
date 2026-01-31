import time
import random


def generate_tx_id():
    return f"tx_{int(time.time())}_{random.randint(1000000, 9999999)}"

class Transaction:
    def __init__(self):
        self.transaction_details = {"tx_id": generate_tx_id(),
                                    "inputs": [],
                                    "outputs": []}

    def add_input(self, prev_tx, index, owner):
        new_input = {
            "prev_tx": prev_tx,
            "index": index,
            "owner": owner
        }
        self.transaction_details["inputs"].append(new_input)

    def add_output(self, amount, address):
        new_output = {
            "amount": amount,
            "address": address
        }
        self.transaction_details["outputs"].append(new_output)

