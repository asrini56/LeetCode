class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        """
        LeetCode 152: Maximum Product Subarray
        
        Core Concept:
        -------------
        Unlike a maximum sum subarray, finding a maximum product requires tracking 
        BOTH the running maximum (`curr_max`) and running minimum (`curr_min`) at 
        every step. 
        
        Why? Because a negative number multiplied by a very small (highly negative) 
        minimum product can instantly flip into a massive positive maximum product.
        
        Example Walkthrough (nums = [2, 3, -2, 4]):
        ------------------------------------------
        - i = 0 (num = 2):  
          curr_min = 2, curr_max = 2, m = 2
        - i = 1 (num = 3):  
          num1 = 3 * 2 = 6, num2 = 3 * 2 = 6
          curr_min = min(3, 6, 6) = 3
          curr_max = max(3, 6, 6) = 6
          m = max(2, 6) = 6
        - i = 2 (num = -2): 
          num1 = -2 * 3 = -6, num2 = -2 * 6 = -12
          curr_min = min(-2, -6, -12) = -12  (Captured the negative minimum streak)
          curr_max = max(-2, -6, -12) = -2
          m = max(6, -2) = 6
        - i = 3 (num = 4):  
          num1 = 4 * -12 = -48, num2 = 4 * -2 = -8
          curr_min = min(4, -48, -8) = -48
          curr_max = max(4, -48, -8) = 4
          m = max(6, 4) = 6
          
        Final Return: 6 (Subarray [2, 3])
        
        Time Complexity: O(n) - Single pass through the array.
        Space Complexity: O(1) - Constant auxiliary space.
        """
        if not nums:
            return 0
        
        # Initialize tracking variables to the first element safely
        m = nums[0]
        curr_min = nums[0]
        curr_max = nums[0]
        
        # Iterate through the rest of the array starting from index 1
        for i in range(1, len(nums)):
            # Calculate potential products by extending previous chains
            num1 = nums[i] * curr_min
            num2 = nums[i] * curr_max
            
            # Update current min and max based on three choices:
            # 1. nums[i]: Abandon previous streak and start a fresh subarray here
            # 2. num1: Extend the previous minimum streak (crucial when nums[i] is negative)
            # 3. num2: Extend the previous maximum streak
            curr_min = min(nums[i], num1, num2)
            curr_max = max(nums[i], num1, num2)
            
            # Update the global maximum product found across all subarrays
            m = max(m, curr_max)
            
        return m
