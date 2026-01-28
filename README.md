# CS 216: Bitcoin Transaction & UTXO Simulator

## Team Information
* **Team Name:** 412
* **Members:**
    * **Divyansh Gupta** - 240041015
    * **Harsh Mahajan** - 240001034
    * **Darsh Chaudhary** - 240004014
    * **Akarsh J** - 240002007

---

## Project Overview
[cite_start]This project is a simplified, local simulation of Bitcoin's transaction system[cite: 18, 29]. [cite_start]It focuses on the logic of the **UTXO (Unspent Transaction Output)** model, transaction validation, and the prevention of double-spending[cite: 18, 30]. [cite_start]The simulator manages a mempool for unconfirmed transactions and mimics the mining process to finalize them into a permanent state[cite: 50, 58].

### Learning Objectives
* [cite_start]Implementation of Bitcoin's transaction validation rules[cite: 23].
* [cite_start]Demonstrating double-spending prevention[cite: 24].
* [cite_start]Simulating the lifecycle from transaction creation to confirmation[cite: 25].

---

## Repository Structure
[cite_start]The project is organized as per the technical requirements:
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
