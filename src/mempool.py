
from validator import is_transaction_valid
from typing import Tuple

class Mempool:
    def __init__(self, max_size: int = 50):
        self.max_size = max_size
        self.transactions = []
        self.spent_utxos = set()

    def add_transaction(self, tx, utxo_manager) -> Tuple[bool, str]:
        """Validate and add transaction. Return (success, message)."""
        if len(self.transactions) >= self.max_size:
            return (False, "Mempool is full")
            
        # Strict Validation 
        if not is_transaction_valid(tx.transaction_details, utxo_manager, self):
            return (False, "Transaction Verification Failed (See strict rules)")

        try:
            tx.fee = tx.get_fees(utxo_manager)
        except ValueError as e:
            return (False, str(e))

        input_info = tx.get_input_info()
        utxos_to_spend = []
        for tx_input in input_info:
            utxo_key = (tx_input['prev_tx'], tx_input['index'])
            utxos_to_spend.append(utxo_key)

        self.transactions.append(tx)
        self.spent_utxos.update(utxos_to_spend)

        return (True, "Transaction added")

    def remove_transaction(self, tx_id: str):
        """Remove transaction and clear its UTXOs from spent_set."""
        tx_to_remove = None

        for tx in self.transactions:
            if tx.transaction_details["tx_id"] == tx_id:
                tx_to_remove = tx
                break

        if tx_to_remove:
            self.transactions.remove(tx_to_remove)
            input_info = tx_to_remove.get_input_info()
            for tx_input in input_info:
                utxo_key = (tx_input['prev_tx'], tx_input['index'])
                if utxo_key in self.spent_utxos:
                    self.spent_utxos.remove(utxo_key)

    def get_top_transactions(self, n: int) -> list:
        """Return top N transactions by fee (highest first)."""
        sorted_txs = sorted(self.transactions, key=lambda tx: tx.fee, reverse=True)
        return sorted_txs[:n]

    def clear(self):
        """Clear all transactions."""
        self.transactions = []
        self.spent_utxos.clear()