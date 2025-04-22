# Group Name: Kappa
# Group Members: Kanishk, Kibrom, Oliver
import os
from insider import get_all_insider_trades, stock_tickers, FH_KEY
from databases import APIdatamanager
from econ import fetch_econdb_data
from marketstack import fetch_marketstack_data
from analysis import *
import time

def main():
    print("Starting data collection...")

    # Initialize db manager
    db_manager = APIdatamanager(db_path="all_data.db")

    try:
        # Process finnhub insider data
        print("\nFetching insider trading data...")
        for cap_level in stock_tickers:
            print(f"Processing {cap_level} cap stocks:")
            for symbol in stock_tickers[cap_level]:
                print(f" -- {symbol}", end=" ")
                
                try:
                    insider_data = get_all_insider_trades(symbol)
                    db_manager.insert_finnhub_data(insider_data, symbol)
                    print("Success")
                    time.sleep(8)
                except Exception as e:
                    print(f"Failure (Error: {str(e)})")
        
        # Process marketstack data
        print("\nFetching stock market data...")
        for cap_level in stock_tickers:
            print(f"Processing {cap_level} cap stocks:")
            for symbol in stock_tickers[cap_level]:
                print(f" -- {symbol}", end=" ")
                
                try:
                    market_data = fetch_marketstack_data(symbol)
                    db_manager.insert_marketstack_data(market_data)
                    print("Success")
                    time.sleep(10)
                except Exception as e:
                    print(f"Failure (Error: {str(e)})")
        
        # Process economic data
        print("\nFetching economic indicators...")
        try:
            econ_data = fetch_econdb_data()
            #print(econ_data)
            db_manager.insert_econdb_data(econ_data)
            print("Economic data saved successfully!")
            db_manager.conn.commit()
        except Exception as e:
            print(f"Failed to save economic data: {str(e)}")
        
        calculate_and_write_pnl(db_path="all_data.db", output_path="trade_pnls.txt")
        analyze_pnls_by_company(pnl_file_path="trade_pnls.txt", output_path="company_pnl_summary.txt")
        print("\nAll data processed successfully!")
        print("Database saved to: all_data.db")
        
    finally:
        db_manager.close()

if __name__ == "__main__":
    main() 
