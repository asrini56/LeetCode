"""
1] If the s.length < k we cannot construct k strings from s and answer is false.
2] If the number of characters that have odd counts is > k then the minimum number of palindrome strings we can construct is > k and answer is false.
"""

class Solution:
    def canConstruct(self, s: str, k: int) -> bool:
        count = Counter(s)
        odd = 0
        for c in count:
            if count[c] % 2 != 0:
                odd+=1
        if odd > k or len(s) < k:
            return False
        return True
