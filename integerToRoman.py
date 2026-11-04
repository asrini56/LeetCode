class Solution:
    def intToRoman(self, num: int) -> str:
        """
        Integer to Roman (LeetCode 12)
        ------------------------------
        Time Complexity: O(1) - The maximum number of iterations is bounded because 
                                the maximum input value is 3999.
        Space Complexity: O(1) - The resulting string length is at most 15 characters.
        """
        # Predefined mapping of integer values to Roman symbols, 
        # including all standard subtractive combinations.
        digits = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), 
            (100, "C"),  (90, "XC"),  (50, "L"),  (40, "XL"), 
            (10, "X"),   (9, "IX"),   (5, "V"),   (4, "IV"),  (1, "I")
        ]
        
        roman_digits = []
        
        for value, symbol in digits:
            if num == 0: 
                break
                
            # Count how many times the current value fits into num
            c = 0
            while num >= value:
                num -= value
                c += 1
                
            # Append the symbol repeated 'c' times
            roman_digits.append(symbol * c)
            
        return "".join(roman_digits)


# ==========================================
# EXAMPLE WALKTHROUGH (num = 1994)
# ==========================================
if __name__ == "__main__":
    solution = Solution()
    
    # Trace for num = 1994:
    # 1. value = 1000 ("M"): fits 1 time. num becomes 994. Appends "M".
    # 2. value = 900  ("CM"): fits 1 time. num becomes 94.  Appends "CM".
    # 3. value = 500  ("D") : 94 >= 500 is False.
    # 4. value = 400  ("CD"): 94 >= 400 is False.
    # 5. value = 100  ("C") : 94 >= 100 is False.
    # 6. value = 90   ("XC"): fits 1 time. num becomes 4.   Appends "XC".
    # 7. value = 50   ("L") : 4 >= 5 is False.
    # ... (skips smaller ones until 4)
    # 8. value = 4    ("IV"): fits 1 time. num becomes 0.   Appends "IV".
    # 9. num == 0 -> breaks out of loop.
    #
    # Result: "".join(["M", "CM", "XC", "IV"]) -> "MCMXCIV"
    
    result = solution.intToRoman(1994)
    print(f"Integer: 1994")
    print(f"Roman Numeral: {result}")  # Output: MCMXCIV
