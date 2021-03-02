#443. String Compression, Time - O(n)
class Solution:
    def compress(self, chars: List[str]) -> int:
        if chars == None or len(chars) < 1:
            return 0
        index = 0
        i = 0
        while i < len(chars):
            j = i
            while j < len(chars) and chars[i] == chars[j]:
                j+=1
            chars[index] = chars[i]
            index+=1
            if j-i > 1:
                s = str(j-i)
                for i1 in range(len(s)):
                    chars[index] = s[i1]
                    index+=1
            i = j
        return index
