#from user_interface import User_interface
from admin_user_interface import Admin_interface, User_interface
while(True):
    print('\n1. Admin Login')
    print('2. User Interface')
    print('3. Exit')
    try:
        option = int(input("Choise an Option: "))
        if option == 1:
            Admin_interface()
        elif option == 2:
            User_interface()
        elif option == 3:
            break
    except:
        print('Invalid Input . Please Enter valid Input')
        continue
