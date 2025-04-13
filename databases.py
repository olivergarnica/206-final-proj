import requests
import sqlite3
import finnhub
from insider import fetch_finnhub_transactions, stock_tickers, FH_KEY
import time
"""
A. Must access three APIs. This is worth 10 points. 
 
B. Access and store at least 100 rows in your database from each API/website 10 points. 
 
C. For at least one API you must have two tables that share an integer key 20 points. 
You must not have duplicate string data in your database! Do not just split data 
from one table into two! Also, there should be only one final database! 
 
D. You must limit how much data you store from an API into the database each time 
you execute the file that stores data to the database to 25 or fewer items (60 points). 
The data must be stored in a SQLite database. This means that you must run the file 
that stores the data multiple times to gather at least 100 items total without 
duplicating any data or changing the source code.
"""

"""Insider trading tends to be after quarterly earning reports. Maybe compare how they trade
vs earnings reports and what kind of trades they execute during these times."""

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
