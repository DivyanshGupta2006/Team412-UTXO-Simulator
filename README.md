# CS 216: Bitcoin Transaction & UTXO Simulator

**Course:** CS 216: Introduction to Blockchain  
**Instructor:** Prof. Subhra Mazumdar  

## Team Information
**Team Name:** 412  

**Members:**
* **Divyansh Gupta** -  240041015
* **Harsh Mahajan** -   240001034
* **Darsh Chaudhary** - 240004014
* **Akarsh J** -        240002007

---

## Project Overview
This project is a functional simulator of Bitcoin's transaction system, developed to demonstrate the core mechanisms of the **UTXO (Unspent Transaction Output)** model. It focuses on the logic of transaction validation, memory pool management, and block mining within a local environment, without the complexity of a distributed network or real cryptography.

The simulator implements the following core components:
* **UTXO Manager:** A centralized "database" that tracks all spendable coins (UTXOs) and their owners.
* **Transaction Validation:** Enforces Bitcoin's rules, ensuring inputs exist, signatures are valid (simulated), and no double-spending occurs.
* **Mempool Management:** Manages unconfirmed transactions, detecting conflicts and preventing race attacks via a "first-seen" rule.
* **Mining Simulation:** Simulates the confirmation process by selecting transactions from the mempool, updating the UTXO set permanently, and awarding transaction fees to miners.
* **Double-Spending Prevention:** Robust checks to reject transactions attempting to spend the same UTXO twice, both within the mempool and against the confirmed blockchain state.

## Repository Structure
The project is organized as follows:

```text
src/
├── main.py              # Main program entry point & Menu interface
├── utxo_manager.py      # UTXO handling class
├── transaction.py       # Transaction data structure
├── mempool.py           # Mempool management & conflict detection
├── validator.py         # Transaction validation logic
├── block.py             # Mining and fee distribution logic
├── tests/
│   └── test_scenarios.py # Implementation of 10 mandatory test cases
├── README.md            # Project documentation
└── sample_output.txt    # Screenshot/text log of a demo run
```
## Installation & Usage

### Prerequisites
* **Python:** Version 3.8+ recommended.
* **Dependencies:** Standard Python libraries only (no external packages like `bitcoinlib` or `pycoin` are used).

### Running the Simulator
1. Clone the repository and navigate to the project folder.
   
   ```bash
   git clone https://github.com/DivyanshGupta2006/Team412-UTXO-Simulator.git
   cd Team412-UTXO-Simulator
   ```
2. Enter the source directory:
   
   ```bash
   cd src
   ```
3. Run the main program
   
   ```bash
   python main.py
   ```
