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

class ATMBase(cmd.Cmd):

    intro = 'Welcome to UnencryptoBank. Type help or ? to list commands.\n'
    prompt = '$$$ '
    file = None

    def __init__(self):
        self.account = AMSSQLite()
        super(ATMBase, self).__init__()

    @report_balance
    def do_check_balance(self, arg):
        pass

    @report_balance
    def do_make_withdraw(self, arg):
        """Withdraw funds, please enter amount to withdraw."""
        amount = float(arg)
        self.account.make_withdraw(float(amount))

    def do_log_out(self, arg):
        """End session"""
        print('Thank you for (kind of) banking with us!')
        self.account.close()
        return True


class CustomerATM(ATMBase):

    intro = (
        'Welcome back to UnencryptoBank, valued customer!\n'
        'Type help or ? to list commands.\n'
    )

    @report_balance
    def do_make_deposit(self, arg):
        """Deposit funds, please enter amount to deposit"""
        amount = float(arg)
        self.account.make_deposit(float(amount))


class GuestATM(ATMBase):

    _fee = 5

    @report_balance
    def do_make_withdraw(self, arg):
        """Withdraw funds, please enter amount to withdraw."""
        msg = (
            'There is a ${} fee for this operation.\n'
            'Would you like to proceed? (Yes or No)\n'
        ).format(self._fee)
        proceed = input(msg + self.prompt)
        if proceed.upper() in ('YES' or 'Y'):
            amount = float(arg) + self._fee
            self.account.make_withdraw(float(amount))

