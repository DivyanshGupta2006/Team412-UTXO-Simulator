from utxo_manager import UTXOManager

def is_transaction_valid(self, utxo_manager: UTXOManager):
    check1 = True
    input_list = self.transaction_details["inputs"]
    # this input_dict is a list of dictionaries
    for input_dict in input_list:
        utxo_key = (input_dict["prev_tx"], input_dict["index"])
        if utxo_key not in utxo_manager.utxo_set:
            check1 = False

        amt, actual_owner = utxo_manager.utxo_set[utxo_key]
        if actual_owner != input_dict["owner"]:
            check1 = False

    check2 = True
    seen_inputs = set()
    for dicti in input_list:
        utxo_key = (dicti["prev_tx"], dicti["index"])

        if utxo_key in seen_inputs:
            check2 = False
        seen_inputs.add(utxo_key)
    check3 = False
    sum_of_inputs = 0
    for input_dict in input_list:
        summ, own = utxo_manager.utxo_set[(input_dict["prev_tx"], input_dict["index"])]
        sum_of_inputs += summ

    sum_of_outputs = 0
    output_list = self.transaction_details["outputs"]
    # this output_list is also a list of dictionaries
    for output_dict in output_list:
        sum_of_outputs += output_dict["amount"]

    fee = sum_of_inputs - sum_of_outputs
    if fee >= 0:
        check3 = True

    check4 = True
    # no negative amounts in outputs
    for output_dict in output_list:
        if output_dict["amount"] < 0:
            check4 = False

    check5 = False
    # TODO: Validation Check Number 5

    return check1 and check2 and check3 and check4 and check5
