class Solution:
    def largestGoodInteger(self, num: str) -> str:
        if len(num) < 3:
            return ""
        m = float("-inf")
        res = ""
        for i in range(len(num)-2):
            s = ""
            s = str(num[i])
            for j in range(i+1,i+3):
                if num[j] != num[i]:
                    break
                else:
                    s = s + str(num[j])
            if len(s) == 3:
                if m < int(s):
                    m = int(s)
                    res = s
        if res:
            return res
        else:
            return ""
