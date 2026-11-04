class Solution:
    def romanToInt(self, s: str) -> int:
        """
        Roman to Integer (LeetCode 13)
        ------------------------------
        Core Logic: Normally, Roman numerals are added from left to right.
        However, when a smaller value precedes a larger value (subtractive notation, 
        e.g., 'IV' or 'XC'), we subtract the smaller value instead of adding it.
        """
        r = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        tot = 0
        
        # Iterate through all characters except the last one
        for i in range(len(s) - 1):
            # If current numeral is smaller than the next, it's a subtractive pair
            if r[s[i]] < r[s[i+1]]:
                tot -= r[s[i]]
            else:
                tot += r[s[i]]
                
        # Always add the very last character
        tot += r[s[-1]]
        return tot


# ==========================================
# EXAMPLE WALKTHROUGH
# ==========================================
if __name__ == "__main__":
    solution = Solution()
    
    # Example: s = "MCMXCIV" (which equals 1994)
    #
    # Trace:
    # 1. 'M' (1000) -> Next is 'C' (100). 1000 < 100 is False -> Add 1000  (tot = 1000)
    # 2. 'C' (100)  -> Next is 'M' (1000). 100 < 1000 is True  -> Subtract 100 (tot = 900)
    # 3. 'M' (1000) -> Next is 'X' (10).   1000 < 10 is False  -> Add 1000  (tot = 1900)
    # 4. 'X' (10)   -> Next is 'C' (100).  10 < 100 is True    -> Subtract 10  (tot = 1890)
    # 5. 'C' (100)  -> Next is 'I' (1).    100 < 1 is False    -> Add 100   (tot = 1990)
    # Loop ends. 
    # 6. Add last char 'V' (5) -> tot = 1990 + 5 = 1995? Wait, let's look at last two: 'I' (1) and 'V' (5).
    #    At index 4 ('I'): 'I' (1) < 'V' (5) is True -> Subtract 1 (tot = 1989).
    #    Add last char 'V' (5) -> tot = 1989 + 5 = 1994.
    
    s = "MCMXCIV"
    result = solution.romanToInt(s)
    
    print(f"Roman Numeral: {s}")
    print(f"Integer Value: {result}")  # Output: 1994
