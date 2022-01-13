#Time/Space - O(t.n),The memo array of size O(t \cdot n)O(t⋅n) has been filled just once. Here, tt refers to the sum of the numsnums array and nn refers to the length of the numsnums array.
class Solution:
    def findTargetSumWays(self, nums: List[int], S: int) -> int:
        self.count = 0
        self.total = sum(nums)
        memo = [[float("-inf")]*(2*self.total+1) for i in range(len(nums))]
        def calculate(nums,i,s,S,memo):
            if i == len(nums):
                if s == S:
                    return 1
                else:
                    return 0
            else:
                if memo[i][s+self.total] != float("-inf"):
                    return memo[i][s+self.total]
                add = calculate(nums,i+1,s+nums[i],S,memo)
                sub = calculate(nums,i+1,s-nums[i],S,memo)
                memo[i][s+self.total] = add+sub
                return memo[i][s+self.total]
        return calculate(nums,0,0,S,memo)
