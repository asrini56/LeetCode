class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        
        # If the total sum is odd, it's mathematically impossible to split into two equal halves
        if total % 2 != 0:
            return False
        
        target = total // 2
        
        # dp[j] represents whether a subset sum of j can be formed
        dp = [False] * (target + 1)
        dp[0] = True  # Base case: a sum of 0 is always achievable (empty subset)
        
        for num in nums:
            # Traverse backwards from target down to num
            # This ensures each number in 'nums' is only used once per partition
            for j in range(target, num - 1, -1):
                if dp[target]:  # Early exit if we've already reached the target sum
                    return True
                dp[j] = dp[j] or dp[j - num]
                
        return dp[target]

# --- Example Usage ---
sol = Solution()

# Example 1: Can be partitioned into [1, 5, 5] and [11] (both sum to 11)
nums1 = [1, 5, 11, 5]
print(f"Can partition {nums1}? {sol.canPartition(nums1)}")  # Output: True

# Example 2: Cannot be partitioned into equal halves (sum is 11, which is odd)
nums2 = [1, 2, 3, 5]
print(f"Can partition {nums2}? {sol.canPartition(nums2)}")  # Output: False
