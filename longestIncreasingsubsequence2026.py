"""
        ========================================================================
        STEP-BY-STEP WALKTHROUGH (O(n log n) Patience Sorting Approach)
        ========================================================================
        Example: nums = [10, 9, 2, 5, 3, 7, 101, 18]

        1. KEY VARIABLES & SETUP:
           - dp: Maintains the smallest tail element for increasing subsequences 
             of various lengths. Always stays strictly sorted.
           - LIS: Tracks the length of the longest increasing subsequence found 
             so far (equal to len(dp) at the end).

        2. ITERATION & LOGIC:
           - If nums[i] > dp[-1]: It extends the longest subsequence, so we append 
             it to dp and increment LIS.
           - Else: We use binary search (bisect_left equivalent) to find the 
             first element in dp that is >= nums[i] and replace it. This greedy 
             optimization keeps tail values as small as possible to aid future extensions.

        3. TRACE HIGHLIGHTS:
           - nums[i] = 2: Replaces 10/9 -> dp = [2]
           - nums[i] = 5: Extends -> dp = [2, 5], LIS = 2
           - nums[i] = 3: Replaces 5 -> dp = [2, 3]
           - nums[i] = 7: Extends -> dp = [2, 3, 7], LIS = 3
           - nums[i] = 101: Extends -> dp = [2, 3, 7, 101], LIS = 4
           - nums[i] = 18: Replaces 101 -> dp = [2, 3, 7, 18]

        4. FINAL RESULT:
           - Returns LIS, which is 4.
        ========================================================================
        """
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
