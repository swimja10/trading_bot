def average(prices):
    if not prices:
        raise ValueError("Price list cannot be empty")
    return sum(prices)/len(prices)

def SMA(prices, window_size):
    if len(prices) < window_size:
        return None

    sma = []
    for i in range(len(prices) - window_size + 1):
        sma.append(sum(prices[i:i+window_size]) / window_size)

    return sma

prices = [1.1050, 1.1060, 1.1040, 1.1070, 1.1080]

print(SMA(prices=prices, window_size=3))

average_indicators = {
    "Average": average(prices),
    "SMA5": SMA(prices, 5),
    "SMA8": SMA(prices, 8),
    "SMA200": SMA(prices, 200)
}