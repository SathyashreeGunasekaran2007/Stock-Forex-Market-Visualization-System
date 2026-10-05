import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# -----------------------------
# Load External CSV Data
# -----------------------------
df = pd.read_csv("market_data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)

# -----------------------------
# EMA Calculation
# -----------------------------
df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()

# -----------------------------
# RSI Calculation (14)
# -----------------------------
delta = df["Close"].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
df["RSI"] = 100 - (100 / (1 + rs))

# -----------------------------
# Buy / Sell Signal Logic
# -----------------------------
df["Signal"] = ""

for i in range(1, len(df)):
    # BUY condition
    if (
        df["EMA20"][i] > df["EMA50"].iloc[i]
        and df["EMA20"][i - 1] <= df["EMA50"].iloc[i - 1]
        and df["RSI"][i] < 70
    ):
        df.at[df.index[i], "Signal"] = "BUY"

    # SELL condition
    elif (
        df["EMA20"][i] < df["EMA50"].iloc[i]
        and df["EMA20"][i - 1] >= df["EMA50"].iloc[i - 1]
        and df["RSI"][i] > 30
    ):
        df.at[df.index[i], "Signal"] = "SELL"

# -----------------------------
# Candlestick + EMA Chart
# -----------------------------
apds = [mpf.make_addplot(df["EMA20"]), mpf.make_addplot(df["EMA50"])]

mpf.plot(
    df,
    type="candle",
    addplot=apds,
    volume=True,
    title="Stock / Forex Candlestick with EMA20 & EMA50",
    style="yahoo",
)

# -----------------------------
# RSI Chart
# -----------------------------
plt.figure()
plt.plot(df.index, df["RSI"])
plt.axhline(70)
plt.axhline(30)
plt.title("RSI Indicator (14)")
plt.show()

# -----------------------------
# Print Trading Signals
# -----------------------------
signals = df[df["Signal"] != ""]
print("\nGenerated Trading Signals:\n")
print(signals[["Close", "EMA20", "EMA50", "RSI", "Signal"]])
