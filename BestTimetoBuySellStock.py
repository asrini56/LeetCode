#121. Best Time to Buy and Sell Stock, Time - O(n)
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        answer = 0
        minimum = float('inf')
        for price in prices:
            if price < minimum:
                minimum = price
            else:
                answer = max(answer,price - minimum)
        return answer
