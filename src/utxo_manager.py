class UTXOManager:
    def __init__(self):
        # Store UTXOs as dictionary : (tx_id , index) -> (amount , owner)
        self.utxo_set = {}

    def add_utxo(self, tx_id, index, amount, owner):
        """ Add a new UTXO to the set """
        if amount < 0:
            raise ValueError("amount must be positive!")

        if index < 0:
            raise ValueError("index must be positive!")

        if not (tx_id.startswith("tx_") and tx_id[-7:].isdigit()):
            raise ValueError("tx_id must be valid!")

        # TODO: Add check for valid owner

        self.utxo_set[(tx_id, index)] = (amount, owner)

    def remove_utxo(self, tx_id: str, index: int):
        """ Remove a UTXO (when spent) """
        del self.utxo_set[(tx_id, index)]

    def get_balance(self, owner: str) -> float:
        """ Calculate total balance for an address """
        balance = 0.0
        for _, (amt, own) in self.utxo_set.items():
            if own == owner:
                balance += amt
        return balance

    def exists(self, tx_id: str, index: int) -> bool:
        """ Check if UTXO exists and is unspent """
        if (tx_id, index) in self.utxo_set:
            return True
        return False

    def get_utxos_for_owner(self, owner: str) -> list:
        """ Get all UTXOs owned by an address """
        utxos = []
        for (tx_id, ind), (amt, own) in self.utxo_set.items():
            if own == owner:
                utxos.append({
                    (tx_id, ind): (amt, own)
                })
        return utxos