def maximumCoins(self, coins, k):
    total = result = i = 0
    coins.sort()
    for j in range(len(coins)):
        l, r, value = coins[j]
        total += value * (r - l + 1)
        while coins[j][1] - coins[i][0] > k - 1:
            excess = coins[j][1] - coins[i][0] + 1 - k
            result = max(result, total - excess * value)
            l1, r1, value1 = coins[i]
            if r1 - l1 + 1 > excess:
                total -= value1 * excess
                coins[i][0] += excess
            else:
                total -= value1 * (r1 - l1 + 1)
                i += 1
        result = max(result, total)
    return result
