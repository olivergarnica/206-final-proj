import sqlite3, pandas as pd
import matplotlib.pyplot as plt

# Average PnL per company (bar chart)
pnl_df = pd.read_csv("trade_pnls.txt", sep="\t")
pnl_df["PnL"] = pd.to_numeric(pnl_df["PnL"])
pnl_df = pnl_df.dropna(subset=["PnL"])                         
pnl_df["PnL"] = pnl_df["PnL"].astype(float)

avg_pnl = pnl_df.groupby("symbol")["PnL"].mean().sort_values()
fig1, ax1 = plt.subplots()
ax1.bar(avg_pnl.index, avg_pnl.values)
ax1.set_ylabel("Average 7 day PnL ($)")
ax1.set_title("Average Insider Trade PnL by Company (last 25 trades)")
ax1.set_xticklabels(avg_pnl.index, rotation=45, ha="right")
plt.tight_layout()
plt.show()

# Scatter plot of number of trades vs average PnL per company
summary_df = pnl_df.groupby("symbol").agg(
    num_trades=("PnL", "count"),
    avg_pnl=("PnL", "mean")
).reset_index()
fig3, ax3 = plt.subplots()
ax3.scatter(summary_df["num_trades"], summary_df["avg_pnl"], s=100, alpha=0.7)
for _, row in summary_df.iterrows():
    ax3.annotate(
        row["symbol"],
        (row["num_trades"], row["avg_pnl"]),
        textcoords="offset points", xytext=(5, 5)
    )
ax3.set_xlabel("Number of Trades")
ax3.set_ylabel("Average 7-day PnL ($)")
ax3.set_title("Average PnL vs Number of Trades by Company")
plt.tight_layout()
plt.show()

# Line chart of stock closing prices over time
db_path = "all_data.db"
conn = sqlite3.connect(db_path)
market_df = pd.read_sql_query(
    "SELECT symbol, date, close FROM market_data", conn
)
conn.close()
market_df["date"] = pd.to_datetime(market_df["date"].str[:10])
pivot_df = market_df.pivot(index="date", columns="symbol", values="close")

fig3, ax3 = plt.subplots()
pivot_df.plot(ax=ax3)
ax3.set_xlabel("Date")
ax3.set_ylabel("Closing Price ($)")
ax3.set_title("Stock Closing Prices Over Time")
plt.tight_layout()
plt.show()

# Chart of percentage change of a stock of choice vs consumer price index, rgdp, and 3 month yield 
conn = sqlite3.connect(db_path)

stock_choice = ['AAPL', 'MSFT', 'GOOGL', 'META', 'DOCU', 'TWLO', 'ZM', 'TEAM', 'PLTR', 'ADBE']
print("Choose a stock from:", stock_choice)
stock = input("Enter your stock choice: ").upper()

indicators = ["RGDPUS", "CPIUS", "M3YDUS"]

# Monthly percent change
def get_monthly_percent_change(df, value_col="value", date_col="date"):
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    cutoff = df[date_col].max() - pd.Timedelta(days=60)
    recent_df = df[df[date_col] >= cutoff]

    if len(recent_df) < 2:
        return None
    prev, latest = recent_df.iloc[-2][value_col], recent_df.iloc[-1][value_col]
    if prev == 0:
        return None
    return ((latest - prev) / prev) * 100

stock_df = pd.read_sql_query(
    f"SELECT date, close as value FROM market_data WHERE symbol = ? ORDER BY date",
    conn, params=(stock,)
)
stock_change = get_monthly_percent_change(stock_df)

macro_changes = {}
for code in indicators:
    macro_df = pd.read_sql_query(
        f"SELECT date, value FROM macroeconomic_indicators WHERE indicator = ? ORDER BY date",
        conn, params=(code,)
    )
    change = get_monthly_percent_change(macro_df)
    macro_changes[code] = change
conn.close()

labels = [stock] + indicators
changes = [stock_change] + list(macro_changes.values())
# Remove None values
labels, changes = zip(*[(l, c) for l, c in zip(labels, changes) if c is not None])

fig5, ax5 = plt.subplots()
bars = ax5.bar(labels, changes)
ax5.set_ylabel("1-Month % Change")
ax5.set_title(f"Monthly % Change: {stock} vs Macroeconomic Indicators")

for bar, val in zip(bars, changes):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f"{val:.2f}%", ha='center', va='bottom')

plt.tight_layout()
plt.show()