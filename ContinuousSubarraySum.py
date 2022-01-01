#Time - O(N)
class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        """
        d = {0:-1}
        d = {0:-1,5:0}
        d = {0:-1,5:0,1:1}
        d = {0:-1,5:0,1:1} -> True [5 present in d]
        """
        if len(nums) < 2:
            return False
        d = {0:-1}
        s = 0
        for i in range(len(nums)):
            s = s + nums[i]
            if k != 0:
                s = s % k
            if s in d:
                if i - d[s] > 1:
                    return True
            else:
                d[s] = i
        return False
