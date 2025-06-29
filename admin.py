from user import Person, User
class Admin(Person):
    # Added 'password' parameter with a default value for easy setup
    def __init__(self, name, email, address, bank, password="123"):
        super().__init__(name, email, address)
        self.bank = bank
        self.password = password  # Store the password as an instance variable

    def create_account(self, name, email, address, account_type, password):
        new_account = User(name, email, address, account_type, self.bank, password=password)
        self.bank.users[new_account.account_number] = new_account
        print(f'Account created successfully! Account number is {new_account.account_number}')

    def delete_account(self, account_number):
        if account_number in self.bank.users:
            self.bank.users.pop(account_number)
            print('Account Deleted Successfully')
        else:
            print("Sorry Account Not found")
    def check_total_balance(self):
        print(f"Total Bank Amount is {self.bank.total_balance}")

    def check_total_loan(self):
        print(f"Total Loan Amount is {self.bank.total_loan}")


    def show_all_user(self):
        if not self.bank.users:
            print("No users found.")
            return
        print(' User Name     Account_Number   Balance ')
        print("-----------    -------------    -------")
        for account_number , user in self.bank.users.items():
            print(f'{user.name}\t{account_number}\t{user.balance}')
