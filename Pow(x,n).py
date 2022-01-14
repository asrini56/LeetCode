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
    """
    pow(3,2):
    while 2 > 0:
        result = 1
        curr = 3 * 3= 9
        p = 1
    while 1>0
        result = 1*9 = 9
        p = 0
    result = 9
    
    working - 
    pow(3,11)- 
    p = 11
    curr = 3
    result = 1
    while 11 > 0:
        11 % 2 == 1:
            result = 3
        curr = 9
        p = 5
    5 > 0:
        result = 27
        curr = 81
        p = 2
    2 > 0
        curr = 81 * 81
        p = 1
    1 > 0:
        result = 27 * 81 = 177147
        p = 0
    result = 177147
    """
