class Transaction:
    def __init__(self):
        self.transaction_details = {"tx_id": "",
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

    def get_fees(self, utxo_manager):
        total_input = 0
        for utxo in self.transaction_details["inputs"]:
            prev_tx = utxo["prev_tx"]
            index = utxo["index"]
            owner = utxo["owner"]

            utxo_owner = utxo_manager.get_owner_of_utxo(prev_tx, index)
            if utxo_owner != owner:
                raise ValueError("UTXO owner mismatch")
            total_input += utxo_manager.get_value_of_utxo(prev_tx, index)

        total_output = 0
        for output in self.transaction_details["outputs"]:
            total_output += output["amount"]

        return total_input - total_output

