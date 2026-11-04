class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        if not nums:
            return 0
            
        dp = [nums[0]]
        LIS = 1
        
        for i in range(1, len(nums)):
            if dp[-1] < nums[i]:
                dp.append(nums[i])
                LIS += 1
            else:
                # Custom binary search (equivalent to bisect_left)
                left, right = 0, len(dp) - 1
                while left <= right:
                    mid = (left + right) // 2
                    if dp[mid] < nums[i]:
                        left = mid + 1
                    else:
                        right = mid - 1
                dp[left] = nums[i]
                
        return LIS

# Example usage:
if __name__ == "__main__":
    solution = Solution()
    
    test_nums = [10, 9, 2, 5, 3, 7, 101, 18]
    result = solution.lengthOfLIS(test_nums)
    
    print(f"Input: {test_nums}")
    print(f"Length of Longest Increasing Subsequence: {result}")
    # Output: 4 (The LIS is [2, 3, 7, 101] or [2, 3, 7, 18])
