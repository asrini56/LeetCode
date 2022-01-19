class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        """
        
        We are trying to find two numbers which modulo to same number
        the difference of their sum will always modulo to 0
        d = {0:-1}
        d = {0:-1,5:0}
        d = {0:-1,5:0,1:1}
        d = {0:-1,5:0,1:1} -> True [5 present in d]
        
        say the the difference is d between a and b, such as d = b - a(b is on the right of a). you want d is multiple of k, so you just need d % k = 0. Because d = b - a, so d % k = 0 = (b - a) %k. so (b-a)%k=0 equal b%k - a%k = 0, then b%k = a%k. Comparing other hashtable based problem, you need check b-k whether in the hashtable. In this problem , you always check b%k, and always pust a%k into hashtable. when k = 0, you need do it as other similar problem.
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
        
            
