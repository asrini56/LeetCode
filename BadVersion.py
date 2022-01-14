# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> int:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        l = 0
        r = n
        while l < r:
            m = (l+r)//2
            if isBadVersion(m):
                r = m
            else:
                l = m + 1
        return l
