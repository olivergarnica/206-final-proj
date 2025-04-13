import sqlite3

class APIdatamanager:
    def __init__(self, db_path="data.db"):
        # Connect to the on-disk SQLite database (creates file if it does not exist)
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self._create_tables()  # Set up the database immediately

    def _create_tables(self):
        # Create the 'insiders' table with all necessary columns.
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS insiders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                symbol TEXT,
                num_shares_after INTEGER,
                change_of_shares INTEGER,
                avg_transaction_price REAL,
                transaction_date TEXT,
                filing_date TEXT,
                transaction_code TEXT,
                UNIQUE(name, symbol, transaction_date)
            );
        """)

    def insert_finnhub_data(self, api_response):
        # The response contains 'symbol' at the top level and a list of transactions in 'data'
        symbol = api_response.get("symbol")
        transactions = api_response.get("data", [])
        
        for entry in transactions[:25]:  # Insert only the first 25 transactions per run
            self.cur.execute("""
                INSERT OR IGNORE INTO insiders
                (name, symbol, num_shares_after, change_of_shares, avg_transaction_price, transaction_date, filing_date, transaction_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.get("name"),
                symbol,
                entry.get("share"),
                entry.get("change"),
                entry.get("transactionPrice"),
                entry.get("transactionDate"),
                entry.get("filingDate"),
                entry.get("transactionCode")
            ))

    def insert_econdb_data(self, data):
        # Insert into 2 related tables with a shared integer key (to be implemented)
        pass

    def insert_marketstack_data(self, data):
        # Insert into market_prices or your chosen table (to be implemented)
        pass

    def close(self):
        self.conn.commit()
        self.conn.close()
