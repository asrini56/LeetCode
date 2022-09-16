#567. Permutation in String Time/Space - O(n)/O(s1)
import collections
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False
        temp = collections.Counter(s1)
        s = ""
        temp1 = {}
        j = 0
        count = 0
        for i in range(len(s2)):
            count+=1
            if s2[i] in temp1:
                temp1[s2[i]]+=1
            else:
                temp1[s2[i]] = 1
            if len(s1) == count:
                if temp1 == temp:
                    return True
                else:
                    temp1[s2[j]]-=1
                    if temp1[s2[j]] == 0:
                        del temp1[s2[j]]
                    j+=1
                    count-=1
        return False
