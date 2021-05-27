#5. Longest Palindromic Substring, Time - O(n)
class Solution:
    def longestPalindrome(self, s: str) -> str:
        s = '#' + '#'.join(s) + '#'
        dp = [1] * len(s)
        center = 0
        for i, _ in enumerate(s):
            if dp[center] + center > i:
                dp[i] = min(dp[2*center-i], dp[center]+center-i) 
            while i - dp[i] >= 0 and i + dp[i] < len(s) and s[i-dp[i]] == s[i+dp[i]]:
                dp[i] += 1
            if dp[i] > dp[center]:
                center = i
        return s[center-dp[center]+2:center+dp[center]:2]
