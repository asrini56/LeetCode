#5. Longest Palindromic Substring, Time - O(n^2)
class Solution:
    def longestPalindrome(self, s: str) -> str:
        def getIndex(s,left,right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                if s[left]!=s[right]:
                    break
                left = left-1
                right = right + 1
            return [left+1,right]
        if not s:
            return ""
        result = [0,1]
        for i in range(1,len(s)):
            odd = getIndex(s,i-1,i+1)
            even = getIndex(s,i-1,i)
            if odd[1] - odd[0] >= even[1] - even[0]:
                temp = odd
            else:
                temp = even
            if temp[1] - temp[0] > result[1] - result[0]:
                result = temp
        return s[result[0]:result[1]]
