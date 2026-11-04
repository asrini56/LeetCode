from typing import List

class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        ans = []
        nums.sort()  # Step 1: Sort to group duplicates together
        visited = [False] * len(nums)  # Track which indices are currently in our path

        def backtrack(path: List[int]):
            # Base Case: If path matches length of nums, we have a complete permutation
            if len(path) == len(nums):
                ans.append(path.copy())
                return
            
            for i in range(len(nums)):
                # Skip if this element is already used in the current path
                if visited[i]:
                    continue
                
                # Skip duplicates: if current element is same as previous, 
                o# and the previous one was NOT used, skip to avoid duplicate branches.
                if i > 0 and nums[i] == nums[i-1] and not visited[i-1]:
                    continue
                
                # Choose
                visited[i] = True
                path.append(nums[i])
                
                # Explore
                backtrack(path)
                
                # Unchoose (Backtrack)
                path.pop()
                visited[i] = False

        backtrack([])
        return ans
