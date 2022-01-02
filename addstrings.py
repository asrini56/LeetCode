class Solution:
    def addStrings(self, num1: str, num2: str) -> str:
        n1 = list(num1)
        n2 = list(num2)
        res = []
        carry = 0
        while n1 or n2:
            m = 0
            n = 0
            if n1:
                n = ord(n1.pop()) - ord('0')
            if n2:
                m = ord(n2.pop()) - ord('0')
            carry,rem = divmod(n + m + carry,10)
            res.append(str(rem))
        if carry:
            res.append(str(carry))
        return ''.join(res)[::-1]
