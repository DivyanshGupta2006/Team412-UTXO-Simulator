
import json
import os
from pathlib import Path

class UTXOManager:
    def __init__(self):
        # Store UTXOs as dictionary : (tx_id , index) -> (amount , owner)
        self.utxo_set = {}
        
        self.root_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.root_dir / 'data' / 'utxo'
        self.data_path = self.data_dir / 'utxo.json'
        
        if self.data_path.exists():
            self.load()
        else:
            self._add_genesis_utxos()
            self.save()

    def _add_genesis_utxos(self):
        """Initialize with mandatory Genesis State."""
        genesis_data = [
            ("Alice", 50.0, 0),
            ("Bob", 30.0, 1),
            ("Charlie", 20.0, 2),
            ("David", 10.0, 3),
            ("Eve", 5.0, 4)
        ]
        for owner, amount, index in genesis_data:
            self.utxo_set[("genesis", index)] = (amount, owner)

    def add_utxo(self, tx_id: str, index: int, amount: float, owner: str):
        """Add a new UTXO to the set."""
        if amount < 0:
            raise ValueError("amount must be positive!")
        if index < 0:
            raise ValueError("index must be positive!")

        self.utxo_set[(tx_id, index)] = (amount, owner)

    def remove_utxo(self, tx_id: str, index: int):
        """Remove a UTXO (when spent)."""
        if (tx_id, index) in self.utxo_set:
            del self.utxo_set[(tx_id, index)]

    def get_balance(self, owner: str) -> float:
        """Calculate total balance for an address."""
        balance = 0.0
        for _, (amt, own) in self.utxo_set.items():
            if own == owner:
                balance += amt
        return balance

    def exists(self, tx_id: str, index: int) -> bool:
        """Check if UTXO exists and is unspent."""
        return (tx_id, index) in self.utxo_set

    def get_value_of_utxo(self, tx_id: str, index: int) -> float:
        if not self.exists(tx_id, index):
            raise ValueError("UTXO does not exist or Already spent")
        return self.utxo_set[(tx_id, index)][0]

    def get_owner_of_utxo(self, tx_id: str, index: int) -> str:
        if not self.exists(tx_id, index):
            raise ValueError("UTXO does not exist")
        return self.utxo_set[(tx_id, index)][1]

    def get_utxos_for_owner(self, owner: str) -> list:
        utxos = []
        for (tx_id, ind), (amt, own) in self.utxo_set.items():
            if own == owner:
                utxos.append({
                    "tx_id": tx_id,
                    "index": ind,
                    "amount": amt,
                    "owner": own
                })
        return utxos

    def save(self):
        """Save the UTXOs to JSON."""
        os.makedirs(self.data_dir, exist_ok=True)
        # Convert tuple keys to string keys for JSON compatibility
        data_to_save = {}
        for (tx_id, index), val in self.utxo_set.items():
            key = f"{tx_id}:{index}"
            data_to_save[key] = val
            
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def load(self):
        """Load the UTXOs from JSON."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                
            self.utxo_set = {}
            for key, val in data.items():
                tx_id, index_str = key.rsplit(":", 1)
                index = int(index_str)
                self.utxo_set[(tx_id, index)] = (val[0], val[1])
                
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading UTXOs: {e}. Re-initializing Genesis.")
            self._add_genesis_utxos()