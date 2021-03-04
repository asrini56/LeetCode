#3. Longest Substring Without Repeating Characters, Time - O(n)
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        dictionary = {}
        i = 0
        curr = [0,1]
        st = 0
        for i in range(len(s)):
            if s[i] in dictionary.keys():
                st = max(st,dictionary[s[i]]+1)
            if curr[1] - curr[0] < (i+1) - st:
                curr = [st,i+1]
            dictionary[s[i]] = i
        return len(s[curr[0]:curr[1]])
