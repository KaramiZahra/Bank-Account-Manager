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
        self.accounts = []
        self.load_accounts()

        if accounts:
            existing_numbers = {acc.account_number for acc in self.accounts}
            for acc in accounts:
                if acc.account_number not in existing_numbers:
                    self.accounts.append(acc)

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


acc1 = Account(1, 'Jim', 200)
acc2 = Account(2, 'John', 250)
acc3 = Account(2, 'Jack', 300)

bm = BankManager([acc1, acc2, acc3])
bm.save_accounts()
