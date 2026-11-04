class Solution:
    def getLIS(self, nums: list[int]) -> list[int]:
        if not nums:
            return []
            
        # Stores the INDICES of nums that form the increasing subsequence
        dp_indices = []
        # Tracks the previous index for each element to reconstruct the path
        parent = [-1] * len(nums)
        
        for i, num in enumerate(nums):
            # Binary search to find the insertion position in dp_indices
            left, right = 0, len(dp_indices) - 1
            while left <= right:
                mid = (left + right) // 2
                if nums[dp_indices[mid]] < num:
                    left = mid + 1
                else:
                    right = mid - 1
            
            # If found position is within bounds, update it; otherwise append
            if left < len(dp_indices):
                dp_indices[left] = i
            else:
                dp_indices.append(i)
            
            # Map the predecessor if this isn't the start of a sequence
            if left > 0:
                parent[i] = dp_indices[left - 1]
                
        # Reconstruct the actual LIS sequence backwards using the parent pointers
        curr = dp_indices[-1]
        lis_sequence = []
        while curr != -1:
            lis_sequence.append(nums[curr])
            curr = parent[curr]
            
        return lis_sequence[::-1] # Reverse to get correct order

# Example usage:
if __name__ == "__main__":
    solution = Solution()
    test_nums = [10, 9, 2, 5, 3, 7, 101, 18]
    result = solution.getLIS(test_nums)
    
    print(f"Input: {test_nums}")
    print(f"Longest Increasing Subsequence: {result}")
    print(f"Length: {len(result)}")
