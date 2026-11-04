class Solution:
    def checkValidString(self, s: str) -> bool:
        """
        Solves LeetCode 678: Valid Parenthesis String using a Greedy Interval approach.
        
        The wildcard '*' can act as '(', ')', or an empty string ''. 
        Because of this flexibility, a single string can result in a range of possible 
        open parenthesis counts rather than a single fixed number.
        
        We maintain a valid range using two counters:
        - minopen: The minimum possible number of unmatched '(' that must be closed.
          (Assumes '*' acts as ')' or '' when possible).
        - maxopen: The maximum possible number of unmatched '(' currently open.
          (Assumes '*' acts as '(').
          
        Example Walkthrough for s = "(*)" :
        - Initial: minopen = 0, maxopen = 0
        - char = '(' : minopen = 1, maxopen = 1
        - char = '*' : minopen = max(0, 1 - 1) = 0, maxopen = 1 + 1 = 2
        - char = ')' : minopen = max(0, 0 - 1) = 0, maxopen = 2 - 1 = 1
        - Final return: minopen == 0 (True)
        """
        minopen = 0
        maxopen = 0
        
        for char in s:
            if char == '(':
                minopen += 1
                maxopen += 1
            elif char == '*':
                # '*' can act as ')' (reducing minopen, clamped at 0) 
                # or '(' (increasing maxopen)
                minopen = max(0, minopen - 1)
                maxopen += 1
            elif char == ')':
                minopen = max(0, minopen - 1)
                maxopen -= 1
                
            # If maxopen drops below 0, it means we have more ')' than '(' and '*' combined.
            # The string is instantly invalid.
            if maxopen < 0:
                return False
                
        # All open parentheses are successfully balanced if minopen reaches 0.
        return minopen == 0

# --- Example Usage ---
sol = Solution()

s1 = "(*)"
print(f"Is '{s1}' valid? {sol.checkValidString(s1)}")  # Output: True

s2 = "(*))"
print(f"Is '{s2}' valid? {sol.checkValidString(s2)}")  # Output: True

s3 = "((*"
print(f"Is '{s3}' valid? {sol.checkValidString(s3)}")  # Output: False
