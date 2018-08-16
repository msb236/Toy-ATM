import cmd
from .accounts_management_system import AMSSQLite

################
## DECORATORS ##
################

# report account balances after an action
def report_balance(fn):
    def add_balance_check(self, *args, **kwargs):
        results = fn(self, *args, **kwargs)
        print('Account balance: {:,}'.format(self.account.balance))
        return results
    return add_balance_check

#####################
## ATM APPLICATION ##
#####################

class ATM(cmd.Cmd):

    intro = 'Welcome to UnencryptoBank. Type help or ? to list commands.\n'
    prompt = '$$$ '
    file = None

    def __init__(self):
        self.account = AMSSQLite()
        super(ATM, self).__init__()

    @report_balance
    def do_check_balance(self, arg):
        pass

    @report_balance
    def do_make_deposit(self, arg):
        amount = float(arg)
        self.account.make_deposit(float(amount))

    @report_balance
    def do_make_withdraw(self, arg):
        amount = float(arg)
        self.account.make_withdraw(float(amount))

    def do_log_out(self, arg):
        print('Thank you for (kind of) banking with us!')
        self.account.close()
        return True
