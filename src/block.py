# from src.mempool import Mempool
from src.utxo_manager import UTXOManager


class Block:
    def __init__(self):
        self.block = None

def mine_block(miner_address: str, mempool: Mempool, utxo_manager: UTXOManager, num_txs=5):
    """
    Simulate mining a block.
    1. Select top transactions from mempool
    2. Update UTXO set (remove inputs, add outputs)
    3. Add miner fee as special UTXO
    4. Remove mined transactions from mempool
    """
    