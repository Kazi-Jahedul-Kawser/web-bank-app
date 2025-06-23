from user import User
from admin import Admin
from bank import Bank
bank = Bank('Bkash')
def Admin_interface():
    name = input("Enter Your Name: ")
    email = input('Enter Your Email: ')
    address = input('Enter Your Address: ')
    admin = Admin(name=name, email=email, address=address, bank= bank)
    
    print("\nWelcome to Admin Interface")
    print(f'Hello Mr/Mrs {admin.name}')
    while True:
        print("------------------------------")
        print('1. Create Account')
        print('2. Check Total Balance')
        print('3. Check Total Loan Amount')
        print('4. Delete Account')
        print('5. Show All User')
        print('6. Stop Loan Feature')
        print('7. Enable Loan Feature')
        print('8. Enable Bankrupt')
        print('9. Disable Bankrupt')
        print('10. Exit\n')
        print("---------------------------------") 
        try:
            option = int(input('Choise Any Option: '))
            if option == 1:
                name = input("Enter Name: ")
                email = input('Enter Email: ')
                address = input('Enter Address: ')
                account_type = input('Enter Account Type (Savings/Cuurent): ')
                password = int(input('Create 6 digit Password: '))
                admin.create_account(name=name, email=email, address=address, account_type=account_type, password=password)
            elif option == 2:
                admin.check_total_balance()
            elif option == 3:
                admin.check_total_loan()
            elif option == 4:
                account_number = int(input('Enter Account Number: '))
                admin.delete_account(account_number)
            elif option == 5:
                admin.show_all_user()
            elif option == 6:
                bank.loan_feature_active = False
                print("Loan Feature Disable successfully")
            elif option == 7:
                bank.loan_feature_active = True
                print("Loan Feature Active successfully")
            elif option == 8:
                bank.bank_rupt = True
                print("Bankrupt Status Activated .All Trunsaction are off now.")
            elif option == 9:
                bank.bank_rupt = False
                print("Bankrupt Status Deactivated .All Trunsaction are on now.")
            elif option == 10:
                break
        except:
            print('Invalid Input . Please Enter valid Input')
            continue

def User_interface():
    print("\nWelcome to User Interface")
    print('\b1. User Login')
    print('2.User Registration')
    
    option = int(input("Choise an Option: "))
    user = None
    if option == 1:
        account_number = int(input("Input your Account Number: "))
        
        if account_number  in bank.users: 
            user = bank.users[account_number]
            password = int(input('Enter Your Password: '))
            if(user.password != password):
                print('Sorry Password is correct!')
                return
                
        elif account_number not in bank.users:
            print('\bAccount is Not found !')
            return        
    elif option == 2:
        name = input("Enter Your Name: ")
        email = input('Enter Your Email: ')
        address = input('Enter Your Address: ')
        account_type = input('Enter Your Account Type (Savings/Curent): ')
        password = int(input('Create 6 digit Password: '))
        user = User(name=name, email=email, address=address, account_type=account_type, bank=bank,password=password)
        bank.users[user.account_number] = user
    print('--------------------------------------------------------')
    print(f'Welcome to {bank.bank_name} Mr/Mrs.{user.name} Account No: {user.account_number}')
    while(True):
        print(f"Acc No:{user.account_number}")
        print('1. Deposit Money')
        print('2. Withdraw Money')
        print('3. Balance Enquiry')
        print('4. Transfer Money')
        print('5. Money Loan')
        print('6. Transaction History')
        print('7. Exit\n')
    
        print('--------------------------------------------------------')
        
        try:
            option = int(input("Choise an Option: "))
            if(option == 1):
                amount = int(input("Enter Diposit Money: "))
                user.diposit_amount(amount)
            elif(option == 2):
                if not bank.bank_rupt :
                    amount = int(input("Enter withdrawal Amount: "))
                    user.withdraw_amount(amount)
                else:
                    print(f"Sorry! The {bank.bank_name} bank is bankrupt")
            elif(option == 3):
                user.check_balance()
            elif(option == 4):
                if not bank.bank_rupt :
                    amount  = int(input('Enter Money: '))
                    reciever_account_no = int(input("Enter Receiver Account Number: "))
                    user.transfer_money(amount,reciever_account_no)
                else:
                    print(f"Sorry! The {bank.name} bank is bankrupt")
       
            elif(option == 5):
                if  bank.loan_feature_active == True:
                    amount = int(input("Enter amount: "))
                    user.take_loan(amount)
                else:
                    print(f"Sorry! The {bank.bank_name} bank is bankrupt")
            elif(option == 6):
                user.check_transaction_history()
            elif(option == 7):
                break
        except:
            print("Invalid Input. Enter valid Input")
