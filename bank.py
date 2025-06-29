class Bank:
    def __init__(self, bank_name ):
        self.bank_name = bank_name
        self.users = {}
        self.admins = []
        self.total_balance = 0
        self.total_loan = 0
        self.loan_feature_active = True
        self.bank_rupt = False
