class Mempool:
    def __init__(self, max_size=50):
        self.max_size = max_size
        self.transactions = []
        self.spent_utxos = set()

    def add_transaction(self, tx, utxo_manager) -> (bool, str):
        """Validate and add transaction. Return (success, message)."""
        if len(self.transactions) >= self.max_size:
            return (False, "Mempool is full")

        input_info = tx.get_input_info()
        utxos_to_spend = []

        for tx_input in input_info:
            utxo_key = (tx_input['prev_tx'], tx_input['index'])

            if utxo_key in self.spent_utxos:
                return (False, f"Double Spend: UTXO {utxo_key} is already pending in mempool")

            if not utxo_manager.exists(tx_input['prev_tx'], tx_input['index']):
                return (False, f"Invalid or Spent UTXO: {utxo_key}")

            utxos_to_spend.append(utxo_key)

        try:
            tx.fee = tx.get_fees(utxo_manager)
            if tx.fee < 0:
                return (False, "Invalid Transaction: Fee is negative")
        except ValueError as e:
            return (False, str(e))

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