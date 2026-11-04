class Solution:
    def findLongestContinuousSequence(self, nums: list[int]) -> list[int]:
        if not nums:
            return []
            
        max_start = 0
        max_len = 1
        curr_start = 0
        curr_len = 1
        
        for i in range(1, len(nums)):
            if nums[i] > nums[i - 1]:
                curr_len += 1
            else:
                # Reset the current sequence tracker
                curr_start = i
                curr_len = 1
            
            # Update the global maximum if the current one is longer
            if curr_len > max_len:
                max_len = curr_len
                max_start = curr_start
                
        return nums[max_start : max_start + max_len]

# Example usage:
if __name__ == "__main__":
    solution = Solution()
    test_nums = [10, 9, 2, 5, 3, 7, 101, 18]
    result = solution.findLongestContinuousSequence(test_nums)
    
    print(f"Input: {test_nums}")
    print(f"Longest Continuous Increasing Sequence: {result}")
    # Output: [3, 7, 101] (Length: 3)
