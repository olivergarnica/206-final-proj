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

