

class ATM:

    _create_table_sql = """
    create table if not exists transactions (
        ACCT VARCHAR(5),
        AMOUNT DECIMAL(36,2)
    );
    """

    _make_deposit_sql = """
    insert into transactions (
        ACCT,
        AMOUNT
    )
    values (12345, ?);
    """

    _check_balance_sql = """
    select 
        ifnull(sum(AMOUNT), 0) 
    from transactions;
    """

    def __init__(self, db_api_v2_connection):

        self.conn = db_api_v2_connection
        self._database_setup()

    #####################################
    ## Database initialization methods ##
    #####################################

    def _database_setup(self):
        self._create_database_if_not_exists()
        self._create_transactions_table()

    def _create_database_if_not_exists(self):
        pass

    def _create_transactions_table(self):
        cur = self.conn.cursor()
        cur.execute(self._create_table_sql)
        cur.close()

    ###################
    ## Public method ##
    ###################

    @property
    def balance(self):
        cur = self.conn.cursor()
        cur.execute(self._check_balance_sql)
        amount = cur.fetchone()[0]
        cur.close()
        return amount

    @balance_check
    def check_balance(self):
        pass

    @balance_check
    def make_deposit(self, amount):
        cur = self.conn.cursor()
        cur.execute(self._make_deposit_sql, (amount,))
        conn.commit()
        cur.close()

    @balance_check
    def make_withdraw(self, amount):
        if amount > self.balance:
            print('Insufficient funds')
        else:
            cur = self.conn.cursor()
            cur.execute(self._make_deposit_sql, (-1 * amount,))
            conn.commit()
            cur.close()
            
################
## DECORATORS ##
################

# report account balances after an action
def balance_check(fn):
    def add_balance_check(self, *args, **kwargs):
        results = fn(self, *args, **kwargs)
        print('Account balance: {:,}'.format(self.balance))
        return results
    return add_balance_check
