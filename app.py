from flask import Flask, request, jsonify, render_template
import os
import json

# Import your classes
from bank import Bank
from user import User
from admin import Admin

app = Flask(__name__)

# --- Global Bank Instance and Data Persistence ---
# For simplicity, we'll use a JSON file to save/load bank state.
# In a real application, you would use a database (e.g., SQLite, PostgreSQL).

BANK_DATA_FILE = 'bank_data.json'
bank = None # Initialize bank as None, it will be loaded or created

def load_bank_data():
    global bank
    if os.path.exists(BANK_DATA_FILE):
        with open(BANK_DATA_FILE, 'r') as f:
            data = json.load(f)
            # Reconstruct Bank object
            bank_name = data.get('bank_name', 'Default Bank')
            bank = Bank(bank_name)
            bank.total_balance = data.get('total_balance', 0)
            bank.total_loan = data.get('total_loan', 0)
            bank.loan_feature_active = data.get('loan_feature_active', True)
            bank.bank_rupt = data.get('bank_rupt', False)

            # Reconstruct User objects
            for acc_num_str, user_data in data.get('users', {}).items():
                acc_num = int(acc_num_str) # Account numbers are ints, but JSON keys are strings
                user = User(
                    user_data['name'],
                    user_data['email'],
                    user_data['address'],
                    user_data['account_type'],
                    bank,
                    user_data['password']
                )
                user.balance = user_data['balance']
                user.get_loan = user_data['get_loan']
                user.loan_balance = user_data['loan_balance']
                user.transaction_history = user_data['transaction_history']
                user.account_number = acc_num # Ensure correct account number after generation
                bank.users[acc_num] = user
            print("Bank data loaded successfully.")
    else:
        # Create a new bank instance if no data file exists
        bank = Bank("My Awesome Web Bank")
        print("New bank instance created.")
    
    # Also create a default admin if none exists (for testing)
    if not any(isinstance(user_obj, Admin) for user_obj in bank.admins):
        default_admin = Admin("Admin User", "admin@example.com", "Admin City", bank)
        bank.admins.append(default_admin)
        print("Default admin created.")


def save_bank_data():
    # Convert bank state to a serializable dictionary
    data = {
        'bank_name': bank.bank_name,
        'total_balance': bank.total_balance,
        'total_loan': bank.total_loan,
        'loan_feature_active': bank.loan_feature_active,
        'bank_rupt': bank.bank_rupt,
        'users': {}
    }
    for acc_num, user_obj in bank.users.items():
        data['users'][str(acc_num)] = { # Convert acc_num to string for JSON key
            'name': user_obj.name,
            'email': user_obj.email,
            'address': user_obj.address,
            'account_type': user_obj.account_type,
            'balance': user_obj.balance,
            'get_loan': user_obj.get_loan,
            'loan_balance': user_obj.loan_balance,
            'transaction_history': user_obj.transaction_history,
            'password': user_obj.password,
            'account_number': user_obj.account_number # Store it explicitly
        }
    
    with open(BANK_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print("Bank data saved successfully.")

# Load data when the app starts
with app.app_context():
    load_bank_data()

# --- Flask Routes ---

@app.route('/')
def index():
    return render_template('index.html') # We'll create this HTML file

# Example User Login API endpoint
@app.route('/api/user/login', methods=['POST'])
def user_login():
    data = request.json
    account_number = data.get('account_number')
    password = data.get('password')

    user = bank.users.get(int(account_number))
    if user and user.password == int(password): # Assuming password is int as per your code
        # For a real app, you'd use sessions or JWTs for stateful login.
        # For simplicity, we'll just return success.
        return jsonify({"success": True, "message": f"Welcome {user.name}!", "account_number": user.account_number})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

# Example User Registration API endpoint
@app.route('/api/user/register', methods=['POST'])
def user_register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    address = data.get('address')
    account_type = data.get('account_type')
    password = data.get('password')

    if not all([name, email, address, account_type, password]):
        return jsonify({"success": False, "message": "All fields are required"}), 400

    new_user = User(name, email, address, account_type, bank, int(password))
    bank.users[new_user.account_number] = new_user
    save_bank_data() # Save data after registration
    return jsonify({
        "success": True,
        "message": f"Account created successfully! Account number is {new_user.account_number}",
        "account_number": new_user.account_number
    })

# ... inside app.py, after the login/register routes ...

@app.route('/api/user/deposit', methods=['POST'])
def user_deposit():
    data = request.json
    account_number = data.get('account_number')
    amount = data.get('amount')

    user = bank.users.get(int(account_number))
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    if not isinstance(amount, int) or amount <= 0:
        return jsonify({"success": False, "message": "Invalid deposit amount"}), 400

    user.diposit_amount(amount)
    save_bank_data() # Save state after modification
    return jsonify({"success": True, "message": f"Deposited {amount}. New balance: {user.balance}"})


@app.route('/api/user/withdraw', methods=['POST'])
def user_withdraw():
    data = request.json
    account_number = data.get('account_number')
    amount = data.get('amount')

    user = bank.users.get(int(account_number))
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    if not isinstance(amount, int) or amount <= 0:
        return jsonify({"success": False, "message": "Invalid withdrawal amount"}), 400
    
    # Check for bank bankruptcy before calling user's method
    if bank.bank_rupt:
        return jsonify({"success": False, "message": f"Sorry! The {bank.bank_name} bank is bankrupt. No withdrawals allowed."}), 400

    # Simulate the check within withdraw_amount, but also handle here
    if amount > user.balance:
        return jsonify({"success": False, "message": "Withdrawal amount exceeded"}), 400

    user.withdraw_amount(amount) # This method also prints, but we need JSON response
    save_bank_data()
    return jsonify({"success": True, "message": f"Withdrew {amount}. New balance: {user.balance}"})


@app.route('/api/user/balance/<int:account_number>', methods=['GET'])
def get_user_balance(account_number):
    user = bank.users.get(account_number)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    return jsonify({"success": True, "balance": user.balance})

@app.route('/api/user/loan', methods=['POST'])
def user_take_loan():
    data = request.json
    account_number = data.get('account_number')
    amount = data.get('amount')

    user = bank.users.get(int(account_number))
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    if not isinstance(amount, int) or amount <= 0:
        return jsonify({"success": False, "message": "Invalid loan amount"}), 400
    
    if not bank.loan_feature_active:
        return jsonify({"success": False, "message": f"Sorry! The {bank.bank_name} bank's loan feature is currently disabled."}), 400

    if user.get_loan >= 2:
        return jsonify({"success": False, "message": "Sorry, loan limit exceeded (max 2 loans)."}), 400
    
    user.take_loan(amount)
    save_bank_data()
    return jsonify({"success": True, "message": f"Loan approved! New balance: {user.balance}"})

@app.route('/api/user/transfer', methods=['POST'])
def user_transfer_money():
    data = request.json
    sender_account_number = data.get('sender_account_number')
    receiver_account_number = data.get('receiver_account_number')
    amount = data.get('amount')

    sender = bank.users.get(int(sender_account_number))
    receiver = bank.users.get(int(receiver_account_number))

    if not sender:
        return jsonify({"success": False, "message": "Sender account not found."}), 404
    if not receiver:
        return jsonify({"success": False, "message": "Receiver account not found."}), 404

    if not isinstance(amount, int) or amount <= 0:
        return jsonify({"success": False, "message": "Invalid transfer amount."}), 400

    if sender.balance < amount:
        return jsonify({"success": False, "message": "Insufficient balance for transfer."}), 400
    
    if bank.bank_rupt:
        return jsonify({"success": False, "message": f"Sorry! The {bank.bank_name} bank is bankrupt. No transfers allowed."}), 400

    # Call the transfer_money method from your User class
    sender.transfer_money(amount, receiver_account_number)
    save_bank_data()
    return jsonify({"success": True, "message": f"Transferred {amount} to {receiver_account_number} successfully. New balance: {sender.balance}"})


@app.route('/api/user/history/<int:account_number>', methods=['GET'])
def get_transaction_history(account_number):
    user = bank.users.get(account_number)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    return jsonify({"success": True, "history": user.transaction_history})

# --- Admin API Endpoints ---
@app.route('/api/admin/create_account', methods=['POST'])
def admin_create_account():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    address = data.get('address')
    account_type = data.get('account_type')
    password = data.get('password')

    # In a real scenario, you'd verify admin credentials here
    # For simplicity, we're assuming the request comes from an "authenticated" admin for now.
    
    # You need an Admin object to call create_account.
    # Let's use the first admin in the list (or create a temporary one for this call if no persistent admin).
    # Assuming bank.admins has at least one Admin object
    admin_obj = bank.admins[0] if bank.admins else Admin("Temp Admin", "temp@example.com", "Temp City", bank)
    
    # Check if a user with this email already exists
    for existing_user in bank.users.values():
        if existing_user.email == email:
            return jsonify({"success": False, "message": "User with this email already exists."}), 400

    try:
        new_user = User(name, email, address, account_type, bank, int(password))
        bank.users[new_user.account_number] = new_user # Your Admin class also adds this, but ensure consistency
        save_bank_data()
        return jsonify({
            "success": True,
            "message": f"Account created successfully! Account number is {new_user.account_number}",
            "account_number": new_user.account_number
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Error creating account: {str(e)}"}), 500


@app.route('/api/admin/delete_account', methods=['POST'])
def admin_delete_account():
    data = request.json
    account_number = data.get('account_number')

    if not isinstance(account_number, int):
        return jsonify({"success": False, "message": "Invalid account number."}), 400

    # Admin object for calling delete_account
    admin_obj = bank.admins[0] if bank.admins else Admin("Temp Admin", "temp@example.com", "Temp City", bank)
    
    if account_number in bank.users:
        admin_obj.delete_account(account_number) # This modifies bank.users directly
        save_bank_data()
        return jsonify({"success": True, "message": f"Account {account_number} deleted successfully."})
    else:
        return jsonify({"success": False, "message": "Account not found."}), 404

@app.route('/api/admin/total_balance', methods=['GET'])
def admin_total_balance():
    # In a real app, you'd check admin login.
    return jsonify({"success": True, "total_balance": bank.total_balance})

@app.route('/api/admin/total_loan', methods=['GET'])
def admin_total_loan():
    # In a real app, you'd check admin login.
    return jsonify({"success": True, "total_loan": bank.total_loan})

@app.route('/api/admin/all_users', methods=['GET'])
def admin_show_all_users():
    # In a real app, you'd check admin login.
    users_list = []
    for acc_num, user_obj in bank.users.items():
        users_list.append({
            "name": user_obj.name,
            "account_number": user_obj.account_number,
            "balance": user_obj.balance,
            "email": user_obj.email # Include more details as needed
        })
    return jsonify({"success": True, "users": users_list})

@app.route('/api/admin/toggle_loan_feature', methods=['POST'])
def admin_toggle_loan_feature():
    # In a real app, you'd check admin login.
    bank.loan_feature_active = not bank.loan_feature_active
    save_bank_data()
    status = "activated" if bank.loan_feature_active else "deactivated"
    return jsonify({"success": True, "message": f"Loan feature {status} successfully."})

@app.route('/api/admin/toggle_bankrupt_status', methods=['POST'])
def admin_toggle_bankrupt_status():
    # In a real app, you'd check admin login.
    bank.bank_rupt = not bank.bank_rupt
    save_bank_data()
    status = "activated" if bank.bank_rupt else "deactivated"
    return jsonify({"success": True, "message": f"Bankrupt status {status}. All transactions are {'off' if bank.bank_rupt else 'on'} now."})
# --- Add more API endpoints for user and admin actions here ---
# (We will add these in the next steps based on your admin.py and user.py)

if __name__ == '__main__':
    # Ensure the 'static' and 'templates' folders exist for Flask to find assets
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True) # debug=True allows hot-reloading and helpful error messages