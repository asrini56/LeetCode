#Minimum Window Substring, Time - O(|s| + |t|), Space - O(|s| + |t|).|s|
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""
        d = Counter(t)
        required = len(d)
        l = 0
        r = 0
        formed = 0
        window = {}
        ans = float("inf"), None, None
        while r < len(s):
            c = s[r]
            if c not in window:
                window[c] = 1
            else:
                window[c]+=1
            if c in d and d[c] == window[c]:
                formed+=1
            while l <= r and formed == required:
                c = s[l]
                if r - l + 1 < ans[0]:
                    ans = (r - l + 1, l, r)
                window[c]-=1
                if c in d and window[c] < d[c]:
                    formed-=1
                l+=1
            r+=1
        if ans[0] == float("inf"):
            return ""
        return s[ans[1] : ans[2] + 1]
                
            
        
