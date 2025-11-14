from datetime import datetime, timedelta
import bcrypt


class Account:
    def __init__(self, account_number, holder_name, balance, account_type, creation_date, account_password):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance
        self.account_type = account_type
        self.creation_date = creation_date or datetime.now().date().isoformat()
        self.account_password = self._hash_password(account_password)

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
            'creation_date': self.creation_date,
            'account_password': self.account_password
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
                data['account_password']
            )

    def _hash_password(self, password):
        if not password:
            return None

        if isinstance(password, str) and password.startswith("$2") and len(password) > 50:
            return password

        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.account_password.encode())


class SavingAccount(Account):
    def __init__(self, account_number, holder_name, balance, account_type, creation_date, account_password, interest_rate, last_interest_date):
        super().__init__(account_number, holder_name, balance,
                         account_type, creation_date, account_password)
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
            data['account_password'],
            data['interest_rate'],
            data['last_interest_date']
        )

    def apply_interest(self):
        if datetime.now().date() - datetime.fromisoformat(self.last_interest_date).date() >= timedelta(days=365):
            interest = self.balance * self.interest_rate / 100
            self.balance += interest
            self.last_interest_date = datetime.now().date().isoformat()
            return interest
        return 0


class CheckingAccount(Account):
    def __init__(self, account_number, holder_name, balance, account_type, creation_date, account_password, overdraft_limit):
        super().__init__(account_number, holder_name, balance,
                         account_type, creation_date, account_password)
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
            data['account_password'],
            data['overdraft_limit']
        )

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance + self.overdraft_limit:
            raise ValueError("Overdraft limit exceeded.")
        self.balance -= amount
        return self.balance
