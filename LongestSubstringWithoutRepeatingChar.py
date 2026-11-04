class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Calculates the length of the longest substring without repeating characters.
        
        Pattern: Sliding Window with Hash Map Index Tracking
        
        Time Complexity: O(n) - Single pass where 'right' scans each character once.
        Space Complexity: O(min(n, m)) - 'm' is the size of the character set (e.g., 128 for ASCII).
        """
        max_len = 0
        char_map = {}  # Maps character -> its most recent index
        left = 0
        
        for right in range(len(s)):
            char = s[right]
            
            # If we've seen this character and it's inside our active window
            if char in char_map and char_map[char] >= left:
                # Jump the left boundary past the previous occurrence
                left = char_map[char] + 1
            
            # Update/insert the character's latest index
            char_map[char] = right
            
            # Track the maximum window size seen so far
            max_len = max(max_len, right - left + 1)
            
        return max_len
