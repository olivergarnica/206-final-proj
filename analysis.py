import sqlite3
from datetime import datetime, timedelta
import csv

def calculate_and_write_pnl(db_path="all_data.db", output_path="trade_pnls.txt"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("Calculating 1 week PnL for insider trades (Sales and Purchases only)...")

    # Fetch trades with symbol, insider name, txn_code, date, price, shares
    cur.execute("""
        SELECT t.id, i.symbol, i.name, t.transaction_date, t.avg_transaction_price, t.change_of_shares, t.transaction_code
        FROM insider_trades t
        JOIN insiders i ON t.insider_id = i.id
        WHERE t.transaction_code IN ('S', 'P')
    """)
    trades = cur.fetchall()

    results = []

    for trade_id, symbol, insider_name, txn_date, txn_price, shares, txn_code in trades:
        # Convert the transaction date string to a datetime object
        # Parse and add 1 day to transaction date
        try:
            transaction_date_obj = datetime.strptime(txn_date, "%Y-%m-%d")
            one_week_later = transaction_date_obj + timedelta(days=7)
            one_week_str = one_week_later.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"Invalid date format in trade {trade_id}: {txn_date}")
            one_week_str = None

        # Get closing price on next day
        # Uses LIKE since the date column includes time (Ex. 2025-04-02T00:00)
        if one_week_str:
            cur.execute("""
                SELECT close FROM market_data
                WHERE symbol = ? AND date LIKE ?
                ORDER BY date ASC LIMIT 1
            """, (symbol, f"{one_week_str}%"))
            row = cur.fetchone()

            if row:
                future_price = row[0]
                pnl = round((future_price - txn_price) * shares, 2)
            else:
                future_price = None
                pnl = None
        else:
            future_price = None
            pnl = None

        results.append((trade_id, insider_name, symbol, txn_code, txn_date, txn_price, shares, future_price, pnl))

    # Write results to file
    with open(output_path, "w") as f:
        f.write("trade_id\tinsider_name\tsymbol\ttxn_code\ttransaction_date\ttxn_price\tshares\tprice+7day\tPnL\n")
        for row in results:
            f.write("\t".join(str(x) if x is not None else "N/A" for x in row) + "\n")

    print(f"PnL written for {len(results)} trades to {output_path}")
    conn.close()

def analyze_pnls_by_company(pnl_file_path="trade_pnls.txt", output_path="company_pnl_summary.txt"):
    company_pnls = {}

    # Open the PnL file as a tab‑delimited CSV
    with open(pnl_file_path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            symbol = row["symbol"]
            pnl_str = row["PnL"]

            try:
                pnl = float(pnl_str)
            except ValueError:
                continue  # skip header or bad lines

            company_pnls.setdefault(symbol, []).append(pnl)

    # Write summary to output file
    with open(output_path, "w", newline="") as out:
        writer = csv.writer(out, delimiter="\t")
        writer.writerow(["symbol", "num_trades", "avg_pnl"])
        for symbol in sorted(company_pnls):
            pnls = company_pnls[symbol]
            avg_pnl = round(sum(pnls) / len(pnls), 2)
            writer.writerow([symbol, len(pnls), avg_pnl])

    print(f"Company-wise PnL summary written to {output_path}")