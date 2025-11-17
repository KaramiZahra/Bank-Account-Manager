# Bank Account Manager

A console-based banking system written in Python, supporting account management, transactions, and secure password handling.

## Features

- **Account Types**:
  - `SavingAccount`: Earns annual interest.
  - `CheckingAccount`: Supports overdraft limits.
  
- **Operations**:
  - Create account with secure password.
  - Deposit and withdraw money.
  - Transfer between accounts.
  - View account details.
  - Delete accounts.
  - View transaction history.
  - Search for accounts by holder name.

- **Security**:
  - Passwords are hashed using `bcrypt`.
  - Password verification required for sensitive operations (deposit, withdraw, transfer).

- **Persistence**:
  - Accounts and transactions are saved in a JSON file (`accounts.json`) and loaded automatically.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/KaramiZahra/Bank-Account-Manager
cd Bank-Account-Manager
```

2. Make sure you have Python 3 installed.

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script:

```bash
python3 app.py
```

Follow the menu prompts to interact with the app:

---Bank Account Manager---

1. Create Account
2. Deposit
3. Withdraw
4. Transfer
5. Show Accounts
6. Delete Account
7. Transactions log
8. Search for an account
9. Save and Exit


## File Structure

```bash
Bank-Account-Manager/
│
├── manager/
    ├── __init__.py
    ├── accounts.py
    └── bank_manager.py
├── app.py
├── accounts.json
├── requirements.txt
├── .gitignore
└── README.md
```

## Notes

- Account numbers are stored as strings to allow flexibility.
- Input validation ensures amounts are numeric and positive.
- Plain-text passwords are never saved.
