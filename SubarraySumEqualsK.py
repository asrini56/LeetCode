#560. Subarray Sum Equals K, Time - O(n)
"""
similar to two sum
brute force -> sum all numbers
find a way to store sum and use them
"""

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        if nums == []:
            return 0
        d = {}
        d[0] = 1
        count = 0
        s = 0
        for i in range(len(nums)):
            s = s + nums[i]
            if s-k in d:
                count = count + d[s-k]
            if s in d:
                d[s] = d[s] + 1
            else:
                d[s] = 1
        return count
