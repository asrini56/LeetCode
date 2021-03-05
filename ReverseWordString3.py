#557. Reverse Words in a String III, Time -O(n)
class Solution:
    def reverseWords(self, s: str) -> str:
        l = s.split(' ')
        ans = []
        for i in range(len(l)):
            if i!= len(l)-1:
                ans.append(l[i][::-1])
                ans.append(" ")
            else:
                ans.append(l[i][::-1])
        return ''.join(ans)
        
