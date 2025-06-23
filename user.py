from abc import ABC
class Person(ABC):
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address
        
class User(Person):
    __account_cnt = 1000
    def __init__(self, name, email, address, account_type, bank,password):
        super().__init__(name, email, address)
        self.account_type = account_type
        self.balance = 0
        self.get_loan = 0
        self.loan_balance = 0
        self.transaction_history = []
        self.account_number = User.generate_account_number()
        self.bank = bank
        self.password = password 
    @classmethod
    def generate_account_number(cls):
        cls.__account_cnt+=1
        return cls.__account_cnt
    
    def diposit_amount(self, amount):
        self.balance+=amount
        self.bank.total_balance += amount
        print(f"{amount} has been deposited. New Balance is {self.balance} Taka")
        self.transaction_history.append(f'Deposited: {amount}')

    def withdraw_amount(self, amount):
        if(self.bank.bank_rupt!=True):
            if amount>self.balance:
                print("Withdrawal amount exceeded")
                return
            self.balance-=amount
            self.bank.total_balance -= amount
            print(f'{amount} has been withdrawn. New Balance is {self.balance} Taka')
            self.transaction_history.append(f'Withdrawn: {amount}')
        else:
            print("Sorry! The bank is bankrupt")
            
    def check_balance(self):
        print(f'Your Balance is : {self.balance}')
    
    def check_transaction_history(self):
        for history in self.transaction_history:
            print(history)
    
    def take_loan(self, amount):
        if self.get_loan <2:
            self.balance+=amount
            self.loan_balance+=amount
            self.bank.total_loan+= amount
            self.get_loan+=1
            self.transaction_history.append(f'Loan Taken: {amount}')
            print(f'Loan approved! New balance is : {self.balance} Taka')
        else:
            print('Sorry Loan Limit Exceeded')
            
    def transfer_money(self, amount, other_account_no):
        if self.bank.bank_rupt != True:
            if other_account_no in self.bank.users:
                account = self.bank.users[other_account_no]
                account.balance += amount
                self.balance -= amount 
                print(f'Transfer {amount} to {account.account_number} Successfully. New balance is : {self.balance} Taka')
                account.transaction_history.append(f'Received Money {amount} from {self.account_number}')
                
                self.transaction_history.append(f'Transferd Amount : {amount} Taka')
                
            else:
                print('Sorry Account Not Found')
        
        else:
            print(f"Sorry! The {self.bank.name} bank is bankrupt")
                   