#471. Encode String with Shortest Length
from functools import lru_cache
class Solution:
    def encode(self, s: str) -> str:
        @lru_cache(maxsize=None)
        def f(s):
            if s=='': return ''
            # take the complete string
            l = [s]
            # split string at each possible index and encode two parts separately
            l += [s[0:i] + f(s[i:]) for i in range(1, len(s))]

            # try to encode each repeating prefix
            for i in range(1, len(s)+1):
                x = s[0:i]
                j, count = i, 1
                while s.find(x, j)==j:
                    j += len(x)
                    count += 1
                    l += ['%d[%s]' % (count, f(x)) + f(s[j:])]
            return min(l, key=len)
        return f(s)
