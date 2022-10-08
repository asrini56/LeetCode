#131. Palindrome Partitioning, Time - O(N.2^N), Space - O(N)
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        ans = []
        def isPalindrome(string):
            if not string:
                return False
            if string == string[::-1]:
                return True
            return False
        def backtrack(st,temp):
            if st >= len(s):
                ans.append(temp[:])
                return
            for i in range(st,len(s)):
                if isPalindrome(s[st:i+1]):
                    temp.append(s[st:i+1])
                    backtrack(i+1,temp)
                    temp.pop(len(temp)-1)
        backtrack(0,[])
        return ans
