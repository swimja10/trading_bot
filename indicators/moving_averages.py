def average(prices):
    total_price = 0
    for price in prices:
        total_price += price
    average = total_price/len(prices)
    return average

def SMA(prices, window_size):
    if len(prices) < window_size:
        return 0
    sma = []
    for i in range(len(prices) - window_size + 1):
        window = prices[i:i+window_size]
        sma.append(average(window))
    return sma[-1]
