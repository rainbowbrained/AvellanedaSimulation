import pandas as pd
import re
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import random

operation_dict = {
    'BUY': False,
    'SELL': True   
}

def parse_log_file(file_path, token = '', start_time = None, interval = 0):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 9:
                datetime = parts[4] + ' ' + parts[5]
                datetime = pd.to_datetime(datetime, format='%Y-%m-%d %H:%M:%S.%f')

                operation = operation_dict[parts[6]]  # BUY or SELL
                price = float(parts[7])
                volume = float(parts[8])  
                data.append({'datetime': datetime, 'op_sell': operation, 'price': price, 'volume': volume})
    df = pd.DataFrame(data)
    df['profit_loss'] = df.apply(lambda row: row['price'] * row['volume'] if row['op_sell'] else -row['price'] * row['volume'], axis=1)
    df['returns'] = df['price'].pct_change()
    return df

def plot_profit_loss(df, l):
    plt.figure(figsize=(12, 6))
    plt.plot(df['datetime'], df['profit_loss'].cumsum(), label=l)
    plt.title('Cumulative profit/loss')
    plt.xlabel('Time')
    plt.ylabel('Cumulative profit/loss')
    plt.axhline(0, color='red', linestyle='--', linewidth=1)
    plt.legend()
    plt.grid()
    plt.show()

token = '1000PEPEUSDT'
df = parse_log_file(token+'.log') 

plot_profit_loss(df, token)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Parameters
gamma = 0.1  # Risk aversion
k = 1.5
A = 140

# Initialize variables
inventory = 0
wealth = 0
equity = []
reservation_prices = []
bids = []
asks = []
spreads = []

# Process transactions
for index, row in df[:40000].iterrows():
    time = row['datetime']
    side = row['op_sell']
    price = row['price']
    volume = row['volume']

    # Calculate reservation price
    reservation_price = price - inventory * gamma * (2)  # Simplified example; adjust based on time and volatility

    # Calculate spread
    spread = gamma * (2) + (2/gamma) * np.log(1 + (gamma/k))
    spread /= 2

    # Calculate bid and ask
    bid = reservation_price - spread
    ask = reservation_price + spread

    # Update inventory and wealth based on transaction
    if not side:
        inventory += volume
        wealth -= bid * volume
    else:
        inventory -= volume
        wealth += ask * volume

    # Update equity
    equity.append(wealth + inventory * price)

    # Store metrics
    reservation_prices.append(reservation_price)
    bids.append(bid)
    asks.append(ask)
    spreads.append(spread)

# Calculate average spread and profit
average_spread = np.mean(spreads)
final_profit = equity[-1]

# Print results
print("                   Results              ")
print("----------------------------------------")
print("%14s %21s" % ('statistic', 'value'))
print(40 * "-")
print("%14s %20.5f" % ("Average spread :", average_spread))
print("%16s %20.5f" % ("Profit :", final_profit))


plt.figure(figsize = (16, 8))
plt.plot(np.array(equity))
plt.grid(True)
plt.xlabel('pnl')
#plt.xlim([0, 8200])
plt.ylabel('number of values')
plt.show()

# Plotting
plt.figure(figsize=(16, 10), dpi=100)
plt.plot(np.array(reservation_prices)+700, linewidth = 0.5, label="Reservation Price")
plt.plot(bids, linewidth = 0.5, label="Bid")
plt.plot(np.array(asks)+1400, linewidth = 0.5, label="Ask")
#plt.ylim([-100, 100])
#plt.xlim([0, 8200])
plt.legend()
plt.grid(True)
plt.title("Reservation Price, Bid, and Ask Over Time")
plt.show()