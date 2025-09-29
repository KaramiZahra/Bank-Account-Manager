from pathlib import Path


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
    def __init__(self, accounts, file_path):
        self.accounts = accounts
        self.file_path = Path(file_path)

    def save_accounts(self):
        pass

    def load_accounts(self):
        pass


acc = Account(1, 'Jim', 200)
acc.deposit(20)
acc.withdraw(50)
print(acc.balance)

