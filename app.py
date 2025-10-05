from pathlib import Path
import json


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

    def save_accounts(self):
        with open(self.FILE_PATH, 'w') as af:
            json.dump([acc.to_dict() for acc in self.accounts], af, indent=4)

    def create_account(self):
        acc_number = input("Enter your account number: ")
        acc_name = input("Enter your account name: ")

        while True:
            try:
                acc_balance = float(input("Enter your account balance: "))
                break
            except ValueError:
                print("Balance must be a number.")

        new_acc = Account(acc_number, acc_name, acc_balance)

        existing_numbers = {acc.account_number for acc in self.accounts}
        if new_acc.account_number in existing_numbers:
            print("\nAccount number already exists.")
        else:
            self.accounts.append(new_acc)
            print("\nAccount successfully created.")

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

            if user_input == '1':
                self.create_account()
            elif user_input == '2':
                pass
            elif user_input == '3':
                pass
            elif user_input == '4':
                pass
            elif user_input == '5':
                pass
            elif user_input == '6':
                self.save_accounts()
                break
            else:
                print("Invalid input.")


if __name__ == "__main__":
    bm = BankManager()
    bm.menu()

#   for acc in bm.accounts:
#       print(vars(acc))
