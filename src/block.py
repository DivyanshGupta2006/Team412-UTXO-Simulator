
import hashlib
import time
import json
import os
from pathlib import Path
from src.mempool import Mempool
from src.utxo_manager import UTXOManager
from src.util import display_msg, Colors

class Block:
    def __init__(self, index: int, transactions: list, prev_hash: str, timestamp: float = None, hash: str = None):
        self.index = index
        self.timestamp = timestamp if timestamp else time.time()
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.hash = hash if hash else self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculates the SHA-256 hash of the block header."""
        tx_ids = [tx['tx_id'] for tx in self.transactions]
        block_string = f"{self.index}{self.timestamp}{tx_ids}{self.prev_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "prev_hash": self.prev_hash,
            "hash": self.hash
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            index=data["index"],
            transactions=data["transactions"],
            prev_hash=data["prev_hash"],
            timestamp=data["timestamp"],
            hash=data["hash"]
        )

def get_blockchain_path() -> Path:
    root_dir = Path(__file__).resolve().parent.parent
    return root_dir / 'data' / 'blockchain' / 'blockchain.json'

def save_blockchain(blockchain: list):
    path = get_blockchain_path()
    os.makedirs(path.parent, exist_ok=True)
    data = [block.to_dict() for block in blockchain]
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def load_blockchain() -> list:
    path = get_blockchain_path()
    if not path.exists():
        return []
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return [Block.from_dict(b_data) for b_data in data]
    except (json.JSONDecodeError, ValueError):
        return []

def mine_block(miner_address: str, mempool: Mempool, utxo_manager: UTXOManager, blockchain: list, num_txs: int = 5):
    """Simulate mining: Select txs, update UTXO, add coinbase, and append to chain."""
    
    # 1. Select top transactions
    txs_to_mine = mempool.get_top_transactions(num_txs)
    if not txs_to_mine:
        print(f" {Colors.YELLOW}No transactions in mempool to mine.{Colors.RESET}")
        return

    print(f" {Colors.CYAN}Mining block...{Colors.RESET}")
    print(f" Selected {len(txs_to_mine)} transactions from mempool.")

    total_fee = 0.0
    valid_txs_data = [] 

    # 2. Process Transactions
    for tx_obj in txs_to_mine:
        tx_data = tx_obj.transaction_details
        inputs = tx_data["inputs"]
        outputs = tx_data["outputs"]
        
        try:
            input_sum = tx_obj.get_total_input(utxo_manager)
            output_sum = tx_obj.get_total_output(utxo_manager)
            fee = input_sum - output_sum
        except ValueError:
             print(f" {Colors.RED}Skipping tx {tx_data['tx_id']}: Error calculating values.{Colors.RESET}")
             continue

        for inp in inputs:
            utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])

        for i, out in enumerate(outputs):
            utxo_manager.add_utxo(tx_data["tx_id"], i, out["amount"], out["address"])

        total_fee += fee
        valid_txs_data.append(tx_data)

    print(f" Total fees: {total_fee:.4f} BTC")

    # 3. Coinbase Transaction
    if total_fee >= 0:
        coinbase_tx_id = f"coinbase_{int(time.time())}_{miner_address}"
        utxo_manager.add_utxo(coinbase_tx_id, 0, total_fee, miner_address)
        print(f" Miner {miner_address} receives {total_fee:.3f} BTC")
        
        coinbase_tx = {
            "tx_id": coinbase_tx_id,
            "inputs": [],
            "outputs": [{"amount": total_fee, "address": miner_address}]
        }
        valid_txs_data.insert(0, coinbase_tx)

    # 4. Remove from Mempool
    for tx_obj in txs_to_mine:
        mempool.remove_transaction(tx_obj.transaction_details["tx_id"])
        
    # 5. Create and Append Block
    prev_hash = blockchain[-1].hash if blockchain else "0" * 64
    new_block = Block(len(blockchain) + 1, valid_txs_data, prev_hash)
    blockchain.append(new_block)
    
    print(f" {Colors.GREEN}Block #{new_block.index} mined successfully! Hash: {new_block.hash[:16]}...{Colors.RESET}")
    
    # 6. Save State
    utxo_manager.save()
    save_blockchain(blockchain)
    print(f" {Colors.DIM}State saved to disk.{Colors.RESET}")