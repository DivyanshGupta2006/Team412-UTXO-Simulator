
from util import display_menu, Colors
from utxo_manager import UTXOManager
from mempool import Mempool
from transaction import Transaction
from block import mine_block, load_blockchain, save_blockchain
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Initialize Global State (Load from persistence)
utxo_manager = UTXOManager() 
mempool = Mempool()
blockchain = load_blockchain() 

def create_transaction_menu():
    print(f"\n {Colors.CYAN}--- Create New Transaction ---{Colors.RESET}")
    
    sender = input(f" Enter Sender Name (e.g. Alice): ").strip()
    if not sender: return

    balance = utxo_manager.get_balance(sender)
    print(f" {Colors.BLUE}Available Balance: {balance} BTC{Colors.RESET}")
    
    if balance <= 0:
        print(f" {Colors.RED}Error: Sender has no funds!{Colors.RESET}")
        return

    recipient = input(f" Enter Recipient Name: ").strip()
    try:
        amount = float(input(f" Enter Amount to Send: "))
        if amount <= 0:
            print(f" {Colors.RED}Amount must be positive!{Colors.RESET}")
            return
    except ValueError:
        print(f" {Colors.RED}Invalid amount format!{Colors.RESET}")
        return

    # Auto-calculate fee (0.001) for simplicity
    fee = 0.001
    target_total = amount + fee
    
    if balance < target_total:
        print(f" {Colors.RED}Insufficient funds! Need {target_total} (incl fee) but have {balance}{Colors.RESET}")
        return

    # Coin Selection (Accumulator strategy)
    sender_utxos = utxo_manager.get_utxos_for_owner(sender)
    selected_inputs = []
    input_sum = 0.0
    
    for utxo in sender_utxos:
        selected_inputs.append(utxo)
        input_sum += utxo["amount"]
        if input_sum >= target_total:
            break
            
    change = input_sum - target_total
    
    tx = Transaction()
    for inp in selected_inputs:
        tx.add_input(inp["tx_id"], inp["index"], inp["owner"])
        
    tx.add_output(amount, recipient)
    if change > 0:
        tx.add_output(change, sender)
        
    print(f" {Colors.DIM}Constructed Tx with {len(selected_inputs)} inputs (Sum: {input_sum}) and Change: {change:.4f}{Colors.RESET}")

    success, msg = mempool.add_transaction(tx, utxo_manager)
    if success:
        print(f" {Colors.GREEN}Success! Transaction added to Mempool.{Colors.RESET}")
        print(f" {Colors.DIM}Tx ID: {tx['tx_id']}{Colors.RESET}")
    else:
        print(f" {Colors.RED}Failed: {msg}{Colors.RESET}")

def view_utxo_set():
    print(f"\n {Colors.CYAN}--- Current UTXO Set ---{Colors.RESET}")
    if not utxo_manager.utxo_set:
        print(" (Empty)")
    else:
        sorted_utxos = sorted(utxo_manager.utxo_set.items(), key=lambda item: item[1][1]) 
        for (tx_id, idx), (amt, owner) in sorted_utxos:
            print(f" {Colors.YELLOW}[{owner}]{Colors.RESET} {amt:.4f} BTC  (Tx: {tx_id[:10]}... Idx: {idx})")

def view_mempool():
    print(f"\n {Colors.CYAN}--- Mempool ({len(mempool.transactions)} txs) ---{Colors.RESET}")
    if not mempool.transactions:
        print(" (Empty)")
    else:
        for tx in mempool.transactions:
             fee = tx.get_fees(utxo_manager) 
             print(f" {Colors.BLUE}{tx['tx_id']}{Colors.RESET} | Fee: {fee:.4f} | Inputs: {len(tx.get_input_info())}")

def view_blockchain():
    print(f"\n {Colors.CYAN}--- Blockchain ({len(blockchain)} blocks) ---{Colors.RESET}")
    if not blockchain:
        print(" (No blocks mined yet)")
    else:
        for block in blockchain:
            print(f" {Colors.GREEN}Block #{block.index}{Colors.RESET}")
            print(f"  Hash:      {Colors.DIM}{block.hash}{Colors.RESET}")
            print(f"  Prev:      {Colors.DIM}{block.prev_hash[:16]}...{Colors.RESET}")
            print(f"  Tx Count:  {len(block.transactions)}")
            print(f"  Timestamp: {block.timestamp}")
            print("  " + "-"*30)

def run_test_scenarios_wrapper():
    try:
        tests_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests')
        if tests_path not in sys.path:
            sys.path.append(tests_path)
        from test_scenarios import run_tests
        run_tests()
    except ImportError as e:
         print(f" {Colors.RED}Could not import tests: {e}{Colors.RESET}")

def run_mainmenu():
    while True:
        options = [
            'Create new transaction', 
            'View UTXO set', 
            'View mempool', 
            'Mine block', 
            'Run test scenarios', 
            'View entire blockchain', 
            'Exit'
        ]
        
        choice = display_menu(options, "Select an option:", "=== Bitcoin Transaction Simulator ===", False)
        
        if choice == 1:
            create_transaction_menu()
        elif choice == 2:
            view_utxo_set()
        elif choice == 3:
            view_mempool()
        elif choice == 4:
            miner_name = input(" Enter Miner Name: ")
            if not miner_name: miner_name = "Miner1"
            mine_block(miner_name, mempool, utxo_manager, blockchain)
        elif choice == 5:
            run_test_scenarios_wrapper()
        elif choice == 6:
            view_blockchain()
        elif choice == 7:
            print(f"\n {Colors.RED}Exiting...{Colors.RESET}")
            exit()
            
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

if __name__ == '__main__':
    run_mainmenu()
