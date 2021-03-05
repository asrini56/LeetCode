#50. Pow(x, n), Time - O(logN), Space - O(1)
class Solution:
    def myPow(self, x: float, n: int) -> float:
        p = n
        if n < 0:
            x = 1/x
            p = -p
        result = 1
        curr = x
        while p > 0:
            if p % 2 == 1:
                result = result * curr
            curr = curr * curr
            p = int(p / 2)
        return result
