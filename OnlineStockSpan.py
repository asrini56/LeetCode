"""
901. Online Stock Span
Given n as the number of calls to next,

Time complexity of each call to next: O(1)

Even though there is a while loop in next, that while loop can only run nn times total across the entire algorithm. Each element can only be popped off the stack once, and there are up to nn elements.

This is called amortized analysis - if you average out the time it takes for next to run across nn calls, it works out to be O(1). If one call to next takes a long time because the while loop runs many times, then the other calls to next won't take as long because their while loops can't run as long.

Space complexity: O(n)

In the worst case scenario for space (when all the stock prices are decreasing), the while loop will never run, which means the stack grows to a size of nn.
"""
class StockSpanner:

    def __init__(self):
        self.count = 0
        self.maximum = float("-inf")
        self.stack = []
        

    def next(self, price: int) -> int:
        answer = 1
        while self.stack and self.stack[-1][0] <= price:
            answer+=self.stack.pop()[1]
        self.stack.append([price,answer])
        return answer


# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
