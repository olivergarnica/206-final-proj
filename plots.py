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