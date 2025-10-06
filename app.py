from pathlib import Path
import json
from tabulate import tabulate


class Account:
    def __init__(self, account_number, holder_name, balance):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance

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
            'balance': self.balance
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['account_number'],
            data['holder_name'],
            data['balance']
        )


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
                except json.JSONDecodeError:
                    self.accounts.clear()
        else:
            self.FILE_PATH.touch()
            self.accounts = []

    def save_accounts(self):
        with open(self.FILE_PATH, 'w') as af:
            json.dump([acc.to_dict() for acc in self.accounts], af, indent=4)

    def create_account(self):
        acc_number = input("Enter your account number: ").strip()
        acc_name = input("Enter your account name: ").strip()

        while True:
            try:
                acc_balance = float(input("Enter your account balance: "))
                break
            except ValueError:
                print("Balance must be a number.")

        new_acc = Account(acc_number, acc_name, acc_balance)

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

        print(tabulate([acc.to_dict() for acc in self.accounts],
                       headers="keys", tablefmt="fancy_grid", colalign=("center", "left", "right")))

    def menu(self):
        while True:
            print("\n---Bank Account Manager---\n")
            print("1.Create Account")
            print("2.Deposit")
            print("3.Withdraw")
            print("4.Transfer")
            print("5.Show Accounts")
            print("6.Save and Exit")

            user_input = input("Choose an option(1-6): ")

            match user_input:
                case '1': self.create_account()
                case '2': self.deposit_amount()
                case '3': self.withdraw_amount()
                case '4': self.transfer()
                case '5': self.show_accounts()
                case '6':
                    self.save_accounts()
                    break
                case _: print("Invalid input.")


if __name__ == "__main__":
    bm = BankManager()
    bm.menu()
