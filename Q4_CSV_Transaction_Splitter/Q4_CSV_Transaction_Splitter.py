import csv
import os
import re
from collections import defaultdict
from typing import Dict, List, Tuple

TIMESTAMP_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

class TransactionValidationError(Exception):
    pass

def validate_row(row: Dict[str, str]) -> Tuple[str, str, str, float, str]:
    tid = row.get("tid", "").strip()
    acc = row.get("acc", "").strip()
    tx_type = row.get("type", "").strip().upper()
    raw_amount = row.get("amount", "").strip()
    raw_time = row.get("time", "").strip()

    if not tid:
        raise TransactionValidationError("Transaction ID (tid) cannot be empty")
    if not acc:
        raise TransactionValidationError("Account ID (acc) cannot be empty")
    if tx_type not in ("CREDIT", "DEBIT"):
        raise TransactionValidationError(f"Invalid type '{tx_type}', must be CREDIT or DEBIT")
    
    try:
        amount = float(raw_amount)
    except ValueError:
        raise TransactionValidationError(f"Amount '{raw_amount}' is not numeric")
        
    if amount <= 0:
        raise TransactionValidationError(f"Amount must be positive, got {amount}")
        
    if not TIMESTAMP_REGEX.match(raw_time):
        raise TransactionValidationError(f"Timestamp '{raw_time}' does not match ISO format yyyy-mm-ddThh:mm:ss")

    return tid, acc, tx_type, amount, raw_time

def process_transaction_csv(input_path: str, output_dir: str = ".") -> Tuple[str, str, str, Dict[str, float]]:
    credit_path = os.path.join(output_dir, "credit.csv")
    debit_path = os.path.join(output_dir, "debit.csv")
    error_path = os.path.join(output_dir, "error.csv")

    balances: Dict[str, float] = defaultdict(float)

    with open(input_path, mode="r", newline="", encoding="utf-8") as infile, \
         open(credit_path, mode="w", newline="", encoding="utf-8") as credfile, \
         open(debit_path, mode="w", newline="", encoding="utf-8") as debfile, \
         open(error_path, mode="w", newline="", encoding="utf-8") as errfile:

        reader = csv.DictReader(infile)
        
        fieldnames = reader.fieldnames or ["tid", "acc", "type", "amount", "time"]
        credit_writer = csv.DictWriter(credfile, fieldnames=fieldnames)
        debit_writer = csv.DictWriter(debfile, fieldnames=fieldnames)
        error_writer = csv.DictWriter(errfile, fieldnames=list(fieldnames) + ["reason"])

        credit_writer.writeheader()
        debit_writer.writeheader()
        error_writer.writeheader()

        for row in reader:
            try:
                tid, acc, tx_type, amount, timestamp = validate_row(row)
                clean_row = {"tid": tid, "acc": acc, "type": tx_type, "amount": str(amount), "time": timestamp}

                if tx_type == "CREDIT":
                    balances[acc] += amount
                    credit_writer.writerow(clean_row)
                elif tx_type == "DEBIT":
                    balances[acc] -= amount
                    debit_writer.writerow(clean_row)

            except TransactionValidationError as ve:
                err_row = dict(row)
                err_row["reason"] = str(ve)
                error_writer.writerow(err_row)
            except Exception as ex:
                err_row = dict(row)
                err_row["reason"] = f"Unexpected error: {ex}"
                error_writer.writerow(err_row)

    return credit_path, debit_path, error_path, balances

def display_summary(balances: Dict[str, float]):
    sorted_accs = sorted(balances.items(), key=lambda item: (-abs(item[1]), item[0]))
    for acc, net_amount in sorted_accs:
        formatted_val = int(net_amount) if net_amount == int(net_amount) else round(net_amount, 2)
        print(f"{acc} {formatted_val}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        c_path, d_path, e_path, balances = process_transaction_csv(sys.argv[1])
        display_summary(balances)
