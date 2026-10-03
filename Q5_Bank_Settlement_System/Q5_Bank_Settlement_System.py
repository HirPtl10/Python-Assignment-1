import sys
from typing import Dict, List, Optional, Tuple, Any

class BankException(Exception):
    pass

class InsufficientBalanceException(BankException):
    pass

class AccountNotFoundException(BankException):
    pass

class InvalidAmountException(BankException):
    pass

class Transaction:
    def __init__(self, tx_type: str, from_acc: Optional[str], to_acc: Optional[str], amount: int):
        self.tx_type = tx_type
        self.from_acc = from_acc
        self.to_acc = to_acc
        self.amount = amount

class Account:
    def __init__(self, account_id: str, initial_balance: int):
        self._account_id = account_id
        if initial_balance < 0:
            raise InvalidAmountException("Initial balance cannot be negative.")
        self._balance = initial_balance

    @property
    def account_id(self) -> str:
        return self._account_id

    @property
    def balance(self) -> int:
        return self._balance

    def deposit(self, amount: int):
        if amount <= 0:
            raise InvalidAmountException("Deposit amount must be positive.")
        self._balance += amount

    def withdraw(self, amount: int):
        if amount <= 0:
            raise InvalidAmountException("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise InsufficientBalanceException("Insufficient balance.")
        self._balance -= amount

    def clone(self) -> 'Account':
        return Account(self._account_id, self._balance)

class Bank:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.transaction_history: List[Transaction] = []
        self.in_batch: bool = False
        self.current_batch_ops: List[str] = []
        self.batch_count: int = 0
        self.failed_batches: List[int] = []
        self._batch_snapshot: Optional[Dict[str, int]] = None

    def add_account(self, account_id: str, balance: int):
        self.accounts[account_id] = Account(account_id, balance)

    def get_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            raise AccountNotFoundException(f"Account '{account_id}' not found.")
        return self.accounts[account_id]

    def deposit(self, account_id: str, amount: int):
        acc = self.get_account(account_id)
        acc.deposit(amount)
        self.transaction_history.append(Transaction("DEPOSIT", None, account_id, amount))

    def withdraw(self, account_id: str, amount: int):
        acc = self.get_account(account_id)
        acc.withdraw(amount)
        self.transaction_history.append(Transaction("WITHDRAW", account_id, None, amount))

    def transfer(self, from_id: str, to_id: str, amount: int):
        from_acc = self.get_account(from_id)
        to_acc = self.get_account(to_id)
        if amount <= 0:
            raise InvalidAmountException("Transfer amount must be positive.")
        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        self.transaction_history.append(Transaction("TRANSFER", from_id, to_id, amount))

    def process_operation(self, op_line: str):
        tokens = op_line.strip().split()
        if not tokens:
            return

        cmd = tokens[0].upper()

        if cmd == "BATCH_BEGIN":
            if self.in_batch:
                raise BankException("Nested BATCH_BEGIN is not supported.")
            self.in_batch = True
            self.batch_count += 1
            self._batch_snapshot = {acc_id: acc.balance for acc_id, acc in self.accounts.items()}
            self.current_batch_ops = []

        elif cmd == "BATCH_END":
            if not self.in_batch:
                raise BankException("BATCH_END without BATCH_BEGIN.")
            
            batch_success = True
            for acc_id, snap_bal in self._batch_snapshot.items():
                self.accounts[acc_id]._balance = snap_bal

            for batch_op in self.current_batch_ops:
                b_tokens = batch_op.split()
                b_cmd = b_tokens[0].upper()
                try:
                    if b_cmd == "DEPOSIT":
                        self.deposit(b_tokens[1], int(b_tokens[2]))
                    elif b_cmd == "WITHDRAW":
                        self.withdraw(b_tokens[1], int(b_tokens[2]))
                    elif b_cmd == "TRANSFER":
                        self.transfer(b_tokens[1], b_tokens[2], int(b_tokens[3]))
                except BankException:
                    batch_success = False
                    break

            if not batch_success:
                for acc_id, snap_bal in self._batch_snapshot.items():
                    self.accounts[acc_id]._balance = snap_bal
                self.failed_batches.append(self.batch_count)

            self.in_batch = False
            self._batch_snapshot = None
            self.current_batch_ops = []

        else:
            if self.in_batch:
                self.current_batch_ops.append(op_line)
            else:
                try:
                    if cmd == "DEPOSIT":
                        self.deposit(tokens[1], int(tokens[2]))
                    elif cmd == "WITHDRAW":
                        self.withdraw(tokens[1], int(tokens[2]))
                    elif cmd == "TRANSFER":
                        self.transfer(tokens[1], tokens[2], int(tokens[3]))
                except BankException:
                    pass

    def get_summary_output(self) -> List[str]:
        output = []
        for b_num in self.failed_batches:
            output.append(f"FAILED {b_num}")
        for acc_id in sorted(self.accounts.keys()):
            output.append(f"{acc_id} {self.accounts[acc_id].balance}")
        return output

if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if lines:
        bank = Bank()
        n = int(lines[0])
        idx = 1
        for _ in range(n):
            parts = lines[idx].split()
            bank.add_account(parts[0], int(parts[1]))
            idx += 1
        q = int(lines[idx])
        idx += 1
        for _ in range(q):
            if idx < len(lines):
                bank.process_operation(lines[idx])
                idx += 1
        output = bank.get_summary_output()
        for line in output:
            print(line)
