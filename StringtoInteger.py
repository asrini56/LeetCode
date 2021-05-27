class Solution:
    def myAtoi(self, s: str) -> int:
        if not s:
            return 0
        n=""
        if len(s)==0:
            return 0
        while s and s[0]==" ":
            s=s[1:]
        for i in range(len(s)):
            if s[i]==" ":
                break
            elif i==0:
                if (s[i]=="-" or s[i]=="+"):
                     n+=s[i]
                elif s[i].isnumeric():
                    n+=s[i]
                else:
                    break
            elif s[i].isnumeric():
                n+=s[i]
            else:
                break
        if n=="+" or n=="-":
            return 0
        if len(n)==0:
            return 0
        if int(n)>2**31-1:
            return int(2**31)-1
        if int(n)<-2**31:
            return int(-2**31)
        return int(n)
