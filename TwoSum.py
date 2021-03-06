#1. Two Sum, Time - O(n)
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dictionary = {}
        for n in range(len(nums)):
            num = nums[n]
            remain = target - num
            if remain in dictionary:
                return [dictionary[remain],n]
            dictionary[num] = n
        return -1
