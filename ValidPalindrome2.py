#680. Valid Palindrome II, Time - O(N), Space - O(1)
class Solution:
    def validPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1
        while left < right:
            if s[left] == s[right]:
                left+=1
                right-=1
            else:
                s1 = s[:left]+s[left+1:]
                if self.isPalindrome(s1):
                    return True
                s2 = s[:right] + s[right+1:]
                if self.isPalindrome(s2):
                    return True
                return False
        return True
    def isPalindrome(self,s):
        if s == s[::-1]:
            return True
        else:
            return False
