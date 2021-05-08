#438. Find All Anagrams in a String, Time - O(ns + np), space - O(1)
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        if len(s) < len(p):
            return []
        result = []
        p_count = Counter(p)
        s_count = Counter()
        np = len(p)
        for i in range(len(s)):
            s_count[s[i]]+=1
            if i >= len(p):
                if s_count[s[i - np]] == 1:
                    del s_count[s[i - np]]
                else:
                    s_count[s[i - np]] -= 1
            if p_count == s_count:
                result.append(i - len(p) + 1)
        return result
