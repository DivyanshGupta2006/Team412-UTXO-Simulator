
from utxo_manager import UTXOManager

def is_transaction_valid(tx_details: dict, utxo_manager: UTXOManager, mempool=None) -> bool:
    """
    Validate transaction against 5 strict rules:
    1. Inputs exist
    2. No double-spending in tx
    3. Inputs >= Outputs
    4. No negative outputs
    5. No Mempool Conflict
    """
    inputs = tx_details["inputs"]
    outputs = tx_details["outputs"]
    
    used_inputs_in_this_tx = set()
    total_input = 0.0
    
    for inp in inputs:
        utxo_key = (inp["prev_tx"], inp["index"])
        
        # Rule 1: Existence
        if not utxo_manager.exists(inp["prev_tx"], inp["index"]):
             return False
             
        # Verify Owner
        owner_in_utxo = utxo_manager.get_owner_of_utxo(inp["prev_tx"], inp["index"])
        if owner_in_utxo != inp["owner"]:
            return False

        # Rule 2: Double Spend in same Tx
        if utxo_key in used_inputs_in_this_tx:
            return False
        used_inputs_in_this_tx.add(utxo_key)

        # Rule 5: Mempool Conflict
        if mempool and utxo_key in mempool.spent_utxos:
            return False
            
        total_input += utxo_manager.get_value_of_utxo(inp["prev_tx"], inp["index"])

    # Rule 4: No negative outputs
    total_output = 0.0
    for out in outputs:
        if out["amount"] < 0:
            return False
        total_output += out["amount"]

    # Rule 3: Input Sum >= Output Sum
    if total_input < total_output:
        return False
        
    return True
