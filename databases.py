import sqlite3

class APIdatamanager:
    def __init__(self, db_path="data.db"):
        # Connect to the on-disk SQLite database (creates file if it does not exist)
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self._create_tables()  # Set up the database immediately

    def _create_tables(self):
        # Create the table for each insider
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS insiders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                symbol TEXT,
                position TEXT,
                UNIQUE(name, symbol)
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

    def insert_finnhub_data(self, api_response):
        symbol = api_response.get("symbol")
        transactions = api_response.get("data", [])

        for entry in transactions[:25]: 
            name = entry.get("name")
            position = entry.get("position") or "Unknown"

            # Insert or ignore the insider
            self.cur.execute("""
                INSERT OR IGNORE INTO insiders (name, symbol, position)
                VALUES (?, ?, ?)
            """, (name, symbol, position))

            # Get the insider's ID
            self.cur.execute("""
                SELECT id FROM insiders WHERE name = ? AND symbol = ?
            """, (name, symbol))
            result = self.cur.fetchone()
            if not result:
                continue

            insider_id = result[0]

            # Insert trade into insider_trades
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

    def insert_econdb_data(self, data):
        datasets = data.get("datasets", {})

        for indicator_code, content in datasets.items():
            entries = content.get("data", [])

            for row in entries[:25]:
                date, value = row
                self.cur.execute("""
                    INSERT OR IGNORE INTO macroeconomic_indicators
                    (indicator, date, value)
                    VALUES (?, ?, ?)
                """, (
                    indicator_code,
                    date,
                    value
                ))


    def insert_marketstack_data(self, data):
        entries = data.get("data", [])

        for entry in entries[:25]:
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
