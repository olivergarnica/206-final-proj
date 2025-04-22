import sqlite3

class APIdatamanager:
    def __init__(self, db_path="data.db"):
        # Connect to the on-disk SQLite database (creates file if it does not exist)
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self._create_tables()  # Set up the database immediately

    def _create_tables(self):
        # New table to store unique company symbols
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT UNIQUE
            );
        """)

        # Updated insiders table to reference companies by id
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS insiders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                company_id INTEGER,
                UNIQUE(name, company_id),
                FOREIGN KEY(company_id) REFERENCES companies(id)
            );
        """)


        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS insider_trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insider_id INTEGER,
                num_shares_after INTEGER,
                change_of_shares INTEGER,
                avg_transaction_price REAL,
                transaction_date TEXT,
                filing_date TEXT,
                transaction_code TEXT,
                FOREIGN KEY(insider_id) REFERENCES insiders(id),
                UNIQUE(insider_id, transaction_date, transaction_code)
            );
        """)

        # Create table for marketstack
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                exchange TEXT,
                UNIQUE(symbol, date)
            );
        """)

        # create table for econDB
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS macroeconomic_indicators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indicator TEXT,
                date TEXT,
                value REAL,
                UNIQUE(indicator, date)
            );
        """)

    def insert_finnhub_data(self, transactions, symbol):
        inserts_done = 0

        # check if the company exists in the table, insert otherwise
        self.cur.execute("""
            INSERT OR IGNORE INTO companies (symbol)
            VALUES (?)
        """, (symbol,))
        
        self.cur.execute("SELECT id FROM companies WHERE symbol = ?", (symbol,))
        company_result = self.cur.fetchone()
        
        if not company_result:
            return
        company_id = company_result[0]
        
        for entry in sorted(transactions, key=lambda x: x.get("transactionDate")):
            if inserts_done >= 25:
                break

            name = entry.get("name")
            # position = entry.get("position") or "Unknown"

            self.cur.execute("""
                INSERT OR IGNORE INTO insiders (name, company_id)
                VALUES (?, ?)
            """, (name, company_id))

            self.cur.execute("""
                SELECT id FROM insiders WHERE name = ? AND company_id = ?
            """, (name, company_id))
            result = self.cur.fetchone()
            if not result:
                continue

            insider_id = result[0]

            self.cur.execute("""
                INSERT OR IGNORE INTO insider_trades
                (insider_id, num_shares_after, change_of_shares, avg_transaction_price, transaction_date, filing_date, transaction_code)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                insider_id,
                entry.get("share"),
                entry.get("change"),
                entry.get("transactionPrice"),
                entry.get("transactionDate"),
                entry.get("filingDate"),
                entry.get("transactionCode")
            ))

            if self.cur.rowcount > 0:
                inserts_done += 1

    def insert_econdb_data(self, data, limit=25):
        for series_json in data.get("series", []):
            code = series_json.get("ticker")
            if not code:
                continue

            dates  = series_json.get("data", {}).get("dates",  [])
            values = series_json.get("data", {}).get("values", [])

            recent_pairs = list(zip(dates, values))[-limit:]

            for date, value in recent_pairs:
                self.cur.execute(
                    """
                    INSERT OR IGNORE INTO macroeconomic_indicators
                    (indicator, date, value)
                    VALUES (?, ?, ?)
                    """,
                    (code, date, value)
                )
    
    def insert_marketstack_data(self, data, limit = 25):
        entries = data.get("data", [])[:limit]

        for entry in entries:
            self.cur.execute("""
                INSERT OR IGNORE INTO market_data 
                (symbol, date, open, high, low, close, volume, exchange)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.get("symbol"),
                entry.get("date"),
                entry.get("open"),
                entry.get("high"),
                entry.get("low"),
                entry.get("close"),
                entry.get("volume"),
                entry.get("exchange")
            ))

    def close(self):
        self.conn.commit()
        self.conn.close()
