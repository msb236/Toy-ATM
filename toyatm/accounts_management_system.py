import os
import sqlite3
import errno


#########################
## APPLICATION CLASSES ##
#########################

class AMS:

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
        self._create_transactions_table()

    #############################################
    ## Private database initialization methods ##
    #############################################

    def _create_transactions_table(self):
        cur = self.conn.cursor()
        cur.execute(self._create_table_sql)
        cur.close()

    ####################
    ## Public methods ##
    ####################

    @property
    def balance(self):
        cur = self.conn.cursor()
        cur.execute(self._check_balance_sql)
        amount = cur.fetchone()[0]
        cur.close()
        return amount

    def make_deposit(self, amount):
        cur = self.conn.cursor()
        cur.execute(self._make_deposit_sql, (amount,))
        self.conn.commit()
        cur.close()

    def make_withdraw(self, amount):
        if amount > self.balance:
            print('Insufficient funds')
        else:
            cur = self.conn.cursor()
            cur.execute(self._make_deposit_sql, (-1 * amount,))
            self.conn.commit()
            cur.close()
            
    def close(self):
        self.conn.close()

class AMSSQLite(AMS):

    _application_relative_dir = 'Toy_ATM'
    _database_name = 'account_management_system.db'

    def __init__(self):

        conn = self._database_setup()
        super(AMSSQLite, self).__init__(db_api_v2_connection=conn)

    ####################################
    ## Private database setup methods ##
    ####################################

    def _database_setup(self): 

        self._get_application_dir_abs_path()
        self._make_application_dir()
        conn = self._get_database_connection()

        return conn

    def _get_application_dir_abs_path(self):

        application_dir = os.path.join(
            os.path.expanduser('~'), 
            self._application_relative_dir
        )

        self._application_dir = application_dir

    def _make_application_dir(self):

        try:
            os.mkdir(self._application_dir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    def _get_database_connection(self):

        database_abs_path = os.path.join(
            self._application_dir, 
            self._database_name
        )
        conn = sqlite3.connect(database=database_abs_path)

        return conn
