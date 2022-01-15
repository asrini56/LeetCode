"""
We use three flags: met_dot, met_e, met_digit, mark if we have met ., e or any digit so far. First we strip the string, then go through each char and make sure:

If char == + or char == -, then prev char (if there is) must be e
. cannot appear twice or after e
e cannot appear twice, and there must be at least one digit before and after e
All other non-digit char is invalid
"""
class Solution:
    def isNumber(self, s: str) -> bool:
        s = s.strip()
        met_dot = met_e = met_digit = False
        for i, char in enumerate(s):
            if char in ['+', '-']:
                if i > 0 and s[i-1] != 'e':
                    return False
            elif char == '.':
                if met_dot or met_e: return False
                met_dot = True
            elif char in ['E','e']:
                if met_e or not met_digit:
                    return False
                met_e, met_digit = True, False
            elif char.isdigit():
                met_digit = True
            else:
                return False
        return met_digit
