import csv
import numpy as np
import datetime as dt

Ticker_csv = "AAPL.csv"
Short_Win = 50
Long_Win = 200
Start_Cap = 1000000
import yfinance as yf

# Download data
data = yf.download("AAPL", start="2010-01-01", end="2024-12-31")

# Save to CSV
data.to_csv("AAPL.csv")
if data.empty:
    print("Download failed. Try again or check internet.")
else:
    data.to_csv("AAPL.csv")
    print("Download successful. File saved as AAPL.csv")
import pandas_datareader.data as web
import datetime as dt

start = dt.datetime(2010, 1, 1)
end   = dt.datetime(2024, 12, 31)

df = web.DataReader('AAPL', 'stooq', start, end)   # source = Stooq
df = df.sort_index()                               # Stooq returns newest‑first
df.to_csv('AAPL.csv')
print("AAPL.csv saved with", len(df), "rows")

# Uncomment and run once to download the file

def read_prices(path):
    dates = []
    closes = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        date_idx = 0
        close_idx = header.index('Close')
        for row in reader:
            if len(row) < close_idx + 1:
                continue
            date_str = row[date_idx]
            close_str = row[close_idx]
            if date_str and close_str:
                dates.append(dt.datetime.strptime(date_str, '%Y-%m-%d'))
                closes.append(float(close_str))
    return dates, closes

def moving_average(series, window):
    sma = [None] * len(series)
    rolling_sum = 0.0
    for i,price in enumerate(series):
        rolling_sum += price
        if i >= window:
            rolling_sum -= series[i - window]
            sma[i] = rolling_sum / window
        elif i == window - 1:
            sma[i] = rolling_sum / window
    return sma

def generate_signals(short_ma, long_ma):
    signals = []
    last_signal = 0  # 0: no signal, 1: buy, -1: sell
    for i,(s,l) in enumerate(zip(short_ma, long_ma)):
        if s is None or l is None:
            signals.append(0)
            continue
        if s > l:
            if last_signal != 1:
                signals.append(1)
                last_signal = 1
            else:
                signals.append(0)
        else:
            if last_signal != 0:
                signals.append(-1)
                last_signal = 0
            else:
                signals.append(0)
    return signals
#######################################
#short_sma = [2, 3, 4]
#long_sma  = [5, 2, 3]

#zip(short_sma, long_sma)
#→ [(2, 5), (3, 2), (4, 3)]
#enumerate adds an index (i) to the loop, so you know which element you're at. It gives you:

#python
#Copy code
#(0, (s0, l0))
#(1, (s1, l1))
#(2, (s2, l2))
######################################
# "SMA = Simple Moving Average

# It’s a technical indicator used in trading. It calculates the average price of a stock over a specific number of past days.
# | Term          | Meaning                                       |
# | ------------- | --------------------------------------------- |
# | **Short SMA** | Avg price over short window (e.g., 50 days)   |
# | **Long SMA**  | Avg price over longer window (e.g., 200 days) |
# | **Why both?** | Compare them to detect trend changes          |
# When short SMA > long SMA: it means price is rising recently → Buy Signal

# When short SMA < long SMA: price is weakening → Sell Signal
# In a basic trading strategy, we don’t want to keep placing the same trade again and again if we're already in a position.

# So we use last_signal to remember our current trading state — whether we're:

# ✅ Already in a position (like holding the stock), or

# ❌ Currently out of the market

# Without last_signal
# Let’s say the short SMA is greater than the long SMA for 10 days in a row.
# Your strategy will generate a buy signal (1) every day — but that’s wrong.
# You already bought on day 1. You shouldn’t be buying again every day.

# This would cause:

# Overtrading

# Unrealistic backtest results

# Wrong P&L

def backtest(closes,signals,Start_Cap):
    cash = Start_Cap
    position = 0.0
    equity_curve = []
    
    for price,sig in zip(closes, signals):
        if sig == 1 and position == 0:
            position = cash / price
            cash = 0.0
        elif sig == -1 and position > 0:
            cash += position * price
            position = 0.0
        equity = cash + position * price
        equity_curve.append(equity)
    return equity_curve

# ------------------------------------------------------------------------------
# Function: backtest(closes, signals, initial_capital)
#
# Purpose:
#   Simulates how your trading strategy would have performed on historical data.
#   It applies buy/sell signals day by day and tracks the total portfolio value
#   (called the "equity curve") over time.
#
# Parameters:
#   - closes           : List of daily closing prices for the stock.
#   - signals          : List of trading signals for each day:
#                          1  = Buy (enter position)
#                         -1  = Sell (exit position)
#                          0  = Do nothing (hold current position)
#   - initial_capital  : Starting amount of cash in the portfolio (e.g., $1,000,000).
#
# Logic:
#   - Start with 100% in cash, 0 shares held.
#   - On a "buy" signal (1), use all cash to buy as many shares as possible.
#   - On a "sell" signal (-1), sell all held shares and convert to cash.
#   - On a "hold" signal (0), do nothing—just carry forward existing position.
#   - At the end of each day, calculate and record:
#       equity = cash + (position * today's closing price)
#
# Returns:
#   - equity_curve: List of total portfolio value (equity) for each day in the backtest.
#
# Notes:
#   - This is a simple long-only backtest with no transaction costs or slippage.
#   - The strategy assumes you execute trades at the same day's closing price.
# ------------------------------------------------------------------------------


def main():
    dates, closes = read_prices(Ticker_csv)
    short_ma = moving_average(closes, Short_Win)
    long_ma = moving_average(closes, Long_Win)
    signals = generate_signals(short_ma, long_ma)
    equity_curve = backtest(closes, signals, Start_Cap)

    for date, equity in zip(dates, equity_curve):
        print(f"{date.strftime('%Y-%m-%d')}: ${equity:.2f}")

    total_ret = (equity_curve[-1] / equity_curve[0] - 1) * 100
    print(f"Total Return: {total_ret:.2f}%")
    print(f"Final Equity: ${equity_curve[-1]:.2f}")
    print(f"Total return: {total_ret:.2f}%")
if __name__ == "__main__":
    main()