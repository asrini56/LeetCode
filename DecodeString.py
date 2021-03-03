#394. Decode String, Time - O(n)
class Solution:
    def decodeString(self, s: str) -> str:
        stackNum = []
        stackArr = []
        result = ""
        num = ""
        for char in s:
            if char.isdigit():
                num = num + char
            elif char == "[":
                n = int(num)
                stackNum.append(n)
                stackArr.append(result)
                num = ""
                result = ""
            elif char == "]":
                result = stackArr.pop() + stackNum.pop() * result
            else:
                result = result + char
        return result   
            
