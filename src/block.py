from src.mempool import Mempool
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

    txs_to_mine = mempool.get_top_transactions(num_txs)

    if not txs_to_mine:
        print("No transactions in mempool to mine.")
        return

    print("Mining block...")
    print(f"Selected {len(txs_to_mine)} transactions from mempool.")

    total_fee = 0.0
    valid_txs = []

    for tx in txs_to_mine:
        input_sum = 0.0
        valid_inputs = True

        for inp in tx["inputs"]:
            if utxo_manager.exists(inp["prev_tx"], inp["index"]):
                utxo = utxo_manager.utxo_set[(inp["prev_tx"], inp["index"])]
                input_sum += utxo["amount"]
            else:
                print(f"Skipping invalid tx {tx['tx_id']}: Input missing")
                valid_inputs = False
                break

        if not valid_inputs:
            continue

        for inp in tx["inputs"]:
            utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])

        output_sum = 0.0
        for i, out in enumerate(tx["outputs"]):
            output_sum += out["amount"]
            utxo_manager.add_utxo(tx["tx_id"], i, out["amount"], out["address"])

        total_fee += (input_sum - output_sum)
        valid_txs.append(tx)

    print(f"Total fees: {total_fee:.4f} BTC")

    if total_fee >= 0:
        coinbase_id = "coinbase_" + valid_txs[0]["tx_id"] if valid_txs else "coinbase_empty"
        utxo_manager.add_utxo(coinbase_id, 0, total_fee, miner_address)
        print(f"Miner {miner_address} receives {total_fee:.3f} BTC")

    print("Block mined successfully!")

    for tx in txs_to_mine:
        mempool.remove_transaction(tx["tx_id"])

    print(f"Removed {len(txs_to_mine)} transactions from mempool.")