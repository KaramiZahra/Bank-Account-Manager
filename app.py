from manager.bank_manager import BankManager


def menu():
    bm = BankManager()

    while True:
        print("\n---Bank Account Manager---\n")
        print("1.Create Account")
        print("2.Deposit")
        print("3.Withdraw")
        print("4.Transfer")
        print("5.Show Accounts")
        print("6.Delete Account")
        print("7.Transactions log")
        print("8.Search for an account")
        print("9.Save and Exit")

        user_input = input("Choose an option(1-9): ")

        match user_input:
            case '1': bm.create_account()
            case '2': bm.deposit_amount()
            case '3': bm.withdraw_amount()
            case '4': bm.transfer()
            case '5': bm.show_accounts()
            case '6': bm.delete_account()
            case '7': bm.transactions_log()
            case '8': bm.search_account()
            case '9':
                bm.save_accounts()
                break
            case _: print("Invalid input.")


if __name__ == "__main__":
    menu()
