class Solution:
    def findCheapestPrice(self, n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
        """
        Time Complexity: O(k * E) 
          - Where k is the maximum number of allowed stops and E is the number of flights (edges).
          - The outer loop runs k + 1 times, and the inner loop checks every flight once.
          
        Space Complexity: O(n + E)
          - O(n) to store the prices and temporary prices arrays.
          - O(E) to store the flights list.
        """
        prices = [float("inf")] * n
        prices[src] = 0

        # Run k + 1 times to account for up to k stops (k + 1 flights)
        for i in range(k + 1):
            temp_prices = prices.copy()

            for source, dest, price in flights:
                if prices[source] == float("inf"):
                    continue
                
                if prices[source] + price < temp_prices[dest]:
                    temp_prices[dest] = prices[source] + price
                
            prices = temp_prices
        
        return prices[dst] if prices[dst] != float("inf") else -1


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    solution = Solution()
    
    n = 4
    flights = [[0, 1, 100], [1, 2, 100], [2, 3, 100], [0, 2, 500]]
    src = 0
    dst = 3
    k = 1  # At most 1 stop (meaning max 2 flights)
    
    result = solution.findCheapestPrice(n, flights, src, dst, k)
    print(f"Cheapest price from {src} to {dst} with at most {k} stop(s): {result}")
    # Output: 600 (Path: 0 -> 2 -> 3)
