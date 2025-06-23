import tkinter as tk
from tkinter import messagebox, simpledialog
from user import User

# Simulated bank structure
class Bank:
    def __init__(self, name):
        self.name = name
        self.total_balance = 0
        self.total_loan = 0
        self.bank_rupt = False
        self.users = {}

# Initialize bank and a test user
bank = Bank("Sample Bank")
user = User("Alice", "alice@example.com", "Wonderland", "Savings", bank, "pass123")
bank.users[user.account_number] = user

# GUI logic
class BankGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bank User Interface")

        self.logged_in_user = None

        self.label = tk.Label(master, text="Welcome to the Bank GUI")
        self.label.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        acc_no = simpledialog.askinteger("Login", "Enter Account Number:")
        password = simpledialog.askstring("Login", "Enter Password:", show='*')

        user = bank.users.get(acc_no)
        if user and user.password == password:
            self.logged_in_user = user
            messagebox.showinfo("Success", f"Welcome {user.name}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def show_dashboard(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text=f"Logged in as: {self.logged_in_user.name}").pack()
        tk.Button(self.master, text="Deposit", command=self.deposit).pack()
        tk.Button(self.master, text="Withdraw", command=self.withdraw).pack()
        tk.Button(self.master, text="Check Balance", command=self.check_balance).pack()
        tk.Button(self.master, text="Take Loan", command=self.take_loan).pack()
        tk.Button(self.master, text="Transfer Money", command=self.transfer_money).pack()
        tk.Button(self.master, text="Transaction History", command=self.transaction_history).pack()
        tk.Button(self.master, text="Logout", command=self.logout).pack()

    def deposit(self):
        amount = simpledialog.askinteger("Deposit", "Enter amount to deposit:")
        if amount:
            self.logged_in_user.diposit_amount(amount)

    def withdraw(self):
        amount = simpledialog.askinteger("Withdraw", "Enter amount to withdraw:")
        if amount:
            self.logged_in_user.withdraw_amount(amount)

    def check_balance(self):
        self.logged_in_user.check_balance()

    def take_loan(self):
        amount = simpledialog.askinteger("Loan", "Enter loan amount:")
        if amount:
            self.logged_in_user.take_loan(amount)

    def transfer_money(self):
        acc_no = simpledialog.askinteger("Transfer", "Enter recipient account number:")
        amount = simpledialog.askinteger("Transfer", "Enter amount to transfer:")
        if acc_no and amount:
            self.logged_in_user.transfer_money(amount, acc_no)

    def transaction_history(self):
        history = "\n".join(self.logged_in_user.transaction_history)
        messagebox.showinfo("Transaction History", history if history else "No transactions yet.")

    def logout(self):
        self.logged_in_user = None
        for widget in self.master.winfo_children():
            widget.destroy()
        self.__init__(self.master)

# Launch GUI
root = tk.Tk()
gui = BankGUI(root)
root.mainloop()
