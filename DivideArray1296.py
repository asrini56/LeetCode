#1296. Divide Array in Sets of K Consecutive Numbers - Similar to question 846. Hand of Straights
from collections import Counter
class Solution:
    def isPossibleDivide(self, nums: List[int], k: int) -> bool:
        counter = Counter(nums)
        nums.sort()
        i = 0
        j = len(nums)
        while i < j:
            curr = nums[i]
            for K in range(k):
                c = curr + K
                if c not in counter:
                    return False
                elif counter[c] == 1:
                    del counter[c]
                else:
                    counter[c]-=1
            while i < j and nums[i] not in counter:
                i+=1
        return True
