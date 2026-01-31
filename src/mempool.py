class Mempool:
    def __init__(self, max_size=50):
        self.max_size = max_size
        self.transactions = []
        self.spent_utxos = set()

    def add_transaction(self, tx, utxo_manager):
        """Validate and add transaction. Return (success, message)."""
        pass

    def remove_transaction(self, tx_id:str):
        """Remove transaction (when mined)"""
        pass

    def get_top_transactions(self, n:int) -> list:
        """Return top N transactions by fee (highest first)."""
        pass

    def clear(self):
        """Clear all transactions."""
        pass