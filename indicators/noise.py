prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]

def efficieny_ratio(prices, window):
    net_change = abs(prices[-1] - prices[-window - 1])
    sum_absolute_changes = sum(abs(prices[i] - prices[i - 1]) for i in range(1, len(prices)))
    efficieny_ratio = net_change / sum_absolute_changes
    return efficieny_ratio
    

print(efficieny_ratio(prices, 10))