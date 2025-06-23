// Global variables to store current user and type (user/admin)
let currentUserAccount = null;
let currentAccountType = null; // 'user' or 'admin'

// --- UI Management Functions ---
function hideAllForms() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('admin-login-form').style.display = 'none';
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('deposit-form').style.display = 'none';
    document.getElementById('withdraw-form').style.display = 'none';
    document.getElementById('take-loan-form').style.display = 'none';
    document.getElementById('transfer-form').style.display = 'none';
    document.getElementById('create-account-form').style.display = 'none';
    document.getElementById('delete-account-form').style.display = 'none';

    // Clear messages and results
    document.querySelectorAll('.message').forEach(el => el.textContent = '');
    document.querySelectorAll('.result-area').forEach(el => el.innerHTML = '');
}

function showAuthSection() {
    hideAllForms();
    document.getElementById('auth-section').style.display = 'block';
}

function showLogin() {
    hideAllForms();
    document.getElementById('login-form').style.display = 'block';
}

function showRegister() {
    hideAllForms();
    document.getElementById('register-form').style.display = 'block';
}

function showAdminLogin() {
    hideAllForms();
    document.getElementById('admin-login-form').style.display = 'block';
}

function showDashboard(type) {
    hideAllForms();
    document.getElementById('dashboard').style.display = 'block';
    if (type === 'user') {
        document.getElementById('dashboard-title').textContent = `User Dashboard (Acc: ${currentUserAccount})`;
        document.getElementById('user-dashboard-buttons').style.display = 'block';
        document.getElementById('admin-dashboard-buttons').style.display = 'none';
    } else if (type === 'admin') {
        document.getElementById('dashboard-title').textContent = `Admin Dashboard`;
        document.getElementById('user-dashboard-buttons').style.display = 'none';
        document.getElementById('admin-dashboard-buttons').style.display = 'block';
    }
}

function hideForms() {
    showAuthSection();
}

function showDepositForm() {
    hideAllForms();
    document.getElementById('deposit-form').style.display = 'block';
}

function showWithdrawForm() {
    hideAllForms();
    document.getElementById('withdraw-form').style.display = 'block';
}

function showTakeLoanForm() {
    hideAllForms();
    document.getElementById('take-loan-form').style.display = 'block';
}

function showTransferForm() {
    hideAllForms();
    document.getElementById('transfer-form').style.display = 'block';
}

function showCreateAccountForm() {
    hideAllForms();
    document.getElementById('create-account-form').style.display = 'block';
}

function showDeleteAccountForm() {
    hideAllForms();
    document.getElementById('delete-account-form').style.display = 'block';
}


// --- API Call Functions (Fetch API) ---

async function userLogin() {
    const accNo = document.getElementById('loginAccNo').value;
    const password = document.getElementById('loginPassword').value;
    const messageDiv = document.getElementById('loginMessage');

    try {
        const response = await fetch('/api/user/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ account_number: accNo, password: password })
        });
        const data = await response.json();

        if (data.success) {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message success';
            currentUserAccount = data.account_number;
            currentAccountType = 'user';
            setTimeout(() => showDashboard('user'), 1000); // Show dashboard after a small delay
        } else {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message error';
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again.';
        messageDiv.className = 'message error';
    }
}

async function userRegister() {
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const address = document.getElementById('registerAddress').value;
    const account_type = document.getElementById('registerAccType').value;
    const password = document.getElementById('registerPassword').value;
    const messageDiv = document.getElementById('registerMessage');

    try {
        const response = await fetch('/api/user/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, address, account_type, password })
        });
        const data = await response.json();

        if (data.success) {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message success';
            // Optionally, log in the user directly or redirect to login
            document.getElementById('loginAccNo').value = data.account_number; // Pre-fill login
            setTimeout(() => showLogin(), 2000);
        } else {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message error';
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred during registration. Please try again.';
        messageDiv.className = 'message error';
    }
}

// Admin login is simplified for now
function adminLoginPlaceholder() {
    currentAccountType = 'admin';
    showDashboard('admin');
}

function logout() {
    currentUserAccount = null;
    currentAccountType = null;
    showAuthSection();
}

// --- Placeholder/Empty functions for other actions (will be implemented in next steps) ---

async function depositMoney() {
    const amount = document.getElementById('depositAmount').value;
    const messageDiv = document.getElementById('depositMessage');
    if (!currentUserAccount) {
        messageDiv.textContent = "Please login first.";
        messageDiv.className = "message error";
        return;
    }
    if (!amount || amount <= 0) {
        messageDiv.textContent = "Please enter a valid amount.";
        messageDiv.className = "message error";
        return;
    }

    try {
        const response = await fetch('/api/user/deposit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ account_number: currentUserAccount, amount: parseInt(amount) })
        });
        const data = await response.json();

        if (data.success) {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message success';
            document.getElementById('depositAmount').value = ''; // Clear input
            setTimeout(() => showDashboard('user'), 1500);
        } else {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message error';
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again.';
        messageDiv.className = 'message error';
    }
}

async function withdrawMoney() {
    const amount = document.getElementById('withdrawAmount').value;
    const messageDiv = document.getElementById('withdrawMessage');
    if (!currentUserAccount) {
        messageDiv.textContent = "Please login first.";
        messageDiv.className = "message error";
        return;
    }
    if (!amount || amount <= 0) {
        messageDiv.textContent = "Please enter a valid amount.";
        messageDiv.className = "message error";
        return;
    }

    try {
        const response = await fetch('/api/user/withdraw', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ account_number: currentUserAccount, amount: parseInt(amount) })
        });
        const data = await response.json();

        if (data.success) {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message success';
            document.getElementById('withdrawAmount').value = '';
            setTimeout(() => showDashboard('user'), 1500);
        } else {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message error';
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again.';
        messageDiv.className = 'message error';
    }
}

async function checkBalance() {
    const messageDiv = document.getElementById('dashboard-message');
    const resultArea = document.getElementById('transaction-result');
    if (!currentUserAccount) {
        messageDiv.textContent = "Please login first.";
        messageDiv.className = "message error";
        return;
    }

    try {
        const response = await fetch(`/api/user/balance/${currentUserAccount}`);
        const data = await response.json();

        if (data.success) {
            resultArea.textContent = `Your current balance is: ${data.balance} Taka`;
            resultArea.className = 'result-area success';
        } else {
            resultArea.textContent = data.message;
            resultArea.className = 'result-area error';
        }
    } catch (error) {
        console.error('Error:', error);
        resultArea.textContent = 'An error occurred. Please try again.';
        resultArea.className = 'result-area error';
    }
}

async function takeLoan() {
    const amount = document.getElementById('loanAmount').value;
    const messageDiv = document.getElementById('loanMessage');
    if (!currentUserAccount) {
        messageDiv.textContent = "Please login first.";
        messageDiv.className = "message error";
        return;
    }
    if (!amount || amount <= 0) {
        messageDiv.textContent = "Please enter a valid amount.";
        messageDiv.className = "message error";
        return;
    }

    try {
        const response = await fetch('/api/user/loan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ account_number: currentUserAccount, amount: parseInt(amount) })
        });
        const data = await response.json();

        if (data.success) {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message success';
            document.getElementById('loanAmount').value = '';
            setTimeout(() => showDashboard('user'), 1500);
        } else {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message error';
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again.';
        messageDiv.className = 'message error';
    }
}

async function transferMoney() {
    const recipientAccNo = document.getElementById('transferAccNo').value;
    const amount = document.getElementById('transferAmount').value;
    const messageDiv = document.getElementById('transferMessage');
    if (!currentUserAccount) {
        messageDiv.textContent = "Please login first.";
        messageDiv.className = "message error";
        return;
    }
    if (!recipientAccNo || !amount || amount <= 0) {
        messageDiv.textContent = "Please enter valid recipient and amount.";
        messageDiv.className = "message error";
        return;
    }

    try {
        const response = await fetch('/api/user/transfer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sender_account_number: currentUserAccount,
                receiver_account_number: parseInt(recipientAccNo),
                amount: parseInt(amount)
            })
        });
        const data = await response.json();

        if (data.success) {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message success';
            document.getElementById('transferAccNo').value = '';
            document.getElementById('transferAmount').value = '';
            setTimeout(() => showDashboard('user'), 1500);
        } else {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message error';
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again.';
        messageDiv.className = 'message error';
    }
}

async function transactionHistory() {
    const messageDiv = document.getElementById('dashboard-message');
    const resultArea = document.getElementById('transaction-result');
    if (!currentUserAccount) {
        messageDiv.textContent = "Please login first.";
        messageDiv.className = "message error";
        return;
    }

    try {
        const response = await fetch(`/api/user/history/${currentUserAccount}`);
        const data = await response.json();

        if (data.success) {
            if (data.history && data.history.length > 0) {
                resultArea.innerHTML = '<h3>Transaction History:</h3>' + data.history.join('<br>');
            } else {
                resultArea.textContent = 'No transactions yet.';
            }
            resultArea.className = 'result-area success';
        } else {
            resultArea.textContent = data.message;
            resultArea.className = 'result-area error';
        }
    } catch (error) {
        console.error('Error:', error);
        resultArea.textContent = 'An error occurred. Please try again.';
        resultArea.className = 'result-area error';
    }
}


// --- Admin Actions ---

async function createAccount() {
    const name = document.getElementById('createName').value;
    const email = document.getElementById('createEmail').value;
    const address = document.getElementById('createAddress').value;
    const account_type = document.getElementById('createAccType').value;
    const password = document.getElementById('createPassword').value;
    const messageDiv = document.getElementById('createAccountMessage');

    try {
        const response = await fetch('/api/admin/create_account', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, address, account_type, password })
        });
        const data = await response.json();

        if (data.success) {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message success';
            // Clear inputs
            document.getElementById('createName').value = '';
            document.getElementById('createEmail').value = '';
            document.getElementById('createAddress').value = '';
            document.getElementById('createAccType').value = '';
            document.getElementById('createPassword').value = '';
            setTimeout(() => showDashboard('admin'), 2000);
        } else {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message error';
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again.';
        messageDiv.className = 'message error';
    }
}

async function deleteAccount() {
    const accNo = document.getElementById('deleteAccNo').value;
    const messageDiv = document.getElementById('deleteAccountMessage');

    if (!accNo) {
        messageDiv.textContent = "Please enter an account number.";
        messageDiv.className = "message error";
        return;
    }

    try {
        const response = await fetch('/api/admin/delete_account', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ account_number: parseInt(accNo) })
        });
        const data = await response.json();

        if (data.success) {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message success';
            document.getElementById('deleteAccNo').value = '';
            setTimeout(() => showDashboard('admin'), 1500);
        } else {
            messageDiv.textContent = data.message;
            messageDiv.className = 'message error';
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again.';
        messageDiv.className = 'message error';
    }
}

async function checkTotalBalance() {
    const messageDiv = document.getElementById('dashboard-message');
    const resultArea = document.getElementById('transaction-result'); // Re-use for generic results

    try {
        const response = await fetch('/api/admin/total_balance');
        const data = await response.json();

        if (data.success) {
            resultArea.textContent = `Total Bank Balance: ${data.total_balance} Taka`;
            resultArea.className = 'result-area success';
        } else {
            resultArea.textContent = data.message;
            resultArea.className = 'result-area error';
        }
    } catch (error) {
        console.error('Error:', error);
        resultArea.textContent = 'An error occurred. Please try again.';
        resultArea.className = 'result-area error';
    }
}

async function checkTotalLoan() {
    const messageDiv = document.getElementById('dashboard-message');
    const resultArea = document.getElementById('transaction-result');

    try {
        const response = await fetch('/api/admin/total_loan');
        const data = await response.json();

        if (data.success) {
            resultArea.textContent = `Total Loan Amount: ${data.total_loan} Taka`;
            resultArea.className = 'result-area success';
        } else {
            resultArea.textContent = data.message;
            resultArea.className = 'result-area error';
        }
    } catch (error) {
        console.error('Error:', error);
        resultArea.textContent = 'An error occurred. Please try again.';
        resultArea.className = 'result-area error';
    }
}

async function showAllUsers() {
    const messageDiv = document.getElementById('dashboard-message');
    const resultArea = document.getElementById('all-users-list'); // Specific div for user list

    try {
        const response = await fetch('/api/admin/all_users');
        const data = await response.json();

        if (data.success) {
            if (data.users && data.users.length > 0) {
                let userHtml = '<h3>All Bank Users:</h3>';
                userHtml += '<table style="width:100%; border-collapse: collapse;">';
                userHtml += '<thead><tr><th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Name</th><th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Acc No</th><th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Balance</th></tr></thead><tbody>';
                data.users.forEach(user => {
                    userHtml += `<tr><td style="border: 1px solid #ddd; padding: 8px; text-align: left;">${user.name}</td><td style="border: 1px solid #ddd; padding: 8px; text-align: left;">${user.account_number}</td><td style="border: 1px solid #ddd; padding: 8px; text-align: left;">${user.balance}</td></tr>`;
                });
                userHtml += '</tbody></table>';
                resultArea.innerHTML = userHtml;
            } else {
                resultArea.textContent = 'No users found.';
            }
            resultArea.className = 'result-area success';
        } else {
            resultArea.textContent = data.message;
            resultArea.className = 'result-area error';
        }
    } catch (error) {
        console.error('Error:', error);
        resultArea.textContent = 'An error occurred. Please try again.';
        resultArea.className = 'result-area error';
    }
}

async function toggleLoanFeature() {
    const messageDiv = document.getElementById('dashboard-message');
    try {
        const response = await fetch('/api/admin/toggle_loan_feature', { method: 'POST' });
        const data = await response.json();
        messageDiv.textContent = data.message;
        messageDiv.className = data.success ? 'message success' : 'message error';
        setTimeout(() => messageDiv.textContent = '', 2000); // Clear message
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again.';
        messageDiv.className = 'message error';
    }
}

async function toggleBankruptStatus() {
    const messageDiv = document.getElementById('dashboard-message');
    try {
        const response = await fetch('/api/admin/toggle_bankrupt_status', { method: 'POST' });
        const data = await response.json();
        messageDiv.textContent = data.message;
        messageDiv.className = data.success ? 'message success' : 'message error';
        setTimeout(() => messageDiv.textContent = '', 2000); // Clear message
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again.';
        messageDiv.className = 'message error';
    }
}


// Initial state: show authentication section
document.addEventListener('DOMContentLoaded', showAuthSection);