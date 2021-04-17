#819. Most Common Word, Time,Space - O(N+M)
import collections
class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        p = ""
        for i in range(len(paragraph)):
            if paragraph[i].isalnum():
                p+=paragraph[i]
            else:
                p+=' '
        l = p.split()
        d = {}
        ban = {}
        for i in range(len(l)):
            k = l[i].lower()
            if k not in d:
                d[k] = 1
            else:
                d[k]+=1
        maximum = []
        ban = set(banned)
        for i in d:
            if i not in ban:
                if not maximum:
                    maximum = (i,d[i])
                if maximum:
                    if maximum[1] < d[i]:
                        maximum = (i,d[i])
        return maximum[0].lower()
