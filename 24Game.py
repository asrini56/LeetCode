#679. 24 Game
class Solution:
    def judgePoint24(self, nums: List[int]) -> bool:
        if not nums:
            return False
        return self.dfs(nums, 4)
        
    
    def dfs(self, nums, n):
        if n == 1:
            if abs(nums[0] - 24) <= 1E-6 :
                return True
        
        for i in range(0, n):
            for j in range(i + 1, n):
                a, b = nums[i], nums[j]
                nums[j] = nums[n - 1]
                
                for temp in [a + b, a - b, b - a, a * b]:
                    nums[i] = temp
                    if self.dfs(nums, n - 1):
                        return True
                
                if a != 0:
                    nums[i] = b / a
                    if self.dfs(nums, n - 1):
                        return True
                if b != 0:
                    nums[i] = a / b
                    if self.dfs(nums, n - 1):
                        return True
                
                nums[i], nums[j] = a, b 
        return False
