#1636. Sort Array by Increasing Frequency
from collections import Counter
class Solution:
    def frequencySort(self, nums: List[int]) -> List[int]:
        numCount = Counter(nums)
        nums.sort(key = lambda x:(numCount[x],-x))
        return nums
