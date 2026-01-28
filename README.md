# CS 216: Bitcoin Transaction & UTXO Simulator

## Team Information
* **Team Name:** 412
* **Members:**
    * **Divyansh Gupta** - 240041015
    * **Harsh Mahajan** - 240001034
    * **Darsh Chaudhary** - 240004014
    * **Akarsh J** - 240002007

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

