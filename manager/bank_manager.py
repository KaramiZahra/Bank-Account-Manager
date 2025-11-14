from .accounts import Account, SavingAccount, CheckingAccount
from pathlib import Path
import json
from tabulate import tabulate
from datetime import datetime
from collections import defaultdict


class BankManager:
    FILE_PATH = Path('accounts.json')

    def __init__(self, accounts=None, transactions=None):
        self.accounts = accounts if accounts is not None else []
        self.transactions = transactions if transactions is not None else []
        self.load_accounts()

    def load_accounts(self):
        if self.FILE_PATH.exists():
            with open(self.FILE_PATH, 'r') as af:
                try:
                    data = json.load(af)

                    accounts_data = data.get("accounts", [])
                    loaded_data = [Account.from_dict(d) for d in accounts_data]
                    self.accounts.extend(loaded_data)

                    transactions_data = data.get("transactions", [])
                    self.transactions.extend(transactions_data)

                    for acc in self.accounts:
                        if isinstance(acc, SavingAccount):
                            interest = acc.apply_interest()
                            if interest > 0:
                                self._record_transactions(
                                    acc.account_number, "interest", interest)

                except json.JSONDecodeError:
                    self.accounts.clear()
                    self.transactions.clear()
        else:
            self.FILE_PATH.touch()
            self.accounts = []
            self.transactions = []

    def save_accounts(self):
        with open(self.FILE_PATH, 'w') as af:
            json.dump({"accounts": [acc.to_dict(
            ) for acc in self.accounts], "transactions": self.transactions}, af, indent=4)

    @staticmethod
    def _get_float(prompt):
        while True:
            try:
                value = float(input(prompt))
                if value <= 0:
                    print("Value must be positive.")
                    continue
                return value
            except ValueError:
                print("Invalid number.")

    def create_account(self):
        acc_number = input("Enter your account number: ").strip()
        acc_name = input("Enter your account name: ").strip()

        acc_balance = self._get_float("Enter your account balance: ")

        acc_password = input("Set a password for your account: ").strip()

        while True:
            acc_type = input(
                "What type (1.Savings Account 2.Checking Account) of account do you want? ")

            if acc_type == "1":
                acc_type = "Saving"

                acc_interest = self._get_float("Enter interest rate (%): ")

                new_acc = SavingAccount(acc_number, acc_name, acc_balance, acc_type, datetime.now(
                ).date().isoformat(), acc_password, acc_interest, datetime.now().date().isoformat())
                break

            elif acc_type == "2":
                acc_type = "Checking"

                acc_overdraft = self._get_float("Enter overdraft limit: ")

                new_acc = CheckingAccount(
                    acc_number, acc_name, acc_balance, acc_type, datetime.now().date().isoformat(), acc_password, acc_overdraft)
                break
            else:
                print("Invalid account type.")

        existing_numbers = {acc.account_number for acc in self.accounts}
        if new_acc.account_number in existing_numbers:
            print("Account number already exists.")
        else:
            self.accounts.append(new_acc)
            print("Account successfully created.")

    def _get_account(self, acc_number):
        return next((acc for acc in self.accounts if acc.account_number == acc_number), None)

    @staticmethod
    def _requires_authentication(func):
        def wrapper(self, *args, **kwargs):
            acc_number = input("Enter your account number: ").strip()
            acc = self._get_account(acc_number)
            if not acc:
                print("Account not found.")
                return

            acc_pass = input("Enter your account password: ").strip()
            if not acc.verify_password(acc_pass):
                print("Access denied.")
                return

            return func(self, acc, *args, **kwargs)
        return wrapper

    @_requires_authentication
    def deposit_amount(self, acc):
        while True:
            try:
                amount = float(input("Enter deposit amount: "))
                acc.deposit(amount)
                print(f"Deposit successful. New balance: {acc.balance}")
                self._record_transactions(
                    acc.account_number, "deposit", amount)
                break
            except ValueError as err:
                print(f"Deposit failed: {err}")

    @_requires_authentication
    def withdraw_amount(self, acc):
        while True:
            try:
                amount = float(input("Enter withdraw amount: "))
                acc.withdraw(amount)
                print(f"Withdraw successful. New balance: {acc.balance}")
                self._record_transactions(
                    acc.account_number, "withdraw", amount)
                break
            except ValueError as err:
                print(f"Withdraw failed: {err}")

    def transfer(self):
        src_number = input("Enter source account number: ").strip()
        dst_number = input("Enter destination account number: ").strip()

        if src_number == dst_number:
            print("Source and destination accounts cannot be the same.")
            return

        src_acc = self._get_account(src_number)
        dst_acc = self._get_account(dst_number)

        if not src_acc or not dst_acc:
            print("Accounts not found.")
            return

        acc_pass = input("Enter your account password: ").strip()

        if src_acc.verify_password(acc_pass):
            while True:
                try:
                    transfer_amount = float(
                        input("Enter transfer amount: "))
                    src_acc.withdraw(transfer_amount)
                    self._record_transactions(
                        src_number, "withdraw", transfer_amount)
                    dst_acc.deposit(transfer_amount)
                    self._record_transactions(
                        dst_number, "deposit", transfer_amount)
                    print(
                        f"Transfer successful. Source new balance: {src_acc.balance}. Destination new balance: {dst_acc.balance}")
                    break
                except ValueError as err:
                    print(f"Transfer failed: {err}")
        else:
            print("Access denied.")

    def show_accounts(self):
        if not self.accounts:
            print("No accounts available.")
            return

        grouped = defaultdict(list)
        for acc in self.accounts:
            grouped[acc.account_type].append(acc.to_dict())

        for acc_type, acc_list in grouped.items():
            filtered_list = [{key: value for key, value in acc.items(
            ) if key != "account_password"} for acc in acc_list]

            print(f"\n {acc_type} Accounts:")
            print(tabulate(filtered_list, headers="keys",
                  tablefmt="fancy_grid", colalign=("center", "left")))

    def delete_account(self):
        acc_number = input("Enter account number: ")

        acc = self._get_account(acc_number)
        if not acc:
            print("Account not found.")
            return

        self.accounts.remove(acc)
        print("Account successfully deleted.")

    def _record_transactions(self, acc_number, tran_type, amount):
        new_tran = {
            'account_number': acc_number,
            'transaction_type': tran_type,
            'amount': amount,
            'date': datetime.now().date().isoformat()
        }
        self.transactions.append(new_tran)

    def transactions_log(self):
        print("\n Transactions history: ")
        print(tabulate(self.transactions, headers="keys",
              tablefmt="fancy_grid", colalign=("center", "left")))

    def search_account(self):
        query = input("Enter holder name: ").strip()
        found = False

        for acc in self.accounts:
            if acc.holder_name.lower().startswith(query):
                print(tabulate([acc.to_dict()], headers="keys",
                      tablefmt="fancy_grid", colalign=("center", "left")))
                found = True

        if not found:
            print("Account not found.")
