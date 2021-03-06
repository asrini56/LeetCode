#202. Happy Number
class Solution:
    def isHappy(self, n: int) -> bool:
        flag = 0
        found = False
        if n == 1:
            return True
        seen = set()
        while n > 3 and n not in seen:
            seen.add(n)
            s = str(n)
            k = 0
            for st in s:
                k += pow(int(st),2)
            if k == 1:
                found = True
                break
            n = k
        return found
