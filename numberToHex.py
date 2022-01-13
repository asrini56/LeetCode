class Solution:
    def toHex(self, num: int) -> str:
        if num < 0:            
            num &= 0xffffffff
            
        chars = "0123456789abcdef";            
        
        result = []
        while num:
            num, d = divmod(num, 16)
            result.append(chars[d])
            
        return "".join(reversed(result)) or "0"
