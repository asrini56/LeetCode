class Solution:
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == "0":
            return 0
            
        n = len(s)
        # Base cases: 
        # prev2 corresponds to ways[0] = 1
        # prev1 corresponds to ways[1] = 1
        prev2 = 1
        prev1 = 1
        
        for i in range(2, n + 1):
            current = 0
            
            # 1. Single digit decode (1-9)
            if s[i-1] != "0":
                current += prev1
                
            # 2. Two digit decode (10-26)
            two_digit = int(s[i-2:i])
            if 10 <= two_digit <= 26:
                current += prev2
                
            # Shift our window forward for the next iteration
            prev2 = prev1
            prev1 = current
            
        return prev1
