from pathlib import Path
import json
from tabulate import tabulate
from datetime import datetime, timedelta
from collections import defaultdict


class Account:
    def __init__(self, account_number, holder_name, balance, account_type, creation_date):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance
        self.account_type = account_type
        self.creation_date = creation_date or datetime.now().date().isoformat()

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        return self.balance

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'holder_name': self.holder_name,
            'balance': self.balance,
            'account_type': self.account_type,
            'creation_date': self.creation_date
        }

    @classmethod
    def from_dict(cls, data):
        acc_type = data.get('account_type')

        if acc_type == "Saving":
            return SavingAccount.from_dict(data)
        elif acc_type == "Checking":
            return CheckingAccount.from_dict(data)
        else:
            return cls(
                data['account_number'],
                data['holder_name'],
                data['balance'],
                acc_type,
                data['creation_date'],
            )


class SavingAccount(Account):
    def __init__(self, account_number, holder_name, balance, account_type, creation_date, interest_rate, last_interest_date):
        super().__init__(account_number, holder_name, balance, account_type, creation_date)
        self.interest_rate = interest_rate
        self.last_interest_date = last_interest_date

    def to_dict(self):
        data = super().to_dict()
        data['interest_rate'] = self.interest_rate
        data['last_interest_date'] = self.last_interest_date
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['account_number'],
            data['holder_name'],
            data['balance'],
            data['account_type'],
            data['creation_date'],
            data['interest_rate'],
            data['last_interest_date']
        )

    def apply_interest(self):
        if datetime.now().date() - datetime.fromisoformat(self.last_interest_date).date() >= timedelta(days=365):
            self.balance += self.balance * self.interest_rate / 100
            self.last_interest_date = datetime.now().date().isoformat()


class CheckingAccount(Account):
    def __init__(self, account_number, holder_name, balance, account_type, creation_date, overdraft_limit):
        super().__init__(account_number, holder_name, balance, account_type, creation_date)
        self.overdraft_limit = overdraft_limit

    def to_dict(self):
        data = super().to_dict()
        data['overdraft_limit'] = self.overdraft_limit
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['account_number'],
            data['holder_name'],
            data['balance'],
            data['account_type'],
            data['creation_date'],
            data['overdraft_limit']
        )

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance + self.overdraft_limit:
            raise ValueError("Overdraft limit exceeded.")
        self.balance -= amount
        return self.balance


class BankManager:
    FILE_PATH = Path('accounts.json')

    def __init__(self, accounts=None):
        self.accounts = accounts if accounts is not None else []
        self.load_accounts()

    def load_accounts(self):
        if self.FILE_PATH.exists():
            with open(self.FILE_PATH, 'r') as af:
                try:
                    data = json.load(af)
                    loaded_data = [Account.from_dict(d) for d in data]
                    self.accounts.extend(loaded_data)

                    for acc in self.accounts:
                        if isinstance(acc, SavingAccount):
                            acc.apply_interest()

                except json.JSONDecodeError:
                    self.accounts.clear()
        else:
            self.FILE_PATH.touch()
            self.accounts = []

    def save_accounts(self):
        with open(self.FILE_PATH, 'w') as af:
            json.dump([acc.to_dict() for acc in self.accounts], af, indent=4)

    @staticmethod
    def get_float(prompt):
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

        acc_balance = self.get_float("Enter your account balance: ")

        while True:
            acc_type = input(
                "What type (1.Savings Account 2.Checking Account) of account do you want? ")

            if acc_type == "1":
                acc_type = "Saving"

                acc_interest = self.get_float("Enter interest rate (%): ")

                new_acc = SavingAccount(acc_number, acc_name, acc_balance, acc_type, datetime.now(
                ).date().isoformat(), acc_interest, datetime.now().date().isoformat())
                break

            elif acc_type == "2":
                acc_type = "Checking"

                acc_overdraft = self.get_float("Enter overdraft limit: ")

                new_acc = CheckingAccount(
                    acc_number, acc_name, acc_balance, acc_type, datetime.now().date().isoformat(), acc_overdraft)
                break
            else:
                print("Invalid account type.")

        existing_numbers = {acc.account_number for acc in self.accounts}
        if new_acc.account_number in existing_numbers:
            print("Account number already exists.")
        else:
            self.accounts.append(new_acc)
            print("Account successfully created.")

    def get_account(self, acc_number):
        return next((acc for acc in self.accounts if acc.account_number == acc_number), None)

    def deposit_amount(self):
        acc_number = input("Enter your account number: ").strip()

        acc = self.get_account(acc_number)
        if not acc:
            print("Account not found.")
            return

        while True:
            try:
                amount = float(input("Enter deposit amount: "))
                acc.deposit(amount)
                print(f"Deposit successful. New balance: {acc.balance}")
                break
            except ValueError as err:
                print(f"Deposit failed: {err}")

    def withdraw_amount(self):
        acc_number = input("Enter your account number: ").strip()

        acc = self.get_account(acc_number)
        if not acc:
            print("Account not found.")
            return

        while True:
            try:
                amount = float(input("Enter withdraw amount: "))
                acc.withdraw(amount)
                print(f"Withdraw successful. New balance: {acc.balance}")
                break
            except ValueError as err:
                print(f"Withdraw failed: {err}")

    def transfer(self):
        src_number = input("Enter source account number: ").strip()
        dst_number = input("Enter destination account number: ").strip()

        if src_number == dst_number:
            print("Source and destination accounts cannot be the same.")
            return

        src_acc = self.get_account(src_number)
        dst_acc = self.get_account(dst_number)

        if src_acc and dst_acc:
            while True:
                try:
                    transfer_amount = float(input("Enter transfer amount: "))
                    src_acc.withdraw(transfer_amount)
                    dst_acc.deposit(transfer_amount)
                    print(
                        f"Transfer successful. Source new balance: {src_acc.balance}. Destination new balance: {dst_acc.balance}")
                    break
                except ValueError as err:
                    print(f"Transfer failed: {err}")
        else:
            print("Accounts not found.")

    def show_accounts(self):
        if not self.accounts:
            print("No accounts available.")
            return

        grouped = defaultdict(list)
        for acc in self.accounts:
            grouped[acc.account_type].append(acc.to_dict())

        for acc_type, acc_list in grouped.items():
            print(f"\n {acc_type} Accounts:")
            print(tabulate(acc_list, headers="keys",
                  tablefmt="fancy_grid", colalign=("center", "left")))

    def delete_account(self):
        acc_number = input("Enter account number: ")

        acc = self.get_account(acc_number)
        if not acc:
            print("Account not found.")
            return

        self.accounts.remove(acc)
        print("Account successfully deleted.")

    def menu(self):
        while True:
            print("\n---Bank Account Manager---\n")
            print("1.Create Account")
            print("2.Deposit")
            print("3.Withdraw")
            print("4.Transfer")
            print("5.Show Accounts")
            print("6.Delete Account")
            print("7.Save and Exit")

            user_input = input("Choose an option(1-7): ")

            match user_input:
                case '1': self.create_account()
                case '2': self.deposit_amount()
                case '3': self.withdraw_amount()
                case '4': self.transfer()
                case '5': self.show_accounts()
                case '6': self.delete_account()
                case '7':
                    self.save_accounts()
                    break
                case _: print("Invalid input.")


if __name__ == "__main__":
    bm = BankManager()
    bm.menu()
